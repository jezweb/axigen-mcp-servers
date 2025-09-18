"""
FastMCP Axigen Filters Server
==============================
MCP server for managing Axigen email filters, whitelist, blacklist, and spam settings.
No environment variables required - all credentials passed as parameters.
"""

import logging
from typing import Dict, List, Optional, Any
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
    name="Axigen Filters Manager",
    instructions="""
    Axigen Filters Server for MCP - Email Filtering and Rules Management

    This server provides comprehensive email filtering management for Axigen
    accounts without requiring environment variables. All credentials are
    passed dynamically to each tool.

    Key Features:
    - Whitelist management (add/remove/list trusted senders)
    - Blacklist management (block unwanted senders)
    - Anti-spam and anti-virus settings
    - Filter presets and custom rules
    - Address book integration options

    All tools require email, password, and server_url as parameters.
    The server handles session management automatically with caching for efficiency.

    Note: Filter rules management requires understanding of Axigen's filter
    syntax and conditions. Complex filters should be tested carefully.
    """
)

# ============================================================================
# Anti-Spam/Anti-Virus Settings
# ============================================================================

@mcp.tool()
async def get_spam_settings(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get anti-spam and anti-virus (AVAS) settings.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL (e.g., https://mail.example.com)

    Returns:
        Current AVAS settings including whitelist/blacklist options
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get AVAS settings
        settings = await quick_request(
            email, password, server_url,
            "GET", "account/avas"
        )

        return format_success(settings, "Spam settings retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting spam settings: {e}")
        return format_error(str(e), "AVAS_ERROR")


@mcp.tool()
async def update_spam_settings(
    email: str,
    password: str,
    server_url: str,
    whitelist_include_addressbook: Optional[bool] = None,
    blacklist_exclude_addressbook: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update anti-spam settings for address book integration.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        whitelist_include_addressbook: Auto-include address book contacts in whitelist
        blacklist_exclude_addressbook: Exclude address book contacts from blacklist

    Returns:
        Updated AVAS settings
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Build update data
        update_data = {}
        if whitelist_include_addressbook is not None:
            update_data["whitelistIncludeAddressBook"] = whitelist_include_addressbook
        if blacklist_exclude_addressbook is not None:
            update_data["blacklistExcludeAddressBook"] = blacklist_exclude_addressbook

        if not update_data:
            return format_error("No settings to update", "NO_UPDATE")

        # Update AVAS settings
        result = await quick_request(
            email, password, server_url,
            "PATCH", "account/avas",
            data=update_data
        )

        return format_success(result, "Spam settings updated successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error updating spam settings: {e}")
        return format_error(str(e), "UPDATE_ERROR")


# ============================================================================
# Whitelist Management
# ============================================================================

@mcp.tool()
async def get_whitelist(
    email: str,
    password: str,
    server_url: str,
    start: int = 0,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Get whitelisted email addresses.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        start: Starting position for pagination (default: 0)
        limit: Maximum number of items to retrieve (default: 100)

    Returns:
        List of whitelisted email addresses with total count
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get whitelist
        result = await quick_request(
            email, password, server_url,
            "GET", "account/avas/whitelist",
            params={"start": start, "limit": limit}
        )

        return format_success(result, "Whitelist retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting whitelist: {e}")
        return format_error(str(e), "WHITELIST_ERROR")


@mcp.tool()
async def add_to_whitelist(
    email: str,
    password: str,
    server_url: str,
    email_address: str
) -> Dict[str, Any]:
    """
    Add an email address to the whitelist.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        email_address: Email address to whitelist

    Returns:
        Created whitelist entry with ID
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        valid, error = validate_email_address(email_address)
        if not valid:
            return format_error(f"Invalid email to whitelist: {error}", "INVALID_EMAIL")

        # Add to whitelist
        result = await quick_request(
            email, password, server_url,
            "POST", "account/avas/whitelist",
            data={"emailAddress": email_address}
        )

        return format_success(result, f"'{email_address}' added to whitelist")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except APIError as e:
        if "already exists" in str(e).lower():
            return format_error(f"'{email_address}' is already whitelisted", "DUPLICATE_ENTRY")
        return format_error(str(e), "API_ERROR")
    except Exception as e:
        logger.error(f"Error adding to whitelist: {e}")
        return format_error(str(e), "ADD_ERROR")


@mcp.tool()
async def remove_from_whitelist(
    email: str,
    password: str,
    server_url: str,
    whitelist_id: str
) -> Dict[str, Any]:
    """
    Remove an email address from the whitelist.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        whitelist_id: ID of the whitelist entry to remove

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

        # Remove from whitelist
        await quick_request(
            email, password, server_url,
            "DELETE", f"account/avas/whitelist/{whitelist_id}"
        )

        return format_success({"id": whitelist_id}, "Email removed from whitelist")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error removing from whitelist: {e}")
        return format_error(str(e), "REMOVE_ERROR")


# ============================================================================
# Blacklist Management
# ============================================================================

@mcp.tool()
async def get_blacklist(
    email: str,
    password: str,
    server_url: str,
    start: int = 0,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Get blacklisted email addresses.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        start: Starting position for pagination (default: 0)
        limit: Maximum number of items to retrieve (default: 100)

    Returns:
        List of blacklisted email addresses with total count
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get blacklist
        result = await quick_request(
            email, password, server_url,
            "GET", "account/avas/blacklist",
            params={"start": start, "limit": limit}
        )

        return format_success(result, "Blacklist retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting blacklist: {e}")
        return format_error(str(e), "BLACKLIST_ERROR")


@mcp.tool()
async def add_to_blacklist(
    email: str,
    password: str,
    server_url: str,
    email_address: str
) -> Dict[str, Any]:
    """
    Add an email address to the blacklist.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        email_address: Email address to blacklist

    Returns:
        Created blacklist entry with ID
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Note: We allow partial emails/domains for blacklist
        # e.g., "@spam.com" to block entire domain
        if "@" in email_address and email_address != "@":
            # Basic validation for email patterns
            if email_address.startswith("@"):
                # Domain block pattern
                domain = email_address[1:]
                if "." not in domain:
                    return format_error("Invalid domain pattern", "INVALID_PATTERN")
            else:
                # Full email validation
                valid, error = validate_email_address(email_address)
                if not valid:
                    return format_error(f"Invalid email to blacklist: {error}", "INVALID_EMAIL")

        # Add to blacklist
        result = await quick_request(
            email, password, server_url,
            "POST", "account/avas/blacklist",
            data={"emailAddress": email_address}
        )

        return format_success(result, f"'{email_address}' added to blacklist")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except APIError as e:
        if "already exists" in str(e).lower():
            return format_error(f"'{email_address}' is already blacklisted", "DUPLICATE_ENTRY")
        return format_error(str(e), "API_ERROR")
    except Exception as e:
        logger.error(f"Error adding to blacklist: {e}")
        return format_error(str(e), "ADD_ERROR")


@mcp.tool()
async def remove_from_blacklist(
    email: str,
    password: str,
    server_url: str,
    blacklist_id: str
) -> Dict[str, Any]:
    """
    Remove an email address from the blacklist.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        blacklist_id: ID of the blacklist entry to remove

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

        # Remove from blacklist
        await quick_request(
            email, password, server_url,
            "DELETE", f"account/avas/blacklist/{blacklist_id}"
        )

        return format_success({"id": blacklist_id}, "Email removed from blacklist")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error removing from blacklist: {e}")
        return format_error(str(e), "REMOVE_ERROR")


# ============================================================================
# Bulk List Management
# ============================================================================

@mcp.tool()
async def bulk_update_whitelist(
    email: str,
    password: str,
    server_url: str,
    add_emails: Optional[List[str]] = None,
    remove_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Bulk update whitelist - add multiple emails or remove multiple entries.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        add_emails: List of email addresses to add to whitelist
        remove_ids: List of whitelist IDs to remove

    Returns:
        Summary of operations performed
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        if not add_emails and not remove_ids:
            return format_error("No operations specified", "NO_OPERATION")

        results = {
            "added": [],
            "add_errors": [],
            "removed": [],
            "remove_errors": []
        }

        # Add emails
        if add_emails:
            for email_addr in add_emails:
                try:
                    valid, err = validate_email_address(email_addr)
                    if not valid:
                        results["add_errors"].append({
                            "email": email_addr,
                            "error": err
                        })
                        continue

                    result = await quick_request(
                        email, password, server_url,
                        "POST", "account/avas/whitelist",
                        data={"emailAddress": email_addr}
                    )
                    results["added"].append(email_addr)
                except Exception as e:
                    results["add_errors"].append({
                        "email": email_addr,
                        "error": str(e)
                    })

        # Remove IDs
        if remove_ids:
            for id_to_remove in remove_ids:
                try:
                    await quick_request(
                        email, password, server_url,
                        "DELETE", f"account/avas/whitelist/{id_to_remove}"
                    )
                    results["removed"].append(id_to_remove)
                except Exception as e:
                    results["remove_errors"].append({
                        "id": id_to_remove,
                        "error": str(e)
                    })

        # Determine overall success
        total_ops = len(add_emails or []) + len(remove_ids or [])
        successful_ops = len(results["added"]) + len(results["removed"])

        if successful_ops == total_ops:
            return format_success(results, f"All {total_ops} operations completed successfully")
        elif successful_ops > 0:
            return format_success(results, f"{successful_ops}/{total_ops} operations completed")
        else:
            return format_error(results, "BULK_OPERATION_FAILED")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error in bulk whitelist update: {e}")
        return format_error(str(e), "BULK_ERROR")


@mcp.tool()
async def bulk_update_blacklist(
    email: str,
    password: str,
    server_url: str,
    add_emails: Optional[List[str]] = None,
    remove_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Bulk update blacklist - add multiple emails/patterns or remove multiple entries.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        add_emails: List of emails/patterns to add (supports @domain.com for domain blocks)
        remove_ids: List of blacklist IDs to remove

    Returns:
        Summary of operations performed
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        if not add_emails and not remove_ids:
            return format_error("No operations specified", "NO_OPERATION")

        results = {
            "added": [],
            "add_errors": [],
            "removed": [],
            "remove_errors": []
        }

        # Add emails/patterns
        if add_emails:
            for pattern in add_emails:
                try:
                    # Validate pattern
                    if "@" in pattern and pattern != "@":
                        if pattern.startswith("@"):
                            # Domain pattern
                            domain = pattern[1:]
                            if "." not in domain:
                                results["add_errors"].append({
                                    "pattern": pattern,
                                    "error": "Invalid domain pattern"
                                })
                                continue
                        else:
                            # Full email
                            valid, err = validate_email_address(pattern)
                            if not valid:
                                results["add_errors"].append({
                                    "pattern": pattern,
                                    "error": err
                                })
                                continue

                    result = await quick_request(
                        email, password, server_url,
                        "POST", "account/avas/blacklist",
                        data={"emailAddress": pattern}
                    )
                    results["added"].append(pattern)
                except Exception as e:
                    results["add_errors"].append({
                        "pattern": pattern,
                        "error": str(e)
                    })

        # Remove IDs
        if remove_ids:
            for id_to_remove in remove_ids:
                try:
                    await quick_request(
                        email, password, server_url,
                        "DELETE", f"account/avas/blacklist/{id_to_remove}"
                    )
                    results["removed"].append(id_to_remove)
                except Exception as e:
                    results["remove_errors"].append({
                        "id": id_to_remove,
                        "error": str(e)
                    })

        # Determine overall success
        total_ops = len(add_emails or []) + len(remove_ids or [])
        successful_ops = len(results["added"]) + len(results["removed"])

        if successful_ops == total_ops:
            return format_success(results, f"All {total_ops} operations completed successfully")
        elif successful_ops > 0:
            return format_success(results, f"{successful_ops}/{total_ops} operations completed")
        else:
            return format_error(results, "BULK_OPERATION_FAILED")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error in bulk blacklist update: {e}")
        return format_error(str(e), "BULK_ERROR")


# ============================================================================
# Filter Presets (Note: Full filter rules API may not be available)
# ============================================================================

@mcp.tool()
async def get_filter_info(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get information about available filter capabilities.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Information about filter settings and capabilities
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Note: The filters API endpoints may vary by Axigen version
        # This is a placeholder for filter information
        info = {
            "whitelist_addressbook_integration": "Available - use update_spam_settings",
            "blacklist_addressbook_integration": "Available - use update_spam_settings",
            "whitelist_management": "Full CRUD operations available",
            "blacklist_management": "Full CRUD operations available",
            "domain_blocking": "Supported via @domain.com pattern in blacklist",
            "custom_filters": "May require WebAdmin or direct server configuration",
            "note": "Complex filter rules typically configured via WebAdmin interface"
        }

        # Try to get current AVAS settings for completeness
        try:
            avas = await quick_request(
                email, password, server_url,
                "GET", "account/avas"
            )
            info["current_settings"] = avas
        except:
            pass

        return format_success(info, "Filter information retrieved")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting filter info: {e}")
        return format_error(str(e), "INFO_ERROR")


# ============================================================================
# Run the server (for local testing)
# ============================================================================

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run())