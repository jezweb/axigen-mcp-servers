#!/usr/bin/env python3
"""
MCP server for Axigen Email operations.
Provides tools for email management through the Axigen REST API.
"""

from fastmcp import FastMCP
from typing import Dict, Any, Optional, List
from src.utils import quick_request, format_email_list, parse_email_addresses
import json
import base64

mcp = FastMCP("Axigen Email Server")

# Helper functions

async def find_label_by_name(email: str, password: str, server_url: str, label_name: str) -> Optional[str]:
    """Find a label ID by name, with option to create if not found."""
    try:
        result = await quick_request(email, password, server_url, "GET", "labels")

        if result.get("items"):
            for label in result["items"]:
                if label.get("name") == label_name:
                    return label.get("id")
        return None
    except Exception:
        return None

async def validate_label_exists(email: str, password: str, server_url: str, label_id: str) -> bool:
    """Check if a label ID exists."""
    try:
        result = await quick_request(email, password, server_url, "GET", f"labels/{label_id}")
        return result.get("id") == label_id
    except Exception:
        return False

async def validate_mail_id(email: str, password: str, server_url: str, mail_id: str) -> Dict[str, Any]:
    """Validate a mail ID exists and return validation info."""
    try:
        # Try to get basic email info first
        result = await quick_request(email, password, server_url, "GET", f"mails/{mail_id}")
        if result.get("id") == mail_id:
            return {
                "valid": True,
                "mail_id": mail_id,
                "subject": result.get("subject", "Unknown"),
                "from": result.get("from", "Unknown")
            }
    except Exception as e:
        return {
            "valid": False,
            "mail_id": mail_id,
            "error": str(e),
            "suggestion": "Verify mail_id exists by using list_emails or search_emails first"
        }
    return {"valid": False, "mail_id": mail_id}

async def validate_folder_id(email: str, password: str, server_url: str, folder_id: str) -> Dict[str, Any]:
    """Validate a folder ID exists and return folder info."""
    try:
        # Get all folders to check if this ID exists
        result = await quick_request(email, password, server_url, "GET", "folders")
        if result.get("items"):
            for folder in result["items"]:
                if folder.get("id") == folder_id:
                    return {
                        "valid": True,
                        "folder_id": folder_id,
                        "name": folder.get("name", "Unknown"),
                        "unread_count": folder.get("unreadCount", 0)
                    }
        return {
            "valid": False,
            "folder_id": folder_id,
            "error": "Folder ID not found",
            "suggestion": "Use get_common_folder_ids or list_folders to get valid folder IDs"
        }
    except Exception as e:
        return {
            "valid": False,
            "folder_id": folder_id,
            "error": str(e),
            "suggestion": "Use get_common_folder_ids to discover available folders"
        }

async def auto_discover_folder_id(email: str, password: str, server_url: str, folder_name: str) -> Optional[str]:
    """Auto-discover folder ID by name (case-insensitive)."""
    try:
        result = await quick_request(email, password, server_url, "GET", "folders")
        if result.get("items"):
            folder_name_lower = folder_name.lower()
            for folder in result["items"]:
                if folder.get("name", "").lower() == folder_name_lower:
                    return folder.get("id")
        return None
    except Exception:
        return None

async def get_reliable_common_folders(email: str, password: str, server_url: str) -> Dict[str, Any]:
    """Get fresh common folder IDs with validation."""
    try:
        # Get all folders first
        folders_result = await quick_request(email, password, server_url, "GET", "folders")

        if not folders_result.get("items"):
            return {
                "success": False,
                "error": "No folders found",
                "suggestion": "Check account permissions or server configuration"
            }

        folders = {}
        folder_mapping = {
            "inbox": ["inbox", "inboxx"],  # Handle variations
            "sent": ["sent", "sent items", "sent mail"],
            "drafts": ["drafts", "draft"],
            "trash": ["trash", "deleted", "deleted items"],
            "spam": ["spam", "junk", "junk mail"],
            "archive": ["archive", "archives"]
        }

        # Map known folder types
        for folder in folders_result["items"]:
            folder_name = folder.get("name", "").lower()
            folder_id = folder.get("id")

            for standard_name, variations in folder_mapping.items():
                if folder_name in variations:
                    folders[standard_name] = folder_id
                    break

        return {
            "success": True,
            "folders": folders,
            "total_folders": len(folders_result["items"]),
            "discovered": len(folders)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Check authentication credentials and server connectivity"
        }

async def get_drafts_folder_info(email: str, password: str, server_url: str) -> Dict[str, Any]:
    """Get drafts folder ID and current draft count."""
    try:
        folders_result = await get_reliable_common_folders(email, password, server_url)
        if not folders_result["success"] or "drafts" not in folders_result["folders"]:
            return {
                "success": False,
                "error": "Drafts folder not found",
                "suggestion": "Check account configuration or folder access"
            }

        drafts_folder_id = folders_result["folders"]["drafts"]

        # Get draft count
        drafts_result = await quick_request(
            email, password, server_url,
            "GET", "mails",
            params={"folderId": drafts_folder_id, "limit": 1}
        )

        draft_count = 0
        if drafts_result.get("success"):
            draft_count = drafts_result.get("data", {}).get("total", 0)

        return {
            "success": True,
            "drafts_folder_id": drafts_folder_id,
            "draft_count": draft_count,
            "folder_info": folders_result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Use get_common_folder_ids to verify folder access"
        }

