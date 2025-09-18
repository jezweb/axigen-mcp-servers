"""
FastMCP Axigen Settings Server
===============================
MCP server for managing Axigen account settings, signatures, and preferences.
No environment variables required - all credentials passed as parameters.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastmcp import FastMCP

# Import utilities
from src.utils import (
    format_success, format_error,
    validate_email_address, validate_server_url,
    get_session_cache, quick_request,
    AxigenError, AuthenticationError, APIError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Server Creation - MUST be at module level for FastMCP Cloud
# ============================================================================

mcp = FastMCP(
    name="Axigen Settings Manager",
    instructions="""
    Axigen Settings Server for MCP - Account Settings and Preferences

    This server provides comprehensive account settings management for Axigen
    email accounts without requiring environment variables. All credentials
    are passed dynamically to each tool.

    Key Features:
    - Account preferences (language, timezone, themes)
    - Email signatures management (CRUD operations)
    - Vacation/auto-reply configuration
    - Avatar management
    - Contact information updates
    - UI settings storage
    - Custom client settings

    All tools require email, password, and server_url as parameters.
    The server handles session management automatically with caching for efficiency.
    """
)

# ============================================================================
# Account Settings Tools
# ============================================================================

@mcp.tool()
async def get_account_settings(
    email: str,

    password: str,

    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get all account settings and preferences.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL (optional, defaults to https://ax.email)

    Returns:
        Complete account settings including language, timezone, theme, etc.
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get account settings
        settings = await quick_request(
            email, password, server_url,
            "GET", "account/settings"
        )

        return format_success(settings, "Account settings retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting account settings: {e}")
        return format_error(str(e), "SETTINGS_ERROR")


@mcp.tool()
async def update_account_settings(
    email: str,
    password: str,
    settings: Dict[str, Any],
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Update account settings and preferences.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        settings: Dictionary of settings to update. Supported fields:
            - archivingPolicy: "none", "folderPerYear", "folderPerMonth"
            - conversationView: boolean
            - theme: "ocean", "breeze", "neutral"
            - language: ISO language code (e.g., "en", "es", "fr")
            - timezone: Timezone string (e.g., "UTC", "America/New_York")
            - dateFormat: Date format string
            - timeFormat: Time format string
            - deleteToTrash: boolean
            - confirmMailDelete: boolean
            - autoAddRecipients: boolean
            - purgeTrashOnLogout: boolean
            - purgeSpamOnLogout: boolean

    Returns:
        Success confirmation or error details
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Update settings (PATCH only updates provided fields)
        await quick_request(
            email, password, server_url,
            "PATCH", "account/settings",
            data=settings
        )

        return format_success(settings, "Account settings updated successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error updating account settings: {e}")
        return format_error(str(e), "UPDATE_ERROR")


# ============================================================================
# Signatures Management
# ============================================================================

@mcp.tool()
async def get_signatures(
    email: str,

    password: str,

    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get all email signatures for the account.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        List of signatures with their IDs, names, and content
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get signatures
        signatures = await quick_request(
            email, password, server_url,
            "GET", "account/signatures"
        )

        return format_success(signatures, "Signatures retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting signatures: {e}")
        return format_error(str(e), "SIGNATURES_ERROR")


@mcp.tool()
async def create_signature(
    email: str,
    password: str,
    name: str,
    content_html: str,
    content_text: Optional[str] = None,
    is_default: bool = False,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Create a new email signature.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        name: Signature name
        content_html: HTML content of the signature
        content_text: Plain text content (optional, auto-generated if not provided)
        is_default: Whether to set as default signature

    Returns:
        Created signature details including ID
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Prepare signature data
        signature_data = {
            "name": name,
            "htmlContent": content_html,
            "isDefault": is_default
        }
        if content_text:
            signature_data["textContent"] = content_text

        # Create signature
        result = await quick_request(
            email, password, server_url,
            "POST", "account/signatures",
            data=signature_data
        )

        return format_success(result, f"Signature '{name}' created successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error creating signature: {e}")
        return format_error(str(e), "CREATE_ERROR")


@mcp.tool()
async def update_signature(
    email: str,
    password: str,
    signature_id: str,
    name: Optional[str] = None,
    content_html: Optional[str] = None,
    content_text: Optional[str] = None,
    is_default: Optional[bool] = None,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Update an existing email signature.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        signature_id: ID of the signature to update
        name: New signature name (optional)
        content_html: New HTML content (optional)
        content_text: New plain text content (optional)
        is_default: Whether to set as default (optional)

    Returns:
        Updated signature details
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Build update data (only include provided fields)
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if content_html is not None:
            update_data["htmlContent"] = content_html
        if content_text is not None:
            update_data["textContent"] = content_text
        if is_default is not None:
            update_data["isDefault"] = is_default

        if not update_data:
            return format_error("No fields to update", "NO_UPDATE")

        # Update signature
        result = await quick_request(
            email, password, server_url,
            "PUT", f"account/signatures/{signature_id}",
            data=update_data
        )

        return format_success(result, "Signature updated successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error updating signature: {e}")
        return format_error(str(e), "UPDATE_ERROR")


@mcp.tool()
async def delete_signature(
    email: str,
    password: str,
    signature_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Delete an email signature.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        signature_id: ID of the signature to delete

    Returns:
        Success confirmation
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Delete signature
        await quick_request(
            email, password, server_url,
            "DELETE", f"account/signatures/{signature_id}"
        )

        return format_success({"id": signature_id}, "Signature deleted successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error deleting signature: {e}")
        return format_error(str(e), "DELETE_ERROR")


# ============================================================================
# Vacation/Auto-Reply
# ============================================================================

@mcp.tool()
async def get_vacation_settings(
    email: str,

    password: str,

    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get vacation/auto-reply settings.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Current vacation settings including status and message
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get vacation settings
        settings = await quick_request(
            email, password, server_url,
            "GET", "account/vacation"
        )

        return format_success(settings, "Vacation settings retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting vacation settings: {e}")
        return format_error(str(e), "VACATION_ERROR")


@mcp.tool()
async def set_vacation_reply(
    email: str,
    password: str,
    enabled: bool,
    subject: Optional[str] = None,
    message: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    exclude_contacts: bool = False,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Configure vacation/auto-reply settings.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        enabled: Whether to enable vacation reply
        subject: Auto-reply subject line
        message: Auto-reply message body
        start_date: Start date (ISO format) for vacation period
        end_date: End date (ISO format) for vacation period
        exclude_contacts: Whether to exclude known contacts from auto-reply

    Returns:
        Updated vacation settings
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Prepare vacation data
        vacation_data = {
            "enabled": enabled
        }

        if enabled:
            if subject:
                vacation_data["subject"] = subject
            if message:
                vacation_data["message"] = message
            if start_date:
                vacation_data["startDate"] = start_date
            if end_date:
                vacation_data["endDate"] = end_date
            vacation_data["excludeContacts"] = exclude_contacts

        # Set vacation settings
        result = await quick_request(
            email, password, server_url,
            "PUT", "account/vacation",
            data=vacation_data
        )

        status = "enabled" if enabled else "disabled"
        return format_success(result, f"Vacation reply {status} successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error setting vacation reply: {e}")
        return format_error(str(e), "VACATION_ERROR")


# ============================================================================
# Contact Information
# ============================================================================

@mcp.tool()
async def get_contact_info(
    email: str,

    password: str,

    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get account contact information.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Contact information including name, personal email, etc.
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get contact info
        info = await quick_request(
            email, password, server_url,
            "GET", "account/contactinfo"
        )

        return format_success(info, "Contact information retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting contact info: {e}")
        return format_error(str(e), "CONTACT_ERROR")


@mcp.tool()
async def update_contact_info(
    email: str,
    password: str,
    server_url: str,
    title: Optional[str] = None,
    first_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    last_name: Optional[str] = None,
    suffix: Optional[str] = None,
    personal_email: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update account contact information.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        title: Title (e.g., "Dr.", "Prof.", "Mr.", "Ms.")
        first_name: First name
        middle_name: Middle name
        last_name: Last name
        suffix: Name suffix (e.g., "Jr.", "Sr.", "III")
        personal_email: Personal email address

    Returns:
        Success confirmation
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Build contact data
        contact_data = {}
        if title is not None:
            contact_data["title"] = title
        if first_name is not None:
            contact_data["firstName"] = first_name
        if middle_name is not None:
            contact_data["middleName"] = middle_name
        if last_name is not None:
            contact_data["lastName"] = last_name
        if suffix is not None:
            contact_data["suffix"] = suffix
        if personal_email is not None:
            # Validate personal email if provided
            valid, error = validate_email_address(personal_email)
            if not valid:
                return format_error(f"Invalid personal email: {error}", "INVALID_EMAIL")
            contact_data["personalEmailAddress"] = personal_email

        if not contact_data:
            return format_error("No fields to update", "NO_UPDATE")

        # Update contact info
        await quick_request(
            email, password, server_url,
            "PUT", "account/contactinfo",
            data=contact_data
        )

        return format_success(contact_data, "Contact information updated successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error updating contact info: {e}")
        return format_error(str(e), "UPDATE_ERROR")


# ============================================================================
# UI Settings Storage
# ============================================================================

@mcp.tool()
async def get_ui_settings(
    email: str,
    password: str,
    server_url: str,
    client_type: str = "webmail"
) -> Dict[str, Any]:
    """
    Get stored UI settings for WebMail or custom client.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        client_type: "webmail" for WebMail UI settings, "client" for custom client settings

    Returns:
        Stored UI settings string (up to 8KB)
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        if client_type not in ["webmail", "client"]:
            return format_error("client_type must be 'webmail' or 'client'", "INVALID_TYPE")

        # Get UI settings
        endpoint = "account/settings/ui" if client_type == "webmail" else "account/settings/client"
        settings = await quick_request(
            email, password, server_url,
            "GET", endpoint
        )

        return format_success(settings, f"{client_type} UI settings retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting UI settings: {e}")
        return format_error(str(e), "UI_ERROR")


