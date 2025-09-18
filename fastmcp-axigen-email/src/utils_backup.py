"""
Utility Functions for Axigen Settings MCP Server
==================================================
Shared utilities for authentication, HTTP client, and response formatting.
"""

import base64
import logging
import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger(__name__)

# ============================================================================
# Error Classes
# ============================================================================

class AxigenError(Exception):
    """Base exception for Axigen API operations"""
    pass

class AuthenticationError(AxigenError):
    """Failed to authenticate with Axigen server"""
    pass

class SessionExpiredError(AxigenError):
    """Session has expired and needs re-authentication"""
    pass

class APIError(AxigenError):
    """General API error from Axigen server"""
    pass

# ============================================================================
# Response Formatting
# ============================================================================

def format_success(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Format a successful response."""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

def format_error(error: Any, error_code: str = "GENERAL_ERROR") -> Dict[str, Any]:
    """Format an error response."""
    return {
        "success": False,
        "error": {
            "code": error_code,
            "message": str(error)
        },
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# Input Validation
# ============================================================================

def validate_email_address(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format.
    Returns (is_valid, error_message)
    """
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_server_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate server URL format.
    Returns (is_valid, error_message)
    """
    if not url:
        return False, "Server URL is required"

    if not url.startswith(('http://', 'https://')):
        return False, "Server URL must start with http:// or https://"

    # Remove trailing slash for consistency
    if url.endswith('/'):
        url = url[:-1]

    return True, None

# ============================================================================
# Session Management
# ============================================================================

class AxigenSession:
    """
    Manages authentication and session state for Axigen API calls.
    Handles automatic re-authentication when session expires.
    """

    def __init__(self, email: str, password: str, server_url: str):
        """
        Initialize session with credentials.

        Args:
            email: User's email address
            password: User's password
            server_url: Axigen server URL (without /api/v1)
        """
        self.email = email
        self.password = password
        self.server_url = server_url.rstrip('/')
        self.base_url = f"{self.server_url}/api/v1"

        # Session state
        self.session_id: Optional[str] = None
        self.auth_header: str = self._create_basic_auth(email, password)
        self.expires_at: Optional[datetime] = None

        # HTTP client (will be initialized on first use)
        self._http_session: Optional[aiohttp.ClientSession] = None

        # Session cache TTL (30 minutes)
        self.session_ttl = timedelta(minutes=30)

    def _create_basic_auth(self, email: str, password: str) -> str:
        """Create Basic Authentication header value."""
        credentials = f"{email}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode('ascii')
        return f"Basic {encoded}"

    async def _ensure_http_session(self):
        """Ensure HTTP session is created."""
        if self._http_session is None or self._http_session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._http_session = aiohttp.ClientSession(timeout=timeout)

    async def authenticate(self) -> str:
        """
        Authenticate with Axigen server and obtain session ID.

        Returns:
            Session ID string

        Raises:
            AuthenticationError: If authentication fails
        """
        await self._ensure_http_session()

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json"
        }

        try:
            async with self._http_session.post(
                f"{self.base_url}/login",
                headers=headers
            ) as response:
                if response.status == 401:
                    raise AuthenticationError("Invalid email or password")
                elif response.status != 200:
                    text = await response.text()
                    raise AuthenticationError(f"Authentication failed: {response.status} - {text}")

                data = await response.json()
                self.session_id = data.get("sessid")
                if not self.session_id:
                    raise AuthenticationError("No session ID received from server")

                # Set expiration time
                self.expires_at = datetime.now() + self.session_ttl

                logger.info(f"Successfully authenticated as {self.email}")
                return self.session_id

        except aiohttp.ClientError as e:
            raise AuthenticationError(f"Connection error: {str(e)}")

    def is_session_valid(self) -> bool:
        """Check if current session is still valid."""
        if not self.session_id or not self.expires_at:
            return False
        return datetime.now() < self.expires_at

    async def ensure_authenticated(self):
        """Ensure we have a valid session, re-authenticating if necessary."""
        if not self.is_session_valid():
            await self.authenticate()

    async def make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to Axigen API.

        Args:
            method: HTTP method (GET, POST, PATCH, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            json_data: JSON body data
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data as dictionary

        Raises:
            APIError: If request fails
        """
        # Ensure we have valid session
        await self.ensure_authenticated()
        await self._ensure_http_session()

        # Build request headers
        request_headers = {
            "Authorization": self.auth_header,
            "X-Axigen-Session": self.session_id,
            "Content-Type": "application/json"
        }
        if headers:
            request_headers.update(headers)

        # Build full URL
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        url = f"{self.base_url}/{endpoint}"

        # Make request with retry on 401
        for attempt in range(2):
            try:
                async with self._http_session.request(
                    method=method,
                    url=url,
                    json=json_data,
                    params=params,
                    headers=request_headers
                ) as response:

                    # Handle authentication errors
                    if response.status == 401:
                        if attempt == 0:
                            # First attempt failed, try re-authenticating
                            logger.info("Session expired, re-authenticating...")
                            self.session_id = None
                            await self.authenticate()
                            request_headers["X-Axigen-Session"] = self.session_id
                            continue
                        else:
                            raise AuthenticationError("Authentication failed after retry")

                    # Handle successful empty responses
                    if response.status in (200, 201, 204):
                        if response.status == 204:
                            return {}

                        content_type = response.headers.get('content-type', '')
                        if 'application/json' in content_type:
                            return await response.json()
                        else:
                            # Return raw text for non-JSON responses
                            text = await response.text()
                            return {"raw_response": text}

                    # Handle errors
                    error_text = await response.text()
                    raise APIError(f"API request failed: {response.status} - {error_text}")

            except aiohttp.ClientError as e:
                raise APIError(f"Connection error: {str(e)}")

        raise APIError("Request failed after retries")

    async def close(self):
        """Close HTTP session."""
        if self._http_session:
            await self._http_session.close()

    async def __aenter__(self):
        """Context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

# ============================================================================
# Session Cache (for reusing sessions across tool calls)
# ============================================================================

class SessionCache:
    """
    Cache for Axigen sessions to avoid re-authentication on every tool call.
    Sessions are cached by (email, server_url) tuple.
    """

    def __init__(self, ttl_minutes: int = 25):
        self._cache: Dict[Tuple[str, str], AxigenSession] = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def get_session(self, email: str, password: str, server_url: str) -> AxigenSession:
        """
        Get or create a session for the given credentials.

        Args:
            email: User's email
            password: User's password
            server_url: Axigen server URL

        Returns:
            AxigenSession instance
        """
        cache_key = (email.lower(), server_url.rstrip('/'))

        # Check if we have a cached session
        if cache_key in self._cache:
            session = self._cache[cache_key]
            # Verify password hasn't changed
            new_auth = base64.b64encode(f"{email}:{password}".encode()).decode('ascii')
            if session.auth_header == f"Basic {new_auth}":
                logger.debug(f"Using cached session for {email}")
                return session
            else:
                # Password changed, remove old session
                logger.info(f"Password changed for {email}, creating new session")
                del self._cache[cache_key]

        # Create new session
        logger.info(f"Creating new session for {email}")
        session = AxigenSession(email, password, server_url)
        self._cache[cache_key] = session
        return session

    def clear_expired(self):
        """Remove expired sessions from cache."""
        now = datetime.now()
        expired_keys = [
            key for key, session in self._cache.items()
            if not session.is_session_valid()
        ]
        for key in expired_keys:
            logger.debug(f"Removing expired session for {key[0]}")
            del self._cache[key]

    async def close_all(self):
        """Close all cached sessions."""
        for session in self._cache.values():
            await session.close()
        self._cache.clear()

# Global session cache instance
_session_cache = SessionCache()

def get_session_cache() -> SessionCache:
    """Get the global session cache instance."""
    return _session_cache

# ============================================================================
# Convenience Functions
# ============================================================================

async def quick_request(
    email: str,
    password: str,
    server_url: str,
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Make a quick authenticated request without managing session manually.

    Args:
        email: User's email
        password: User's password
        server_url: Axigen server URL
        method: HTTP method
        endpoint: API endpoint
        data: Request data
        params: Query parameters

    Returns:
        Response data
    """
    session = get_session_cache().get_session(email, password, server_url)
    return await session.make_request(method, endpoint, json_data=data, params=params)