async def list_current_drafts(email: str, password: str, server_url: str, limit: int = 20) -> Dict[str, Any]:
    """List current drafts with enhanced metadata."""
    drafts_info = await get_drafts_folder_info(email, password, server_url)
    if not drafts_info["success"]:
        return drafts_info

    try:
        result = await quick_request(
            email, password, server_url,
            "GET", "mails",
            params={"folderId": drafts_info["drafts_folder_id"], "limit": limit}
        )

        if result.get("success"):
            drafts = result.get("data", {}).get("items", [])
            enhanced_drafts = []

            for draft in drafts:
                enhanced_draft = {
                    "draft_id": draft.get("id"),
                    "subject": draft.get("subject", "No Subject"),
                    "to": draft.get("to", []),
                    "created": draft.get("date"),
                    "size": draft.get("size", 0),
                    "has_attachments": draft.get("hasAttachments", False),
                    "is_flagged": draft.get("isFlagged", False),
                    "lifecycle": {
                        "is_draft": True,
                        "is_sent": False,
                        "status": "draft"
                    }
                }
                enhanced_drafts.append(enhanced_draft)

            return {
                "success": True,
                "drafts": enhanced_drafts,
                "total_drafts": result.get("data", {}).get("total", len(drafts)),
                "drafts_folder_id": drafts_info["drafts_folder_id"]
            }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Check drafts folder access and account permissions"
        }

# Standardized error response helper

def create_error_response(operation: str, error: str, suggestion: str = None, details: Dict = None) -> Dict[str, Any]:
    """Create standardized error response with actionable guidance."""
    response = {
        "success": False,
        "operation": operation,
        "error": error
    }

    if suggestion:
        response["suggestion"] = suggestion
    if details:
        response["details"] = details

    return response

# Draft response helper with lifecycle tracking

