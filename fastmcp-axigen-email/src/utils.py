"""Utility functions for Axigen Email API operations."""

import httpx
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime

async def make_request(
    email: str,
    password: str,
    server_url: str,
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make an authenticated request to the Axigen API.

    Args:
        email: User email for authentication
        password: User password for authentication
        server_url: Axigen server URL
        method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        endpoint: API endpoint path
        data: Optional request body data
        params: Optional query parameters

    Returns:
        API response as dictionary
    """
    credentials = f"{email}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    url = f"{server_url}{endpoint}"

    try:
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params
            )

            if response.status_code == 401:
                return {
                    "success": False,
                    "error": "Authentication failed. Please check your credentials."
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": f"Endpoint not found: {endpoint}"
                }
            elif response.status_code >= 400:
                error_msg = f"API error {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg = error_data["error"]
                    elif "message" in error_data:
                        error_msg = error_data["message"]
                except:
                    error_msg = f"API error {response.status_code}: {response.text}"
                return {
                    "success": False,
                    "error": error_msg
                }

            try:
                result = response.json()
                return {
                    "success": True,
                    "data": result
                }
            except:
                if response.status_code == 204:
                    return {
                        "success": True,
                        "data": {}
                    }
                return {
                    "success": True,
                    "data": {"text": response.text}
                }

    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timed out"
        }
    except httpx.ConnectError:
        return {
            "success": False,
            "error": f"Failed to connect to {server_url}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

async def quick_request(
    email: str,
    password: str,
    server_url: str,
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Convenience wrapper for make_request."""
    return await make_request(
        email, password, server_url,
        method, endpoint, data, params
    )

def format_email_list(emails: List[Dict[str, Any]]) -> str:
    """Format a list of emails for display."""
    if not emails:
        return "No emails found"

    result = []
    for email in emails:
        subject = email.get("subject", "(no subject)")
        from_addr = email.get("from", "(unknown)")
        date = email.get("date", "")
        is_unread = email.get("isUnread", False)
        is_flagged = email.get("isFlagged", False)

        status = []
        if is_unread:
            status.append("UNREAD")
        if is_flagged:
            status.append("FLAGGED")
        status_str = f" [{', '.join(status)}]" if status else ""

        result.append(f"- {subject} | From: {from_addr} | {date}{status_str}")

    return "\n".join(result)

def parse_email_addresses(addresses: str) -> List[str]:
    """Parse comma-separated email addresses."""
    if not addresses:
        return []
    return [addr.strip() for addr in addresses.split(",") if addr.strip()]