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

# Note: search_emails is currently disabled as the query format for ax.email is unknown
# The endpoint exists but requires a specific query structure that hasn't been documented
# @mcp.tool()
# async def search_emails(...):
#     """
#     Search emails - CURRENTLY UNSUPPORTED on ax.email
#     The endpoint exists but the query format is unknown.
#     """
#     return {
#         "success": False,
#         "error": "Search is currently unsupported. Use list_emails with specific folder IDs instead."
#     }

@mcp.tool()
async def get_email(
    email: str,
    password: str,
    mail_id: str,
    include_body: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get detailed information about a specific email.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to retrieve
        include_body: Whether to include email body (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Full email details including headers and body
    """
    result = await quick_request(
        email, password, server_url,
        "GET", f"mails/{mail_id}"
    )

    if result.get("success") and include_body:
        body_result = await quick_request(
            email, password, server_url,
            "GET", f"mails/{mail_id}/body"
        )
        if body_result.get("success"):
            result["data"]["body"] = body_result["data"]

    return result

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
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Create a new draft email.

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
        Created draft details with ID
    """
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

    result = await quick_request(
        email, password, server_url,
        "POST", "mails",
        data=draft_data
    )

    if result.get("success"):
        return {
            "success": True,
            "message": "Draft created successfully",
            "draft_id": result["data"].get("id"),
            "data": result["data"]
        }

    return result

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
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Send an existing draft email.

    Args:
        email: User email for authentication
        password: User password
        draft_id: The draft email ID to send
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Send status
    """
    result = await quick_request(
        email, password, server_url,
        "POST", f"drafts/{draft_id}/send"
    )

    if result.get("success"):
        return {
            "success": True,
            "message": "Draft sent successfully",
            "data": result.get("data", {})
        }

    return result

@mcp.tool()
async def update_draft(
    email: str,
    password: str,
    draft_id: str,
    to: Optional[str] = None,
    subject: Optional[str] = None,
    body_text: Optional[str] = None,
    body_html: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Update an existing draft email.

    Args:
        email: User email for authentication
        password: User password
        draft_id: The draft email ID to update
        to: New recipient(s) (optional)
        subject: New subject (optional)
        body_text: New plain text body (optional)
        body_html: New HTML body (optional)
        cc: New CC recipients (optional)
        bcc: New BCC recipients (optional)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Updated draft details
    """
    update_data = {}

    if to is not None:
        update_data["to"] = to
    if subject is not None:
        update_data["subject"] = subject
    if body_text is not None:
        update_data["bodyText"] = body_text
    if body_html is not None:
        update_data["bodyHtml"] = body_html
    if cc is not None:
        update_data["cc"] = cc
    if bcc is not None:
        update_data["bcc"] = bcc

    return await quick_request(
        email, password, server_url,
        "PUT", f"drafts/{draft_id}",
        data=update_data
    )

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

@mcp.tool()
async def mark_as_not_spam(
    email: str,
    password: str,
    mail_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Mark an email as not spam.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID to mark as not spam
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Operation status
    """
    result = await quick_request(
        email, password, server_url,
        "POST", f"mails/{mail_id}/notspam"
    )

    if result.get("success"):
        return {
            "success": True,
            "message": "Email marked as not spam successfully"
        }

    return result

# Attachment Tools

@mcp.tool()
async def list_attachments(
    email: str,
    password: str,
    mail_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    List attachments in an email.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        List of attachments with metadata
    """
    result = await quick_request(
        email, password, server_url,
        "GET", f"mails/{mail_id}/attachments"
    )

    if result.get("success") and result.get("data"):
        attachments = result["data"].get("items", [])
        formatted = []
        for att in attachments:
            name = att.get("name", "unknown")
            size = att.get("size", 0)
            mime = att.get("mimeType", "unknown")
            formatted.append(f"- {name} ({size} bytes, {mime})")

        return {
            "success": True,
            "attachments": attachments,
            "formatted": "\n".join(formatted) if formatted else "No attachments"
        }

    return result

@mcp.tool()
async def get_email_headers(
    email: str,
    password: str,
    mail_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get email headers.

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Email headers
    """
    return await quick_request(
        email, password, server_url,
        "GET", f"mails/{mail_id}/headers"
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
async def get_common_folder_ids(
    email: str,
    password: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get IDs for common folders (Inbox, Sent, Drafts, etc.).

    Args:
        email: User email for authentication
        password: User password
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Dictionary with common folder names and their IDs
    """
    result = await quick_request(
        email, password, server_url,
        "GET", "folders",
        params={"type": "mails"}
    )

    if "items" in result:
        folders = result["items"]
        common_folders = {}

        for folder in folders:
            name = folder.get("name", "")
            folder_id = folder.get("id", "")
            name_lower = name.lower()

            # Map common folder names
            if name_lower == "inbox":
                common_folders["inbox"] = folder_id
            elif name_lower == "sent":
                common_folders["sent"] = folder_id
            elif name_lower == "drafts":
                common_folders["drafts"] = folder_id
            elif name_lower == "trash":
                common_folders["trash"] = folder_id
            elif name_lower == "spam":
                common_folders["spam"] = folder_id
            elif name_lower == "archive":
                common_folders["archive"] = folder_id
            elif name_lower == "flagged":
                common_folders["flagged"] = folder_id

        return {
            "success": True,
            "folders": common_folders,
            "message": f"Found {len(common_folders)} common folders. Use these IDs with list_emails.",
            "example": f"To list inbox emails, use folder_id='{common_folders.get('inbox', 'not_found')}'"
        }

    return {
        "success": False,
        "error": "Could not retrieve folders",
        "data": result
    }

if __name__ == "__main__":
    mcp.run()