async def create_draft_response(
    operation: str,
    success: bool,
    api_result: Dict[str, Any],
    email: str,
    password: str,
    server_url: str,
    draft_id: str = None,
    additional_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create standardized draft response with lifecycle tracking.

    Args:
        operation: Operation performed (create_draft, send_draft, etc.)
        success: Whether operation succeeded
        api_result: Raw API response
        email: User email for additional queries
        password: User password
        server_url: Server URL
        draft_id: Draft ID if known
        additional_data: Additional data to include

    Returns:
        Standardized draft response with lifecycle info
    """
    import time

    response = {
        "success": success,
        "operation": operation,
        "timestamp": int(time.time())
    }

    if success:
        # Extract IDs from API result
        data = api_result.get("data", {})

        # Standardize ID fields
        response["draft_id"] = draft_id or data.get("id") or data.get("mailId")
        if data.get("mailId"):
            response["mail_id"] = data["mailId"]
        if data.get("processingId"):
            response["processing_id"] = data["processingId"]

        # Add lifecycle tracking
        response["lifecycle"] = {
            "is_draft": operation in ["create_draft", "update_draft"],
            "is_sent": operation in ["send_draft", "send_email"],
            "status": "draft" if operation in ["create_draft", "update_draft"] else "sent",
            "last_action": operation
        }

        # Include original API data
        response["api_data"] = data

        # Add any additional data
        if additional_data:
            response.update(additional_data)

        # Set appropriate message
        messages = {
            "create_draft": f"Draft created successfully (ID: {response.get('draft_id', 'unknown')})",
            "update_draft": f"Draft updated successfully (ID: {response.get('draft_id', 'unknown')})",
            "send_draft": f"Draft sent successfully (Mail ID: {response.get('mail_id', 'unknown')})",
            "send_email": f"Email sent successfully (Mail ID: {response.get('mail_id', 'unknown')})"
        }
        response["message"] = messages.get(operation, f"{operation} completed successfully")

    else:
        # Handle error case
        response["error"] = api_result.get("error", "Operation failed")
        response["api_data"] = api_result

        # Add operation-specific suggestions
        suggestions = {
            "create_draft": "Check recipient addresses and required fields",
            "update_draft": "Verify draft_id exists using list_emails in Drafts folder",
            "send_draft": "Ensure draft_id is valid and draft hasn't been sent already",
            "send_email": "Verify recipient addresses and email content"
        }
        response["suggestion"] = suggestions.get(operation, "Check operation parameters")

    return response

# Email Listing and Search Tools

@mcp.tool()
async def list_emails(
    email: str,
    password: str,
    folder_id: str,
    start: Optional[int] = 0,
    limit: Optional[int] = 50,
    sort: Optional[str] = "date",
    sort_dir: Optional[str] = "DESC",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    List emails from a specific folder.

    Args:
        email: User email for authentication
        password: User password
        folder_id: Folder ID to list from (required - use list_folders to get IDs)
        start: Starting position for pagination (default: 0)
        limit: Number of emails to return (default: 50, max: 500)
        sort: Sort field - "date", "from", "subject", "size" (default: "date")
        sort_dir: Sort direction - "ASC" or "DESC" (default: "DESC")
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        List of emails with metadata
    """
    params = {
        "folderId": folder_id,
        "start": start,
        "limit": min(limit, 500),
        "sort": sort,
        "dir": sort_dir
    }

    result = await quick_request(
        email, password, server_url,
        "GET", "mails",
        params=params
    )

    if result.get("success") and result.get("data"):
        data = result["data"]
        emails = data.get("items", [])
        formatted = format_email_list(emails)
        return {
            "success": True,
            "total": data.get("total", len(emails)),
            "emails": emails,
            "formatted": formatted
        }

    return result

@mcp.tool()
async def search_emails(
    email: str,
    password: str,
    folder_ids: List[str],
    search_criteria: List[Dict[str, Any]],
    recursive: bool = False,
    limit: int = 50,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Search emails using Axigen's search syntax.

    Args:
        email: User email for authentication
        password: User password
        folder_ids: List of folder IDs to search in (use get_common_folder_ids to find these)
        search_criteria: List of search criteria objects. Each object should have:
            - field: The field to search
            - value: The value to search for
            - negate: Optional boolean to negate the criteria (default: false)
        recursive: Whether to search recursively in subfolders (default: False)
        limit: Maximum number of results (default: 50)
        server_url: Axigen server URL (default: https://ax.email)

    Available search fields:
        Text fields: "from", "to", "subject", "body"
        Boolean fields: "unread" (not "isUnread")
        Note: "flagged" and "attachment" fields are not supported on ax.email

    Examples:
        Search for unread emails from a specific sender:
        search_criteria = [
            {"field": "from", "value": "john@example.com"},
            {"field": "unread", "value": "true"}
        ]

        Search for emails with subject containing "test":
        search_criteria = [
            {"field": "subject", "value": "test"}
        ]

    Returns:
        Search results with email list
    """
    search_data = {
        "folderIds": folder_ids,
        "query": search_criteria,
        "recursive": recursive
    }

    # Add pagination
    search_data["limit"] = limit

    result = await quick_request(
        email, password, server_url,
        "POST", "mails/search",
        data=search_data
    )

    if result.get("folderId"):
        # Search returns a temporary folder ID with results
        # Now we need to list the mails in that temporary folder
        temp_folder_id = result["folderId"]
        total_items = result.get("totalItems", 0)

        # Get the actual emails from the temporary search folder
        mails_result = await quick_request(
            email, password, server_url,
            "GET", "mails",
            params={"folderId": temp_folder_id, "limit": limit}
        )

        return {
            "success": True,
            "message": f"Found {total_items} matching emails",
            "search_folder_id": temp_folder_id,
            "total_matches": total_items,
            "emails": mails_result.get("items", [])
        }

    return result

# Bulk Operations for Efficiency


# Bulk Draft and Template Operations


@mcp.tool()
async def get_email(
    email: str,
    password: str,
    mail_id: str,
    include_body: bool = True,
    validate_id: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get detailed information about a specific email with validation.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to retrieve
        include_body: Whether to include email body (default: True)
        validate_id: Pre-validate mail_id exists (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Full email details including headers and body with validation info
    """
    # Pre-validate mail ID if requested
    if validate_id:
        validation = await validate_mail_id(email, password, server_url, mail_id)
        if not validation["valid"]:
            return create_error_response(
                "get_email",
                f"Invalid mail_id: {validation['error']}",
                validation.get("suggestion", "Verify mail_id using list_emails or search_emails"),
                {"mail_id": mail_id, "validation": validation}
            )

    try:
        result = await quick_request(
            email, password, server_url,
            "GET", f"mails/{mail_id}"
        )

        if result.get("success") and include_body:
            try:
                body_result = await quick_request(
                    email, password, server_url,
                    "GET", f"mails/{mail_id}/body"
                )
                if body_result.get("success"):
                    result["data"]["body"] = body_result["data"]
                    result["data"]["body_included"] = True
                else:
                    result["data"]["body_included"] = False
                    result["data"]["body_error"] = "Body could not be retrieved"
            except Exception as e:
                result["data"]["body_included"] = False
                result["data"]["body_error"] = f"Body retrieval failed: {str(e)}"

        # Add metadata for reliability
        if result.get("success"):
            result["metadata"] = {
                "mail_id": mail_id,
                "retrieved_at": "now",
                "body_included": result.get("data", {}).get("body_included", False),
                "validated": validate_id
            }

        return result
    except Exception as e:
        if "404" in str(e):
            return create_error_response(
                "get_email",
                "Email not found",
                "Verify mail_id exists using list_emails or search_emails",
                {"mail_id": mail_id, "error": str(e)}
            )
        raise

@mcp.tool()
async def get_email_body(
    email: str,
    password: str,
    mail_id: str,
    format: str = "both",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get the body content of an email.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        format: Body format - "text", "html", or "both" (default: "both")
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Email body content in requested format (decoded from base64)
    """
    params = {}
    if format != "both":
        params["format"] = format

    result = await quick_request(
        email, password, server_url,
        "GET", f"mails/{mail_id}/body",
        params=params
    )

    # Decode base64 encoded body if present
    if isinstance(result, dict) and result.get("data"):
        try:
            decoded_body = base64.b64decode(result["data"]).decode('utf-8')
            result["bodyText"] = decoded_body
            result["decoded"] = True
            # Keep original base64 data too
            result["dataBase64"] = result["data"]
            del result["data"]  # Remove to avoid confusion
        except Exception as e:
            result["decodeError"] = str(e)

    return result

# Email Composition and Sending Tools

@mcp.tool()
async def create_draft(
    email: str,
    password: str,
    to: str,
    subject: str,
    body_text: Optional[str] = None,
    body_html: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
    importance: Optional[str] = "normal",
    validate_recipients: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Create a new draft email with enhanced tracking and validation.

    Args:
        email: User email for authentication
        password: User password
        to: Recipient email address(es), comma-separated
        subject: Email subject
        body_text: Plain text body (optional)
        body_html: HTML body (optional)
        cc: CC recipients, comma-separated (optional)
        bcc: BCC recipients, comma-separated (optional)
        reply_to: Reply-To address (optional)
        importance: Email importance - "low", "normal", "high" (default: "normal")
        validate_recipients: Pre-validate recipient email formats (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Standardized draft response with lifecycle tracking
    """
    # Validate recipients if requested
    if validate_recipients:
        recipients = [addr.strip() for addr in to.split(",")]
        if cc:
            recipients.extend([addr.strip() for addr in cc.split(",")])
        if bcc:
            recipients.extend([addr.strip() for addr in bcc.split(",")])

        invalid_recipients = []
        for recipient in recipients:
            if "@" not in recipient or "." not in recipient.split("@")[-1]:
                invalid_recipients.append(recipient)

        if invalid_recipients:
            return await create_draft_response(
                "create_draft",
                False,
                {
                    "error": f"Invalid recipient format(s): {', '.join(invalid_recipients)}",
                    "invalid_recipients": invalid_recipients
                },
                email, password, server_url
            )

    # Validate content
    if not body_text and not body_html:
        return await create_draft_response(
            "create_draft",
            False,
            {"error": "Either body_text or body_html must be provided"},
            email, password, server_url
        )

    draft_data = {
        "to": to,
        "subject": subject,
        "importance": importance
    }

    if body_text:
        draft_data["bodyText"] = body_text
    if body_html:
        draft_data["bodyHtml"] = body_html
    if cc:
        draft_data["cc"] = cc
    if bcc:
        draft_data["bcc"] = bcc
    if reply_to:
        draft_data["replyTo"] = reply_to

    try:
        result = await quick_request(
            email, password, server_url,
            "POST", "mails",
            data=draft_data
        )

        return await create_draft_response(
            "create_draft",
            result.get("success", False),
            result,
            email, password, server_url,
            additional_data={
                "input_parameters": {
                    "to": to,
                    "subject": subject,
                    "has_text_body": bool(body_text),
                    "has_html_body": bool(body_html),
                    "importance": importance
                },
                "recipients_validated": validate_recipients
            }
        )

    except Exception as e:
        return await create_draft_response(
            "create_draft",
            False,
            {"error": str(e)},
            email, password, server_url
        )

@mcp.tool()
async def send_email(
    email: str,
    password: str,
    to: str,
    subject: str,
    body_text: Optional[str] = None,
    body_html: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
    importance: Optional[str] = "normal",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Send a new email directly.

    Args:
        email: User email for authentication
        password: User password
        to: Recipient email address(es), comma-separated
        subject: Email subject
        body_text: Plain text body (optional)
        body_html: HTML body (optional)
        cc: CC recipients, comma-separated (optional)
        bcc: BCC recipients, comma-separated (optional)
        reply_to: Reply-To address (optional)
        importance: Email importance - "low", "normal", "high" (default: "normal")
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Send status and message ID
    """
    email_data = {
        "to": to,
        "subject": subject,
        "importance": importance
    }

    if body_text:
        email_data["bodyText"] = body_text
    if body_html:
        email_data["bodyHtml"] = body_html
    if cc:
        email_data["cc"] = cc
    if bcc:
        email_data["bcc"] = bcc
    if reply_to:
        email_data["replyTo"] = reply_to

    result = await quick_request(
        email, password, server_url,
        "POST", "mails/send",
        data=email_data
    )

    if result.get("success"):
        return {
            "success": True,
            "message": f"Email sent successfully to {to}",
            "data": result["data"]
        }

    return result

@mcp.tool()
async def send_draft(
    email: str,
    password: str,
    draft_id: str,
    validate_draft: bool = True,
    idempotent: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Send an existing draft email with validation and idempotent behavior.

    Args:
        email: User email for authentication
        password: User password
        draft_id: The draft email ID to send
        validate_draft: Pre-validate draft exists and is sendable (default: True)
        idempotent: Return success if draft already sent (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Standardized send response with lifecycle tracking
    """
    # Pre-validate draft if requested
    if validate_draft:
        draft_validation = await validate_mail_id(email, password, server_url, draft_id)
        if not draft_validation["valid"]:
            return await create_draft_response(
                "send_draft",
                False,
                {
                    "error": f"Draft not found: {draft_validation['error']}",
                    "validation": draft_validation
                },
                email, password, server_url,
                draft_id=draft_id
            )

        # Check if it's actually a draft (in Drafts folder)
        try:
            # Get common folders to find Drafts folder ID
            folders_result = await get_reliable_common_folders(email, password, server_url)
            if folders_result["success"] and "drafts" in folders_result["folders"]:
                drafts_folder_id = folders_result["folders"]["drafts"]

                # List emails in Drafts to see if this draft is there
                drafts_result = await quick_request(
                    email, password, server_url,
                    "GET", "mails",
                    params={"folderId": drafts_folder_id, "limit": 100}
                )

                if drafts_result.get("success"):
                    draft_ids = [item.get("id") for item in drafts_result.get("data", {}).get("items", [])]
                    if draft_id not in draft_ids and idempotent:
                        # Draft not in Drafts folder - might already be sent
                        return await create_draft_response(
                            "send_draft",
                            True,
                            {
                                "data": {"id": draft_id},
                                "already_sent": True
                            },
                            email, password, server_url,
                            draft_id=draft_id,
                            additional_data={
                                "message": "Draft appears to already be sent (idempotent operation)",
                                "idempotent_result": True
                            }
                        )
        except Exception:
            # Validation failed, but continue with send attempt
            pass

    try:
        result = await quick_request(
            email, password, server_url,
            "POST", f"drafts/{draft_id}/send"
        )

        return await create_draft_response(
            "send_draft",
            result.get("success", False),
            result,
            email, password, server_url,
            draft_id=draft_id,
            additional_data={
                "validated": validate_draft,
                "idempotent_mode": idempotent
            }
        )

    except Exception as e:
        if idempotent and ("not found" in str(e).lower() or "404" in str(e)):
            # Might already be sent
            return await create_draft_response(
                "send_draft",
                True,
                {
                    "data": {"id": draft_id},
                    "already_sent": True
                },
                email, password, server_url,
                draft_id=draft_id,
                additional_data={
                    "message": "Draft not found - likely already sent (idempotent operation)",
                    "idempotent_result": True
                }
            )

        return await create_draft_response(
            "send_draft",
            False,
            {"error": str(e)},
            email, password, server_url,
            draft_id=draft_id
        )

@mcp.tool()
async def update_draft(
    email: str,
    password: str,
    draft_id: str,
    to: str,
    subject: str,
    body_text: Optional[str] = None,
    body_html: Optional[str] = None,
    from_address: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
    importance: str = "normal",
    is_unread: bool = True,
    is_flagged: bool = False,
    validate_draft: bool = True,
    validate_recipients: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Replace an existing draft email with validation and enhanced tracking.

    Args:
        email: User email for authentication
        password: User password
        draft_id: The draft email ID to replace
        to: Recipients (required)
        subject: Email subject (required)
        body_text: Plain text body (optional)
        body_html: HTML body (optional)
        from_address: From address (optional, defaults to account email)
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        reply_to: Reply-To address (optional)
        importance: "low", "normal", or "high" (default: "normal")
        is_unread: Unread status (default: True)
        is_flagged: Flagged status (default: False)
        validate_draft: Pre-validate draft exists (default: True)
        validate_recipients: Validate recipient email formats (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Standardized update response with lifecycle tracking
    """
    # Validate draft exists if requested
    if validate_draft:
        draft_validation = await validate_mail_id(email, password, server_url, draft_id)
        if not draft_validation["valid"]:
            return await create_draft_response(
                "update_draft",
                False,
                {
                    "error": f"Draft not found: {draft_validation['error']}",
                    "validation": draft_validation
                },
                email, password, server_url,
                draft_id=draft_id
            )

    # Validate recipients if requested
    if validate_recipients:
        recipients = [addr.strip() for addr in to.split(",")]
        if cc:
            recipients.extend([addr.strip() for addr in cc.split(",")])
        if bcc:
            recipients.extend([addr.strip() for addr in bcc.split(",")])

        invalid_recipients = []
        for recipient in recipients:
            if "@" not in recipient or "." not in recipient.split("@")[-1]:
                invalid_recipients.append(recipient)

        if invalid_recipients:
            return await create_draft_response(
                "update_draft",
                False,
                {
                    "error": f"Invalid recipient format(s): {', '.join(invalid_recipients)}",
                    "invalid_recipients": invalid_recipients
                },
                email, password, server_url,
                draft_id=draft_id
            )

    # Validate content
    if not body_text and not body_html:
        return await create_draft_response(
            "update_draft",
            False,
            {"error": "Either body_text or body_html must be provided"},
            email, password, server_url,
            draft_id=draft_id
        )

    # Build the complete draft replacement data
    draft_data = {
        "to": to,
        "subject": subject,
        "importance": importance,
        "isUnread": is_unread,
        "isFlagged": is_flagged
    }

    if from_address:
        draft_data["from"] = from_address
    if cc:
        draft_data["cc"] = cc
    if bcc:
        draft_data["bcc"] = bcc
    if reply_to:
        draft_data["replyTo"] = reply_to
    if body_text:
        draft_data["bodyText"] = body_text
    if body_html:
        draft_data["bodyHtml"] = body_html

    try:
        result = await quick_request(
            email, password, server_url,
            "PUT", f"drafts/{draft_id}",
            data=draft_data
        )

        # Handle the response format difference
        success = result.get("id") is not None or result.get("success", False)
        if success and not result.get("success"):
            # Transform direct ID response to standard format
            result = {
                "success": True,
                "data": result
            }

        return await create_draft_response(
            "update_draft",
            success,
            result,
            email, password, server_url,
            draft_id=draft_id,
            additional_data={
                "input_parameters": {
                    "to": to,
                    "subject": subject,
                    "has_text_body": bool(body_text),
                    "has_html_body": bool(body_html),
                    "importance": importance
                },
                "validated": validate_draft,
                "recipients_validated": validate_recipients
            }
        )

    except Exception as e:
        return await create_draft_response(
            "update_draft",
            False,
            {"error": str(e)},
            email, password, server_url,
            draft_id=draft_id
        )

# Scheduled Send Operations

async def schedule_send_email(
    email: str,
    password: str,
    to: str,
    subject: str,
    delivery_time: int,
    body_text: Optional[str] = None,
    body_html: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
    importance: Optional[str] = "normal",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Schedule an email to be sent at a specific time.

    Args:
        email: User email for authentication
        password: User password
        to: Recipient email address(es), comma-separated
        subject: Email subject
        delivery_time: When to send the email (unix timestamp in seconds)
        body_text: Plain text body (optional)
        body_html: HTML body (optional)
        cc: CC recipients, comma-separated (optional)
        bcc: BCC recipients, comma-separated (optional)
        reply_to: Reply-To address (optional)
        importance: Email importance - "low", "normal", "high" (default: "normal")
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Scheduled send details including mail ID
    """
    email_data = {
        "to": to,
        "subject": subject,
        "deliveryTime": delivery_time,
        "importance": importance
    }

    if body_text:
        email_data["bodyText"] = body_text
    if body_html:
        email_data["bodyHtml"] = body_html
    if cc:
        email_data["cc"] = cc
    if bcc:
        email_data["bcc"] = bcc
    if reply_to:
        email_data["replyTo"] = reply_to

    result = await quick_request(
        email, password, server_url,
        "POST", "mails/send/schedule",
        data=email_data
    )

    if result.get("mailId"):
        return {
            "success": True,
            "message": f"Email scheduled for delivery",
            "mail_id": result["mailId"],
            "data": result
        }

    return result

@mcp.tool()
async def schedule_send_draft(
    email: str,
    password: str,
    draft_id: str,
    delivery_time: int,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Schedule an existing draft to be sent at a specific time.

    Args:
        email: User email for authentication
        password: User password
        draft_id: The draft email ID to schedule
        delivery_time: When to send the draft (unix timestamp in seconds)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Scheduled send details
    """
    schedule_data = {
        "deliveryTime": delivery_time
    }

    result = await quick_request(
        email, password, server_url,
        "POST", f"drafts/{draft_id}/send/schedule",
        data=schedule_data
    )

    if result.get("mailId"):
        return {
            "success": True,
            "message": f"Draft scheduled for delivery",
            "mail_id": result["mailId"],
            "data": result
        }

    return result

@mcp.tool()
async def cancel_scheduled_send(
    email: str,
    password: str,
    mail_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Cancel a scheduled email send.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The scheduled email ID to cancel
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Cancellation status with draft mail ID
    """
    result = await quick_request(
        email, password, server_url,
        "DELETE", f"mails/send/schedule/{mail_id}"
    )

    if result.get("mailId"):
        return {
            "success": True,
            "message": "Scheduled send cancelled successfully",
            "draft_id": result["mailId"],
            "data": result
        }

    return result

# Note: undo_send is not available on ax.email (404 errors)
# This may work on full Axigen installations with advanced features enabled

# Email Management Tools

@mcp.tool()
async def delete_email(
    email: str,
    password: str,
    mail_id: str,
    permanent: bool = False,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Delete an email (move to trash or permanently delete).

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to delete
        permanent: If True, permanently delete; if False, move to trash (default: False)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Deletion status
    """
    params = {}
    if permanent:
        params["permanent"] = "true"

    result = await quick_request(
        email, password, server_url,
        "DELETE", f"mails/{mail_id}",
        params=params
    )

    if result.get("success"):
        action = "permanently deleted" if permanent else "moved to trash"
        return {
            "success": True,
            "message": f"Email {action} successfully"
        }

    return result

@mcp.tool()
async def move_email(
    email: str,
    password: str,
    mail_id: str,
    folder_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Move an email to a different folder.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to move
        folder_id: The target folder ID
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Move operation status
    """
    move_data = {
        "destinationFolderId": folder_id
    }

    result = await quick_request(
        email, password, server_url,
        "POST", f"mails/{mail_id}/move",
        data=move_data
    )

    if result.get("success"):
        return {
            "success": True,
            "message": f"Email moved to folder {folder_id} successfully"
        }

    return result

@mcp.tool()
async def copy_email(
    email: str,
    password: str,
    mail_id: str,
    folder_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Copy an email to another folder.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to copy
        folder_id: The target folder ID
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Copy operation status with new email details
    """
    copy_data = {
        "destinationFolderId": folder_id
    }

    result = await quick_request(
        email, password, server_url,
        "POST", f"mails/{mail_id}/copy",
        data=copy_data
    )

    return result

@mcp.tool()
async def update_email_flags(
    email: str,
    password: str,
    mail_id: str,
    is_unread: Optional[bool] = None,
    is_flagged: Optional[bool] = None,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Update email flags (read/unread, flagged/unflagged).

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to update
        is_unread: Set read/unread status (optional)
        is_flagged: Set flagged status (optional)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Update status
    """
    update_data = {}

    if is_unread is not None:
        update_data["isUnread"] = is_unread
    if is_flagged is not None:
        update_data["isFlagged"] = is_flagged

    if not update_data:
        return {
            "success": False,
            "error": "No flags to update"
        }

    result = await quick_request(
        email, password, server_url,
        "PATCH", f"mails/{mail_id}",
        data=update_data
    )

    if result.get("success"):
        status_parts = []
        if is_unread is not None:
            status_parts.append(f"marked as {'unread' if is_unread else 'read'}")
        if is_flagged is not None:
            status_parts.append(f"{'flagged' if is_flagged else 'unflagged'}")

        return {
            "success": True,
            "message": f"Email {' and '.join(status_parts)} successfully"
        }

    return result

@mcp.tool()
async def mark_as_spam(
    email: str,
    password: str,
    mail_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Mark an email as spam.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to mark as spam
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Operation status
    """
    result = await quick_request(
        email, password, server_url,
        "POST", f"mails/{mail_id}/spam"
    )

    if result.get("success"):
        return {
            "success": True,
            "message": "Email marked as spam successfully"
        }

    return result

# Note: mark_as_not_spam is not supported on ax.email
# The /notspam endpoint returns 400 Bad Parameter error
# Keeping function commented in case it works on other Axigen servers
# @mcp.tool()
# async def mark_as_not_spam(...)

# Label Management Tools

async def list_labels(
    email: str,
    password: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    List all available labels.

    Args:
        email: User email for authentication
        password: User password
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        List of all labels with their IDs and names
    """
    result = await quick_request(
        email, password, server_url,
        "GET", "labels"
    )

    if result.get("items"):
        labels = result["items"]
        formatted = []
        for label in labels:
            name = label.get("name", "Unknown")
            label_id = label.get("id", "")
            formatted.append(f"- {name} (ID: {label_id})")

        return {
            "success": True,
            "labels": labels,
            "formatted": "\n".join(formatted) if formatted else "No labels found",
            "message": "Use these label IDs with add_label_to_email and remove_label_from_email"
        }

    return result

@mcp.tool()
async def get_label(
    email: str,
    password: str,
    label_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get details of a specific label.

    Args:
        email: User email for authentication
        password: User password
        label_id: The label ID to retrieve
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Label details including name
    """
    return await quick_request(
        email, password, server_url,
        "GET", f"labels/{label_id}"
    )

@mcp.tool()
async def create_label(
    email: str,
    password: str,
    name: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Create a new label.

    Args:
        email: User email for authentication
        password: User password
        name: Label name (max 128 characters)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Created label details with ID
    """
    label_data = {
        "name": name
    }

    result = await quick_request(
        email, password, server_url,
        "POST", "labels",
        data=label_data
    )

    if result.get("id"):
        return {
            "success": True,
            "message": f"Label '{name}' created successfully",
            "label_id": result["id"],
            "data": result
        }

    return result

@mcp.tool()
async def update_label(
    email: str,
    password: str,
    label_id: str,
    name: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Update an existing label.

    Args:
        email: User email for authentication
        password: User password
        label_id: The label ID to update
        name: New label name (max 128 characters)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Updated label details
    """
    update_data = {
        "name": name
    }

    result = await quick_request(
        email, password, server_url,
        "PATCH", f"labels/{label_id}",
        data=update_data
    )

    if result.get("id"):
        return {
            "success": True,
            "message": "Label updated successfully",
            "data": result
        }

    return result

@mcp.tool()
async def delete_label(
    email: str,
    password: str,
    label_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Delete a label.

    Args:
        email: User email for authentication
        password: User password
        label_id: The label ID to delete
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Deletion status
    """
    result = await quick_request(
        email, password, server_url,
        "DELETE", f"labels/{label_id}"
    )

    if result.get("success"):
        return {
            "success": True,
            "message": "Label deleted successfully"
        }

    return result

# Email Label Operations

@mcp.tool()
async def add_label_to_email(
    email: str,
    password: str,
    mail_id: str,
    label_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Add a label to an email.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        label_id: The label ID to add (use list_labels to find available IDs)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Operation status with detailed feedback
    """
    # Validate label exists first
    label_exists = await validate_label_exists(email, password, server_url, label_id)
    if not label_exists:
        return {
            "success": False,
            "error": f"Label ID '{label_id}' not found",
            "message": "Use list_labels to get valid label IDs, or create_label to make a new one",
            "suggestion": "Run list_labels first to discover available labels"
        }

    label_data = {
        "labelId": label_id
    }

    try:
        result = await quick_request(
            email, password, server_url,
            "POST", f"mails/{mail_id}/labels",
            data=label_data
        )

        if result.get("success"):
            return {
                "success": True,
                "message": f"Label {label_id} added to email successfully"
            }

        return result
    except Exception as e:
        if "already applied" in str(e).lower():
            return {
                "success": True,
                "message": f"Label {label_id} already applied to email (idempotent operation)"
            }
        raise

@mcp.tool()
async def remove_label_from_email(
    email: str,
    password: str,
    mail_id: str,
    label_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Remove a label from an email.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        label_id: The label ID to remove
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Operation status with detailed feedback
    """
    try:
        result = await quick_request(
            email, password, server_url,
            "DELETE", f"mails/{mail_id}/labels/{label_id}"
        )

        if result.get("success"):
            return {
                "success": True,
                "message": f"Label {label_id} removed from email successfully"
            }

        return result
    except Exception as e:
        if "not found" in str(e).lower() or "404" in str(e):
            return {
                "success": True,
                "message": f"Label {label_id} was not applied to email (idempotent operation)"
            }
        raise

@mcp.tool()
async def add_label_by_name(
    email: str,
    password: str,
    mail_id: str,
    label_name: str,
    create_if_missing: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Add a label to an email by name, with option to auto-create the label.

    This is a convenience function that handles the label discovery workflow
    automatically, making labeling much easier for users.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        label_name: The label name to add
        create_if_missing: Create the label if it doesn't exist (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Operation status with detailed workflow information
    """
    # First try to find existing label
    label_id = await find_label_by_name(email, password, server_url, label_name)

    if not label_id and create_if_missing:
        # Create the label
        try:
            create_result = await quick_request(
                email, password, server_url,
                "POST", "labels",
                data={"name": label_name}
            )

            if create_result.get("id"):
                label_id = create_result["id"]
            else:
                return {
                    "success": False,
                    "error": f"Failed to create label '{label_name}'",
                    "details": create_result
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create label '{label_name}': {str(e)}"
            }
    elif not label_id:
        return {
            "success": False,
            "error": f"Label '{label_name}' not found",
            "message": "Set create_if_missing=True to auto-create, or use list_labels to see available labels"
        }

    # Now add the label to the email
    return await add_label_to_email(email, password, mail_id, label_id, server_url)


# Note: Message parts operations don't work as expected on ax.email
# The /parts endpoint returns the full message structure, not a list of parts
# @mcp.tool()
# async def list_message_parts(...)
# @mcp.tool()
# async def get_message_part(...)

# Note: Temporary attachment operations are not available on ax.email (404 errors)
# - create_temp_attachment, get_temp_attachment, delete_temp_attachment
# These may work on full Axigen installations
# To send emails with attachments on ax.email, include them inline in the email body

@mcp.tool()
async def get_email_headers(
    email: str,
    password: str,
    mail_id: str,
    use_fallback: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get email headers with intelligent fallbacks for reliability.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        use_fallback: Use get_email_source fallback if headers endpoint fails (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Email headers with fallback information
    """
    try:
        # First try the dedicated headers endpoint
        result = await quick_request(
            email, password, server_url,
            "GET", f"mails/{mail_id}/headers"
        )

        if result.get("success"):
            result["source"] = "headers_endpoint"
            return result

    except Exception as e:
        headers_error = str(e)

        if use_fallback and "404" in headers_error:
            # Fallback: Extract headers from email source
            try:
                source_result = await quick_request(
                    email, password, server_url,
                    "GET", f"mails/{mail_id}/source"
                )

                if source_result.get("success") or source_result.get("raw_response"):
                    # Extract headers from source
                    source_text = source_result.get("raw_response") or source_result.get("source", "")

                    if isinstance(source_text, str) and source_text:
                        # Extract headers (everything before first empty line)
                        lines = source_text.split('\n')
                        headers = []
                        for line in lines:
                            if line.strip() == "":
                                break
                            headers.append(line)

                        headers_text = '\n'.join(headers)

                        return {
                            "success": True,
                            "source": "source_fallback",
                            "headers": headers_text,
                            "message": "Headers extracted from email source (headers endpoint unavailable)",
                            "fallback_used": True,
                            "original_error": headers_error
                        }

            except Exception as fallback_error:
                return create_error_response(
                    "get_email_headers",
                    f"Headers endpoint failed and fallback failed",
                    "Try using get_email_source to get full email content",
                    {
                        "mail_id": mail_id,
                        "headers_error": headers_error,
                        "fallback_error": str(fallback_error)
                    }
                )

        return create_error_response(
            "get_email_headers",
            f"Headers endpoint failed: {headers_error}",
            "Try get_email_source for full email content, or set use_fallback=True",
            {"mail_id": mail_id, "error": headers_error}
        )

# Folder Tools

@mcp.tool()
async def list_folders(
    email: str,
    password: str,
    folder_type: str = "mails",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    List email folders with their IDs.

    Args:
        email: User email for authentication
        password: User password
        folder_type: Type of folders - "all", "mails", "events", "tasks", "notes", "contacts" (default: "mails")
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        List of folders with IDs and metadata
    """
    params = {
        "type": folder_type
    }

    result = await quick_request(
        email, password, server_url,
        "GET", "folders",
        params=params
    )

    if "items" in result:
        folders = result["items"]
        formatted = []
        common_folders = {}

        for folder in folders:
            name = folder.get("name", "unknown")
            folder_id = folder.get("id", "")
            unread = folder.get("unreadCount", 0)
            total = folder.get("totalCount", 0)
            formatted.append(f"- {name} (ID: {folder_id}, Unread: {unread}/{total})")

            # Track common folder names
            name_lower = name.lower()
            if name_lower in ["inbox", "sent", "drafts", "trash", "spam", "archive"]:
                common_folders[name_lower] = folder_id

        return {
            "success": True,
            "folders": folders,
            "common_folders": common_folders,
            "formatted": "\n".join(formatted) if formatted else "No folders found",
            "message": "Use the folder ID with list_emails to see messages in that folder"
        }

    return result

@mcp.tool()
async def create_folder(
    email: str,
    password: str,
    name: str,
    parent_id: Optional[str] = None,
    folder_type: str = "mails",
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Create a new email folder.

    Args:
        email: User email for authentication
        password: User password
        name: Name of the new folder
        parent_id: Parent folder ID (optional, defaults to root)
        folder_type: Type of folder - "mails" (default: "mails")
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        New folder details
    """
    folder_data = {
        "name": name,
        "type": folder_type
    }

    if parent_id:
        folder_data["parentId"] = parent_id

    result = await quick_request(
        email, password, server_url,
        "POST", "folders",
        data=folder_data
    )

    if result.get("id"):
        return {
            "success": True,
            "message": f"Folder '{name}' created successfully",
            "folder_id": result["id"],
            "data": result
        }

    return result

@mcp.tool()
async def update_folder(
    email: str,
    password: str,
    folder_id: str,
    name: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Update/rename a folder.

    Args:
        email: User email for authentication
        password: User password
        folder_id: The folder ID to update
        name: New folder name
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Updated folder details
    """
    folder_data = {
        "name": name
    }

    result = await quick_request(
        email, password, server_url,
        "PATCH", f"folders/{folder_id}",
        data=folder_data
    )

    if result.get("id"):
        return {
            "success": True,
            "message": f"Folder renamed to '{name}' successfully",
            "folder_id": result["id"],
            "data": result
        }

    return result

# Note: move_folder is not available on ax.email (404 errors)
# This may work on full Axigen installations

@mcp.tool()
async def delete_folder(
    email: str,
    password: str,
    folder_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Delete a folder (must be empty).

    Args:
        email: User email for authentication
        password: User password
        folder_id: The folder ID to delete
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Deletion status
    """
    result = await quick_request(
        email, password, server_url,
        "DELETE", f"folders/{folder_id}"
    )

    if result.get("success"):
        return {
            "success": True,
            "message": "Folder deleted successfully"
        }

    return result

# @mcp.tool()
# async def move_folder(...)

@mcp.tool()
async def get_common_folder_ids(
    email: str,
    password: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get fresh common folder IDs with enhanced discovery and validation.

    This function provides reliable, up-to-date folder IDs needed for other operations
    like list_emails. Uses intelligent mapping to handle folder name variations.

    Args:
        email: User email for authentication
        password: User password
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Dictionary with common folder names mapped to IDs plus discovery info
    """
    result = await get_reliable_common_folders(email, password, server_url)

    if result["success"]:
        folders = result["folders"]
        return {
            "success": True,
            "folders": folders,
            "total_folders": result["total_folders"],
            "discovered": result["discovered"],
            "message": f"Found {len(folders)} common folders from {result['total_folders']} total folders",
            "example": f"To list inbox emails: list_emails(folder_id='{folders.get('inbox', 'not_found')}')",
            "available_folders": list(folders.keys())
        }

    return result

# Unified Response Schema Helper

def create_unified_response(
    operation: str,
    success: bool,
    data: Any = None,
    message: str = None,
    error: str = None,
    suggestion: str = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create a standardized response format for all operations.

    Args:
        operation: Name of the operation performed
        success: Whether the operation succeeded
        data: The main response data
        message: Success message or description
        error: Error message if failed
        suggestion: Actionable suggestion for errors
        metadata: Additional metadata about the operation

    Returns:
        Standardized response dictionary
    """
    response = {
        "success": success,
        "operation": operation,
        "timestamp": "now"  # In real implementation, use actual timestamp
    }

    if success:
        if data is not None:
            response["data"] = data
        if message:
            response["message"] = message
    else:
        if error:
            response["error"] = error
        if suggestion:
            response["suggestion"] = suggestion

    if metadata:
        response["metadata"] = metadata

    return response

# Dry-Run and Preview Tools





# Draft-Specific Dry-Run and Testing Tools



if __name__ == "__main__":
    mcp.run()