@mcp.tool()
async def save_ui_settings(
    email: str,
    password: str,
    settings_data: str,
    client_type: str = "webmail",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Save UI settings for WebMail or custom client.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        settings_data: Settings string to store (max 8192 bytes)
        client_type: "webmail" for WebMail UI settings, "client" for custom client settings

    Returns:
        Success confirmation
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        if client_type not in ["webmail", "client"]:
            return format_error("client_type must be 'webmail' or 'client'", "INVALID_TYPE")

        # Check size limit
        if len(settings_data.encode('utf-8')) > 8192:
            return format_error("Settings data exceeds 8KB limit", "SIZE_LIMIT")

        # Save UI settings
        endpoint = "account/settings/ui" if client_type == "webmail" else "account/settings/client"
        key = "uiSettings" if client_type == "webmail" else "clientSettings"

        await quick_request(
            email, password, server_url,
            "POST", endpoint,
            data={key: settings_data}
        )

        return format_success(
            {"size": len(settings_data.encode('utf-8'))},
            f"{client_type} UI settings saved successfully"
        )

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error saving UI settings: {e}")
        return format_error(str(e), "SAVE_ERROR")


# ============================================================================
# Account Info
# ============================================================================

@mcp.tool()
async def get_account_info(
    email: str,

    password: str,

    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get comprehensive account information including quotas, limits, and policies.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Complete account information including:
        - Account and domain names
        - Quota usage and limits
        - Message count limits
        - Password policies
        - Security settings
        - Feature restrictions
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get account info
        info = await quick_request(
            email, password, server_url,
            "GET", "account/info"
        )

        return format_success(info, "Account information retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting account info: {e}")
        return format_error(str(e), "INFO_ERROR")


# ============================================================================
# Run the server (for local testing)
# ============================================================================

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run())