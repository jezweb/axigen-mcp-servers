"""
FastMCP Axigen Security Server
===============================
MCP server for managing Axigen account security, passwords, 2FA, and temporary aliases.
No environment variables required - all credentials passed as parameters.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
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
    name="Axigen Security Manager",
    instructions="""
    Axigen Security Server for MCP - Account Security and Authentication

    This server provides comprehensive security management for Axigen accounts
    without requiring environment variables. All credentials are passed
    dynamically to each tool.

    Key Features:
    - Temporary email aliases (create/delete disposable addresses)
    - Password management (change password with policy compliance)
    - Account information (quotas, limits, security policies)
    - Security settings overview
    - Account aliases management

    Note: 2FA configuration typically requires interactive setup through
    WebMail or other clients. This server provides information about
    security policies but cannot fully configure 2FA programmatically.

    All tools require email, password, and server_url as parameters.
    The server handles session management automatically with caching for efficiency.
    """
)

# ============================================================================
# Account Information & Security Overview
# ============================================================================

@mcp.tool()
async def get_security_info(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get comprehensive security information including policies and restrictions.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL (e.g., https://mail.example.com)

    Returns:
        Complete security information including:
        - Password policies and requirements
        - 2FA status and configuration
        - Temporary alias settings
        - Account restrictions
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get account info which includes security policies
        info = await quick_request(
            email, password, server_url,
            "GET", "account/info"
        )

        # Extract security-relevant information
        security_info = {
            "account": info.get("accountName"),
            "domain": info.get("domainName"),
            "twoFactorAuthConfigured": info.get("twoFactorAuthConfigured", False)
        }

        # Extract restrictions if present
        if "restrictions" in info:
            restrictions = info["restrictions"]

            # Password policy
            if "passwordPolicy" in restrictions:
                security_info["passwordPolicy"] = restrictions["passwordPolicy"]

            # Temporary aliases
            if "temporaryAliases" in restrictions:
                security_info["temporaryAliases"] = restrictions["temporaryAliases"]

            # Security policy
            if "securityPolicy" in restrictions:
                security_info["securityPolicy"] = restrictions["securityPolicy"]

        return format_success(security_info, "Security information retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting security info: {e}")
        return format_error(str(e), "INFO_ERROR")


# ============================================================================
# Temporary Email Aliases
# ============================================================================

@mcp.tool()
async def get_temporary_aliases(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get all temporary email aliases for the account.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        List of temporary aliases with their expiration dates
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get temporary aliases
        aliases = await quick_request(
            email, password, server_url,
            "GET", "account/temporaryaliases"
        )

        # Enhance with human-readable expiration info
        if "items" in aliases:
            for alias in aliases["items"]:
                if "expireDate" in alias:
                    try:
                        # Parse ISO date
                        expire_dt = datetime.fromisoformat(alias["expireDate"].replace('Z', '+00:00'))
                        now = datetime.now(expire_dt.tzinfo)
                        remaining = expire_dt - now

                        if remaining.total_seconds() > 0:
                            days = remaining.days
                            hours = remaining.seconds // 3600
                            alias["remaining"] = f"{days} days, {hours} hours"
                            alias["isExpired"] = False
                        else:
                            alias["remaining"] = "Expired"
                            alias["isExpired"] = True
                    except:
                        pass

        return format_success(aliases, "Temporary aliases retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting temporary aliases: {e}")
        return format_error(str(e), "ALIASES_ERROR")


@mcp.tool()
async def create_temporary_alias(
    email: str,
    password: str,
    server_url: str,
    days_valid: int = 7
) -> Dict[str, Any]:
    """
    Create a new temporary email alias.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        days_valid: Number of days the alias should be valid (default: 7)

    Returns:
        Created alias details including generated email address and expiration
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        if days_valid < 1 or days_valid > 365:
            return format_error("days_valid must be between 1 and 365", "INVALID_DAYS")

        # Note: The API typically auto-generates the alias address
        # and sets expiration based on server/domain policies
        result = await quick_request(
            email, password, server_url,
            "POST", "account/temporaryaliases",
            data={}  # Server generates the alias
        )

        # Add user-friendly info
        if "emailAddress" in result:
            result["note"] = f"Emails sent to {result['emailAddress']} will be delivered to your inbox"
            result["requestedDays"] = days_valid

        return format_success(result, "Temporary alias created successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except APIError as e:
        if "limit" in str(e).lower() or "maximum" in str(e).lower():
            return format_error("Maximum number of temporary aliases reached", "LIMIT_REACHED")
        elif "not enabled" in str(e).lower() or "disabled" in str(e).lower():
            return format_error("Temporary aliases are not enabled for this account", "FEATURE_DISABLED")
        return format_error(str(e), "API_ERROR")
    except Exception as e:
        logger.error(f"Error creating temporary alias: {e}")
        return format_error(str(e), "CREATE_ERROR")


@mcp.tool()
async def delete_temporary_alias(
    email: str,
    password: str,
    server_url: str,
    alias_id: str
) -> Dict[str, Any]:
    """
    Delete a temporary email alias.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL
        alias_id: ID of the temporary alias to delete

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

        # Delete the alias
        await quick_request(
            email, password, server_url,
            "DELETE", f"account/temporaryaliases/{alias_id}"
        )

        return format_success({"id": alias_id}, "Temporary alias deleted successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error deleting temporary alias: {e}")
        return format_error(str(e), "DELETE_ERROR")


@mcp.tool()
async def cleanup_expired_aliases(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Remove all expired temporary aliases.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Summary of cleanup operations
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get all aliases
        aliases_response = await quick_request(
            email, password, server_url,
            "GET", "account/temporaryaliases"
        )

        if not aliases_response.get("items"):
            return format_success({"removed": 0}, "No temporary aliases found")

        removed = []
        errors = []
        active = []

        for alias in aliases_response["items"]:
            try:
                # Check if expired
                if "expireDate" in alias:
                    expire_dt = datetime.fromisoformat(alias["expireDate"].replace('Z', '+00:00'))
                    now = datetime.now(expire_dt.tzinfo)

                    if now > expire_dt:
                        # Expired - delete it
                        await quick_request(
                            email, password, server_url,
                            "DELETE", f"account/temporaryaliases/{alias['id']}"
                        )
                        removed.append({
                            "email": alias.get("emailAddress"),
                            "expired": alias.get("expireDate")
                        })
                    else:
                        active.append(alias.get("emailAddress"))
            except Exception as e:
                errors.append({
                    "alias": alias.get("emailAddress", alias.get("id")),
                    "error": str(e)
                })

        result = {
            "removed": removed,
            "active": active,
            "errors": errors
        }

        if removed:
            return format_success(result, f"Removed {len(removed)} expired aliases")
        else:
            return format_success(result, "No expired aliases to remove")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error cleaning up aliases: {e}")
        return format_error(str(e), "CLEANUP_ERROR")


# ============================================================================
# Permanent Aliases
# ============================================================================

@mcp.tool()
async def get_permanent_aliases(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get permanent email aliases (domain and account aliases).

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        List of permanent aliases and their types
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get permanent aliases
        aliases = await quick_request(
            email, password, server_url,
            "GET", "account/aliases"
        )

        # Categorize aliases
        if "items" in aliases:
            main_address = None
            account_aliases = []
            domain_aliases = []
            combined_aliases = []

            for alias in aliases["items"]:
                alias_type = alias.get("type", "")
                email_addr = alias.get("emailAddress", "")

                if alias_type == "mainAddress":
                    main_address = email_addr
                elif alias_type == "accountAlias":
                    account_aliases.append(email_addr)
                elif alias_type == "domainAlias":
                    domain_aliases.append(email_addr)
                elif alias_type == "accountAndDomainAlias":
                    combined_aliases.append(email_addr)

            categorized = {
                "mainAddress": main_address,
                "accountAliases": account_aliases,
                "domainAliases": domain_aliases,
                "combinedAliases": combined_aliases,
                "totalCount": len(aliases["items"])
            }

            aliases["categorized"] = categorized

        return format_success(aliases, "Permanent aliases retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting permanent aliases: {e}")
        return format_error(str(e), "ALIASES_ERROR")


# ============================================================================
# Password Management
# ============================================================================

@mcp.tool()
async def change_password(
    email: str,
    password: str,
    server_url: str,
    new_password: str,
    logout_other_sessions: bool = False
) -> Dict[str, Any]:
    """
    Change the account password.

    Args:
        email: User's email address
        password: Current password
        server_url: Axigen server URL
        new_password: New password to set
        logout_other_sessions: Whether to invalidate other active sessions

    Returns:
        Success confirmation with policy compliance info
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Basic password validation
        if len(new_password) < 8:
            return format_error("Password must be at least 8 characters long", "WEAK_PASSWORD")

        if new_password == password:
            return format_error("New password must be different from current password", "SAME_PASSWORD")

        # Attempt to change password
        result = await quick_request(
            email, password, server_url,
            "POST", "account/password/change",
            data={
                "oldPassword": password,
                "newPassword": new_password,
                "logoutOtherSessions": logout_other_sessions
            }
        )

        message = "Password changed successfully"
        if logout_other_sessions:
            message += " (other sessions have been logged out)"

        return format_success({"changed": True}, message)

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except APIError as e:
        error_msg = str(e).lower()
        if "policy" in error_msg or "requirement" in error_msg:
            return format_error("Password does not meet policy requirements", "POLICY_VIOLATION")
        elif "history" in error_msg:
            return format_error("Password was recently used", "PASSWORD_HISTORY")
        elif "weak" in error_msg or "simple" in error_msg:
            return format_error("Password is too weak", "WEAK_PASSWORD")
        return format_error(str(e), "PASSWORD_ERROR")
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        return format_error(str(e), "CHANGE_ERROR")


@mcp.tool()
async def get_password_policy(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get the password policy requirements for the account.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Password policy details including:
        - Minimum/maximum length
        - Character requirements
        - History restrictions
        - Expiration settings
    """
    try:
        # Validate inputs
        valid, error = validate_email_address(email)
        if not valid:
            return format_error(error, "INVALID_EMAIL")

        valid, error = validate_server_url(server_url)
        if not valid:
            return format_error(error, "INVALID_URL")

        # Get account info which includes password policy
        info = await quick_request(
            email, password, server_url,
            "GET", "account/info"
        )

        policy = {}

        # Extract password policy from restrictions
        if "restrictions" in info and "passwordPolicy" in info["restrictions"]:
            pwd_policy = info["restrictions"]["passwordPolicy"]

            # Must change password flag
            if "mustChangePassword" in pwd_policy:
                policy["mustChangePassword"] = pwd_policy["mustChangePassword"]

            # Content policy
            if "contentPolicy" in pwd_policy:
                content = pwd_policy["contentPolicy"]
                policy["requirements"] = {
                    "enabled": content.get("enabled", False),
                    "minLength": content.get("minLength"),
                    "maxLength": content.get("maxLength"),
                    "mustInclude": content.get("mustInclude")
                }

                # Translate mustInclude values
                must_include = content.get("mustInclude", "")
                if must_include == "letters":
                    policy["requirements"]["description"] = "Must contain letters"
                elif must_include == "lettersAndNumbers":
                    policy["requirements"]["description"] = "Must contain letters and numbers"
                elif must_include == "lettersAndNumbersAndSpecial":
                    policy["requirements"]["description"] = "Must contain letters, numbers, and special characters"

            # History policy
            if "history" in pwd_policy:
                history = pwd_policy["history"]
                policy["history"] = {
                    "enabled": history.get("enabled", False),
                    "size": history.get("size", 0),
                    "description": f"Cannot reuse last {history.get('size', 0)} passwords" if history.get("enabled") else "No history restrictions"
                }

            # Change permissions
            if "allowChangeByUser" in pwd_policy:
                policy["allowUserChange"] = pwd_policy["allowChangeByUser"]

            # Renewal interval
            if "renewalInterval" in pwd_policy:
                renewal = pwd_policy["renewalInterval"]
                if renewal.get("enabled"):
                    policy["renewalInterval"] = {
                        "enabled": True,
                        "days": renewal.get("interval"),
                        "description": f"Must wait {renewal.get('interval')} days between password changes"
                    }

            # Expiration policy
            if "expiration" in pwd_policy:
                exp = pwd_policy["expiration"]
                policy["expiration"] = {
                    "enabled": exp.get("enabled", False),
                    "date": exp.get("date"),
                    "warningDays": exp.get("warningInterval"),
                    "inWarningPeriod": exp.get("inWarningInterval", False)
                }

                if exp.get("enabled") and exp.get("date"):
                    try:
                        expire_dt = datetime.fromisoformat(exp["date"].replace('Z', '+00:00'))
                        now = datetime.now(expire_dt.tzinfo)
                        remaining = expire_dt - now
                        policy["expiration"]["daysRemaining"] = remaining.days
                    except:
                        pass

        if not policy:
            policy = {
                "note": "No specific password policy found - using system defaults",
                "defaultRequirements": "Minimum 8 characters recommended"
            }

        return format_success(policy, "Password policy retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting password policy: {e}")
        return format_error(str(e), "POLICY_ERROR")


# ============================================================================
# Quota and Limits Information
# ============================================================================

@mcp.tool()
async def get_account_limits(
    email: str,
    password: str,
    server_url: str
) -> Dict[str, Any]:
    """
    Get account quotas and usage limits.

    Args:
        email: User's email address
        password: User's password
        server_url: Axigen server URL

    Returns:
        Account limits including:
        - Storage quota (used/total)
        - Message count limits
        - Percentage usage
        - Warning thresholds
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

        limits = {
            "storage": {},
            "messages": {},
            "features": {}
        }

        # Extract quota information
        if "totalQuota" in info and "usedQuota" in info:
            total_kb = info.get("totalQuota", 0)
            used_kb = info.get("usedQuota", 0)
            remaining_kb = info.get("remainingQuota", 0)

            # Convert to more readable units
            limits["storage"] = {
                "totalKB": total_kb,
                "usedKB": used_kb,
                "remainingKB": remaining_kb,
                "totalMB": round(total_kb / 1024, 2),
                "usedMB": round(used_kb / 1024, 2),
                "remainingMB": round(remaining_kb / 1024, 2),
                "percentUsed": round((used_kb / total_kb * 100), 2) if total_kb > 0 else 0,
                "overQuotaThreshold": info.get("overQuotaThreshold", 90)
            }

            # Check if approaching limit
            if limits["storage"]["percentUsed"] >= info.get("overQuotaThreshold", 90):
                limits["storage"]["warning"] = "Approaching storage quota limit"

        # Extract message count limits
        if "totalMessageCount" in info and "usedMessageCount" in info:
            total_msgs = info.get("totalMessageCount", 0)
            used_msgs = info.get("usedMessageCount", 0)
            remaining_msgs = info.get("remainingMessageCount", 0)

            limits["messages"] = {
                "total": total_msgs,
                "used": used_msgs,
                "remaining": remaining_msgs,
                "percentUsed": round((used_msgs / total_msgs * 100), 2) if total_msgs > 0 else 0
            }

        # Extract feature limits from restrictions
        if "restrictions" in info:
            restrictions = info["restrictions"]

            # Temporary aliases limit
            if "temporaryAliases" in restrictions:
                temp_aliases = restrictions["temporaryAliases"]
                limits["features"]["temporaryAliases"] = {
                    "enabled": temp_aliases.get("enabled", False),
                    "maxCount": temp_aliases.get("maxNumberOfAliases", 0)
                }

            # Conversation view
            if "allowConversationView" in info:
                limits["features"]["conversationView"] = info["allowConversationView"]

        return format_success(limits, "Account limits retrieved successfully")

    except AuthenticationError as e:
        return format_error(str(e), "AUTH_FAILED")
    except Exception as e:
        logger.error(f"Error getting account limits: {e}")
        return format_error(str(e), "LIMITS_ERROR")


# ============================================================================
# Run the server (for local testing)
# ============================================================================

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run())