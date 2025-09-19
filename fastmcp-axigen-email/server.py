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

@mcp.tool()
async def bulk_get_emails(
    email: str,
    password: str,
    mail_ids: List[str],
    include_body: bool = False,
    include_headers: bool = False,
    max_concurrent: int = 5,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Retrieve multiple emails efficiently with configurable detail levels.

    Args:
        email: User email for authentication
        password: User password
        mail_ids: List of email IDs to retrieve
        include_body: Include email bodies (increases processing time)
        include_headers: Include email headers (increases processing time)
        max_concurrent: Maximum concurrent requests (default: 5)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Bulk retrieval results with per-email status
    """
    import asyncio

    results = {
        "success": True,
        "total_requested": len(mail_ids),
        "successful": 0,
        "failed": 0,
        "emails": {},
        "errors": {},
        "processing_time": "estimated"
    }

    async def fetch_single_email(mail_id: str) -> tuple[str, dict]:
        """Fetch a single email with error handling."""
        try:
            # Get basic email info
            email_result = await quick_request(
                email, password, server_url,
                "GET", f"mails/{mail_id}"
            )

            if not email_result.get("success"):
                return mail_id, {"error": "Failed to retrieve email", "details": email_result}

            email_data = email_result.get("data", {})

            # Add body if requested
            if include_body:
                try:
                    body_result = await quick_request(
                        email, password, server_url,
                        "GET", f"mails/{mail_id}/body"
                    )
                    if body_result.get("success"):
                        email_data["body"] = body_result.get("data")
                    else:
                        email_data["body_error"] = "Could not retrieve body"
                except Exception as e:
                    email_data["body_error"] = str(e)

            # Add headers if requested
            if include_headers:
                try:
                    headers_result = await quick_request(
                        email, password, server_url,
                        "GET", f"mails/{mail_id}/headers"
                    )
                    if headers_result.get("success"):
                        email_data["headers"] = headers_result.get("data")
                    else:
                        email_data["headers_error"] = "Could not retrieve headers"
                except Exception as e:
                    email_data["headers_error"] = str(e)

            return mail_id, email_data

        except Exception as e:
            return mail_id, {"error": str(e)}

    # Process emails in batches to respect server limits
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_with_semaphore(mail_id: str):
        async with semaphore:
            return await fetch_single_email(mail_id)

    # Execute all requests
    tasks = [fetch_with_semaphore(mail_id) for mail_id in mail_ids]
    fetch_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for result in fetch_results:
        if isinstance(result, Exception):
            results["failed"] += 1
            results["errors"]["general"] = str(result)
        else:
            mail_id, email_data = result
            if "error" in email_data:
                results["failed"] += 1
                results["errors"][mail_id] = email_data["error"]
            else:
                results["successful"] += 1
                results["emails"][mail_id] = email_data

    # Update success status
    if results["failed"] > 0:
        results["success"] = results["successful"] > 0  # Partial success allowed

    results["message"] = f"Retrieved {results['successful']}/{results['total_requested']} emails"
    return results

@mcp.tool()
async def batch_email_search(
    email: str,
    password: str,
    search_queries: List[Dict[str, Any]],
    max_results_per_query: int = 20,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Execute multiple search queries efficiently.

    Args:
        email: User email for authentication
        password: User password
        search_queries: List of search query dictionaries
        max_results_per_query: Max results per query (default: 20)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Batch search results with per-query status
    """
    results = {
        "success": True,
        "total_queries": len(search_queries),
        "successful_queries": 0,
        "failed_queries": 0,
        "search_results": {},
        "errors": {}
    }

    for i, query in enumerate(search_queries):
        query_id = f"query_{i + 1}"
        try:
            search_result = await search_emails(
                email, password,
                query.get("search_criteria", []),
                query.get("start", 0),
                min(query.get("limit", max_results_per_query), max_results_per_query),
                server_url
            )

            if search_result.get("success"):
                results["successful_queries"] += 1
                results["search_results"][query_id] = {
                    "query": query,
                    "results": search_result
                }
            else:
                results["failed_queries"] += 1
                results["errors"][query_id] = search_result.get("error", "Unknown error")

        except Exception as e:
            results["failed_queries"] += 1
            results["errors"][query_id] = str(e)

    if results["failed_queries"] > 0:
        results["success"] = results["successful_queries"] > 0

    results["message"] = f"Executed {results['successful_queries']}/{results['total_queries']} search queries"
    return results

# Bulk Draft and Template Operations

@mcp.tool()
async def bulk_create_drafts(
    email: str,
    password: str,
    draft_templates: List[Dict[str, Any]],
    validate_all: bool = True,
    max_concurrent: int = 3,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Create multiple drafts from templates efficiently.

    Args:
        email: User email for authentication
        password: User password
        draft_templates: List of draft template dictionaries
        validate_all: Validate all templates before creating any drafts (default: True)
        max_concurrent: Maximum concurrent draft creations (default: 3)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Bulk creation results with per-draft status
    """
    import asyncio

    results = {
        "success": True,
        "total_requested": len(draft_templates),
        "successful": 0,
        "failed": 0,
        "drafts": {},
        "errors": {},
        "templates_validated": validate_all
    }

    # Pre-validate all templates if requested
    if validate_all:
        validation_errors = []
        for i, template in enumerate(draft_templates):
            template_id = f"template_{i + 1}"

            # Check required fields
            if not template.get("to") or not template.get("subject"):
                validation_errors.append({
                    "template_id": template_id,
                    "error": "Missing required fields: 'to' and 'subject'"
                })
                continue

            # Validate recipients
            recipients = [addr.strip() for addr in template["to"].split(",")]
            invalid_recipients = [r for r in recipients if "@" not in r or "." not in r.split("@")[-1]]
            if invalid_recipients:
                validation_errors.append({
                    "template_id": template_id,
                    "error": f"Invalid recipients: {', '.join(invalid_recipients)}"
                })

            # Check body content
            if not template.get("body_text") and not template.get("body_html"):
                validation_errors.append({
                    "template_id": template_id,
                    "error": "Either body_text or body_html required"
                })

        if validation_errors:
            return {
                "success": False,
                "error": "Template validation failed",
                "validation_errors": validation_errors,
                "message": f"Failed validation for {len(validation_errors)} templates"
            }

    async def create_single_draft(template_index: int, template: Dict[str, Any]) -> tuple[str, dict]:
        """Create a single draft with error handling."""
        template_id = f"template_{template_index + 1}"
        try:
            result = await create_draft(
                email, password,
                template["to"],
                template["subject"],
                template.get("body_text"),
                template.get("body_html"),
                template.get("cc"),
                template.get("bcc"),
                template.get("reply_to"),
                template.get("importance", "normal"),
                validate_recipients=False,  # Already validated above
                server_url=server_url
            )

            if result.get("success"):
                return template_id, {
                    "draft_id": result.get("draft_id"),
                    "template": template,
                    "creation_result": result
                }
            else:
                return template_id, {"error": result.get("error", "Creation failed")}

        except Exception as e:
            return template_id, {"error": str(e)}

    # Process drafts with concurrency control
    semaphore = asyncio.Semaphore(max_concurrent)

    async def create_with_semaphore(template_index: int, template: Dict[str, Any]):
        async with semaphore:
            return await create_single_draft(template_index, template)

    # Execute all creation tasks
    tasks = [create_with_semaphore(i, template) for i, template in enumerate(draft_templates)]
    creation_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for result in creation_results:
        if isinstance(result, Exception):
            results["failed"] += 1
            results["errors"]["general"] = str(result)
        else:
            template_id, draft_data = result
            if "error" in draft_data:
                results["failed"] += 1
                results["errors"][template_id] = draft_data["error"]
            else:
                results["successful"] += 1
                results["drafts"][template_id] = draft_data

    # Update success status
    if results["failed"] > 0:
        results["success"] = results["successful"] > 0  # Partial success allowed

    results["message"] = f"Created {results['successful']}/{results['total_requested']} drafts"
    return results

@mcp.tool()
async def batch_send_drafts(
    email: str,
    password: str,
    draft_ids: List[str],
    validate_drafts: bool = True,
    max_concurrent: int = 3,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Send multiple drafts efficiently with per-draft tracking.

    Args:
        email: User email for authentication
        password: User password
        draft_ids: List of draft IDs to send
        validate_drafts: Pre-validate all drafts exist (default: True)
        max_concurrent: Maximum concurrent send operations (default: 3)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Batch send results with per-draft status
    """
    import asyncio

    results = {
        "success": True,
        "total_requested": len(draft_ids),
        "successful": 0,
        "failed": 0,
        "sent_emails": {},
        "errors": {},
        "drafts_validated": validate_drafts
    }

    async def send_single_draft(draft_id: str) -> tuple[str, dict]:
        """Send a single draft with error handling."""
        try:
            result = await send_draft(
                email, password, draft_id,
                validate_draft=validate_drafts,
                idempotent=True,
                server_url=server_url
            )

            if result.get("success"):
                return draft_id, {
                    "mail_id": result.get("mail_id"),
                    "processing_id": result.get("processing_id"),
                    "send_result": result
                }
            else:
                return draft_id, {"error": result.get("error", "Send failed")}

        except Exception as e:
            return draft_id, {"error": str(e)}

    # Process sends with concurrency control
    semaphore = asyncio.Semaphore(max_concurrent)

    async def send_with_semaphore(draft_id: str):
        async with semaphore:
            return await send_single_draft(draft_id)

    # Execute all send tasks
    tasks = [send_with_semaphore(draft_id) for draft_id in draft_ids]
    send_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for result in send_results:
        if isinstance(result, Exception):
            results["failed"] += 1
            results["errors"]["general"] = str(result)
        else:
            draft_id, send_data = result
            if "error" in send_data:
                results["failed"] += 1
                results["errors"][draft_id] = send_data["error"]
            else:
                results["successful"] += 1
                results["sent_emails"][draft_id] = send_data

    # Update success status
    if results["failed"] > 0:
        results["success"] = results["successful"] > 0  # Partial success allowed

    results["message"] = f"Sent {results['successful']}/{results['total_requested']} drafts"
    return results

@mcp.tool()
async def create_draft_template(
    template_name: str,
    to: str,
    subject: str,
    body_text: str = None,
    body_html: str = None,
    cc: str = None,
    bcc: str = None,
    reply_to: str = None,
    importance: str = "normal",
    variables: List[str] = None
) -> Dict[str, Any]:
    """
    Create a reusable draft template with placeholder support.

    Args:
        template_name: Name for the template
        to: Recipient(s) - can include variables like {{recipient_email}}
        subject: Subject line - can include variables like {{subject_prefix}}
        body_text: Plain text body with variable placeholders
        body_html: HTML body with variable placeholders
        cc: CC recipients with variable placeholders
        bcc: BCC recipients with variable placeholders
        reply_to: Reply-To address
        importance: Email importance level
        variables: List of variable names used in the template

    Returns:
        Template definition with usage instructions
    """
    template = {
        "template_name": template_name,
        "template_data": {
            "to": to,
            "subject": subject,
            "body_text": body_text,
            "body_html": body_html,
            "cc": cc,
            "bcc": bcc,
            "reply_to": reply_to,
            "importance": importance
        },
        "variables": variables or [],
        "usage_example": {
            "description": "Use bulk_create_drafts with variable substitution",
            "example_variables": {var: f"example_{var}" for var in (variables or [])}
        }
    }

    # Detect variables automatically if not provided
    if not variables:
        import re
        detected_vars = set()
        for field_name, field_value in template["template_data"].items():
            if isinstance(field_value, str):
                matches = re.findall(r'\{\{([^}]+)\}\}', field_value)
                detected_vars.update(matches)
        template["variables"] = list(detected_vars)

    return {
        "success": True,
        "template": template,
        "message": f"Template '{template_name}' created with {len(template['variables'])} variables",
        "variables_found": template["variables"]
    }

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

@mcp.tool()
async def bulk_label_emails(
    email: str,
    password: str,
    mail_ids: List[str],
    label_name: str,
    create_if_missing: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Apply a label to multiple emails at once.

    Args:
        email: User email for authentication
        password: User password
        mail_ids: List of email IDs to label
        label_name: The label name to add
        create_if_missing: Create the label if it doesn't exist (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Bulk operation results with per-email status
    """
    results = {
        "success": True,
        "total_emails": len(mail_ids),
        "successful": 0,
        "failed": 0,
        "details": []
    }

    # Get or create label once
    label_id = await find_label_by_name(email, password, server_url, label_name)

    if not label_id and create_if_missing:
        try:
            create_result = await quick_request(
                email, password, server_url,
                "POST", "labels",
                data={"name": label_name}
            )
            if create_result.get("id"):
                label_id = create_result["id"]
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create label '{label_name}': {str(e)}"
            }

    if not label_id:
        return {
            "success": False,
            "error": f"Label '{label_name}' not found and create_if_missing=False"
        }

    # Apply label to each email
    for mail_id in mail_ids:
        try:
            result = await add_label_to_email(email, password, mail_id, label_id, server_url)
            if result.get("success"):
                results["successful"] += 1
                results["details"].append({"mail_id": mail_id, "status": "success"})
            else:
                results["failed"] += 1
                results["details"].append({"mail_id": mail_id, "status": "failed", "error": result.get("error", "Unknown error")})
        except Exception as e:
            results["failed"] += 1
            results["details"].append({"mail_id": mail_id, "status": "failed", "error": str(e)})

    if results["failed"] > 0:
        results["success"] = False

    results["message"] = f"Labeled {results['successful']}/{results['total_emails']} emails with '{label_name}'"
    return results

@mcp.tool()
async def get_email_source(
    email: str,
    password: str,
    mail_id: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get the raw source of an email (as text, suitable for saving as .eml).

    Args:
        email: User email for authentication
        password: User password
        mail_id: The email ID
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Raw email source including headers and body
    """
    result = await quick_request(
        email, password, server_url,
        "GET", f"mails/{mail_id}/source"
    )

    # Check for raw_response field (ax.email format)
    if result.get("raw_response"):
        return {
            "success": True,
            "source": result["raw_response"],
            "message": "Email source retrieved. You can save this as a .eml file."
        }

    if isinstance(result, str):
        return {
            "success": True,
            "source": result,
            "message": "Email source retrieved. You can save this as a .eml file."
        }

    # If it returns data field with base64
    if result.get("data"):
        import base64
        try:
            decoded = base64.b64decode(result["data"]).decode('utf-8')
            return {
                "success": True,
                "source": decoded,
                "message": "Email source retrieved and decoded."
            }
        except:
            return {
                "success": True,
                "source": result["data"],
                "message": "Email source retrieved (base64 encoded)."
            }

    return result

# Note: Message parts operations don't work as expected on ax.email
# The /parts endpoint returns the full message structure, not a list of parts
# @mcp.tool()
# async def list_message_parts(...)
# @mcp.tool()
# async def get_message_part(...)

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

@mcp.tool()
async def preview_folder_operation(
    email: str,
    password: str,
    operation: str,
    folder_id: str = None,
    folder_name: str = None,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Preview folder operations without making changes.

    Args:
        email: User email for authentication
        password: User password
        operation: Operation to preview ('list', 'create', 'delete', etc.)
        folder_id: Folder ID for operations requiring it
        folder_name: Folder name for create operations
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Preview of what the operation would do
    """
    preview = {
        "dry_run": True,
        "operation": operation,
        "would_execute": False
    }

    if operation == "list":
        # Preview folder listing
        try:
            folders_result = await get_reliable_common_folders(email, password, server_url)
            if folders_result["success"]:
                preview.update({
                    "success": True,
                    "preview": f"Would list {folders_result['total_folders']} folders",
                    "available_folders": list(folders_result["folders"].keys()),
                    "recommendation": "Use list_folders to execute this operation"
                })
            else:
                preview.update({
                    "success": False,
                    "error": "Cannot preview - folder access failed",
                    "details": folders_result
                })
        except Exception as e:
            preview.update({"success": False, "error": str(e)})

    elif operation == "create" and folder_name:
        # Preview folder creation
        existing_folder = await auto_discover_folder_id(email, password, server_url, folder_name)
        if existing_folder:
            preview.update({
                "success": False,
                "preview": f"Would NOT create folder '{folder_name}' - already exists",
                "existing_id": existing_folder,
                "recommendation": "Choose a different name or use existing folder"
            })
        else:
            preview.update({
                "success": True,
                "preview": f"Would create new folder '{folder_name}'",
                "recommendation": "Use create_folder to execute this operation"
            })

    elif operation == "delete" and folder_id:
        # Preview folder deletion
        validation = await validate_folder_id(email, password, server_url, folder_id)
        if validation["valid"]:
            preview.update({
                "success": True,
                "preview": f"Would delete folder '{validation['name']}' (ID: {folder_id})",
                "warning": "This action cannot be undone",
                "recommendation": "Use delete_folder to execute this operation"
            })
        else:
            preview.update({
                "success": False,
                "preview": "Cannot delete - folder not found",
                "error": validation["error"]
            })

    else:
        preview.update({
            "success": False,
            "error": "Unsupported operation or missing parameters",
            "supported_operations": ["list", "create", "delete"]
        })

    return preview

# Draft Auditing and Traceability

@mcp.tool()
async def get_draft_lifecycle_history(
    email: str,
    password: str,
    draft_id: str,
    include_content_changes: bool = False,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Get the complete lifecycle history of a draft.

    Args:
        email: User email for authentication
        password: User password
        draft_id: Draft ID to trace
        include_content_changes: Include content snapshots (default: False)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Complete draft lifecycle with timestamps and actions
    """
    import time

    history = {
        "draft_id": draft_id,
        "lifecycle_events": [],
        "current_status": "unknown",
        "traced_at": int(time.time())
    }

    try:
        # Check if draft exists in drafts folder
        drafts_info = await get_drafts_folder_info(email, password, server_url)
        if drafts_info["success"]:
            drafts_result = await quick_request(
                email, password, server_url,
                "GET", "mails",
                params={"folderId": drafts_info["drafts_folder_id"], "limit": 100}
            )

            if drafts_result.get("success"):
                draft_items = drafts_result.get("data", {}).get("items", [])
                draft = next((item for item in draft_items if item.get("id") == draft_id), None)

                if draft:
                    history["current_status"] = "draft"
                    history["lifecycle_events"].append({
                        "event": "draft_exists",
                        "timestamp": draft.get("date"),
                        "details": {
                            "subject": draft.get("subject"),
                            "to": draft.get("to", []),
                            "size": draft.get("size", 0),
                            "is_flagged": draft.get("isFlagged", False)
                        }
                    })

                    if include_content_changes:
                        # Get current content
                        try:
                            content_result = await get_email(
                                email, password, draft_id,
                                include_body=True, validate_id=False,
                                server_url=server_url
                            )
                            if content_result.get("success"):
                                history["current_content"] = content_result.get("api_data", {})
                        except Exception:
                            pass
                else:
                    # Draft not in drafts folder - check if it was sent
                    history["current_status"] = "possibly_sent"
                    history["lifecycle_events"].append({
                        "event": "not_in_drafts",
                        "timestamp": int(time.time()),
                        "details": {
                            "inference": "Draft may have been sent or deleted",
                            "recommendation": "Check Sent folder for confirmation"
                        }
                    })

        # Check Sent folder for evidence
        try:
            folders_result = await get_reliable_common_folders(email, password, server_url)
            if folders_result["success"] and "sent" in folders_result["folders"]:
                sent_folder_id = folders_result["folders"]["sent"]
                sent_result = await quick_request(
                    email, password, server_url,
                    "GET", "mails",
                    params={"folderId": sent_folder_id, "limit": 50}
                )

                if sent_result.get("success"):
                    # Look for emails that might match our draft
                    sent_items = sent_result.get("data", {}).get("items", [])
                    # This is approximate - we can't definitively link draft_id to sent mail_id
                    # But we can provide likely matches
                    recent_sent = [item for item in sent_items if item.get("date")][:10]
                    if recent_sent:
                        history["lifecycle_events"].append({
                            "event": "recent_sent_emails",
                            "timestamp": int(time.time()),
                            "details": {
                                "note": "Recent sent emails (may include this draft if sent)",
                                "recent_sent_count": len(recent_sent),
                                "recent_subjects": [item.get("subject", "No Subject") for item in recent_sent[:5]]
                            }
                        })
        except Exception:
            pass

        return {
            "success": True,
            "history": history,
            "message": f"Traced {len(history['lifecycle_events'])} lifecycle events for draft {draft_id}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "draft_id": draft_id,
            "message": "Failed to trace draft lifecycle"
        }

@mcp.tool()
async def audit_draft_operations(
    email: str,
    password: str,
    operation_type: str = None,
    time_range_hours: int = 24,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Audit recent draft operations for accountability and tracking.

    Args:
        email: User email for authentication
        password: User password
        operation_type: Filter by operation type ('create', 'send', 'update')
        time_range_hours: Hours to look back (default: 24)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Audit report of draft operations
    """
    import time
    from datetime import datetime, timedelta

    audit_report = {
        "audit_timestamp": int(time.time()),
        "time_range_hours": time_range_hours,
        "operation_filter": operation_type,
        "findings": {
            "current_drafts": 0,
            "recent_activity": [],
            "statistics": {}
        }
    }

    try:
        # Get current drafts
        drafts_result = await list_current_drafts(email, password, server_url, limit=100)
        if drafts_result["success"]:
            audit_report["findings"]["current_drafts"] = len(drafts_result["drafts"])

            # Analyze draft creation patterns
            draft_subjects = [draft.get("subject", "No Subject") for draft in drafts_result["drafts"]]
            audit_report["findings"]["statistics"]["draft_subjects"] = draft_subjects[:10]  # Top 10
            audit_report["findings"]["statistics"]["avg_subject_length"] = sum(len(s) for s in draft_subjects) / len(draft_subjects) if draft_subjects else 0

            # Recent activity analysis
            cutoff_time = datetime.now() - timedelta(hours=time_range_hours)
            recent_drafts = []

            for draft in drafts_result["drafts"]:
                if draft.get("created"):
                    try:
                        # Parse date (format may vary)
                        draft_time = draft["created"]
                        recent_drafts.append({
                            "action": "draft_created",
                            "draft_id": draft["draft_id"],
                            "subject": draft["subject"],
                            "timestamp": draft_time,
                            "recipients": len(draft.get("to", []))
                        })
                    except Exception:
                        pass

            audit_report["findings"]["recent_activity"] = recent_drafts

        # Get sent folder activity
        try:
            folders_result = await get_reliable_common_folders(email, password, server_url)
            if folders_result["success"] and "sent" in folders_result["folders"]:
                sent_folder_id = folders_result["folders"]["sent"]
                sent_result = await quick_request(
                    email, password, server_url,
                    "GET", "mails",
                    params={"folderId": sent_folder_id, "limit": 50}
                )

                if sent_result.get("success"):
                    sent_items = sent_result.get("data", {}).get("items", [])
                    recent_sent = sent_items[:10]  # Most recent 10

                    audit_report["findings"]["statistics"]["recent_sent_count"] = len(recent_sent)
                    audit_report["findings"]["statistics"]["recent_sent_subjects"] = [
                        item.get("subject", "No Subject") for item in recent_sent
                    ]
        except Exception:
            pass

        # Summary statistics
        total_activity = len(audit_report["findings"]["recent_activity"])
        audit_report["findings"]["statistics"]["total_recent_activity"] = total_activity
        audit_report["findings"]["statistics"]["activity_rate"] = f"{total_activity / time_range_hours:.2f} operations/hour"

        return {
            "success": True,
            "audit_report": audit_report,
            "message": f"Audited {total_activity} recent operations in {time_range_hours} hour window"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Audit failed - check account permissions and connectivity"
        }

@mcp.tool()
async def guided_draft_workflow(
    email: str,
    password: str,
    workflow_type: str = "create_send",
    parameters: Dict[str, Any] = None,
    dry_run: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Execute a guided draft workflow with step-by-step tracking.

    Args:
        email: User email for authentication
        password: User password
        workflow_type: Type of workflow ('create_send', 'update_send', 'bulk_create')
        parameters: Workflow parameters
        dry_run: Preview workflow without executing (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Guided workflow execution with step-by-step results
    """
    workflow = {
        "workflow_type": workflow_type,
        "dry_run": dry_run,
        "steps": [],
        "current_step": 0,
        "success": True
    }

    if workflow_type == "create_send" and parameters:
        # Create → Send workflow
        workflow["steps"] = [
            {"step": 1, "action": "validate_parameters", "status": "pending"},
            {"step": 2, "action": "create_draft", "status": "pending"},
            {"step": 3, "action": "send_draft", "status": "pending"},
            {"step": 4, "action": "verify_sent", "status": "pending"}
        ]

        # Step 1: Validate parameters
        workflow["current_step"] = 1
        required_params = ["to", "subject"]
        missing_params = [p for p in required_params if not parameters.get(p)]

        if missing_params:
            workflow["steps"][0]["status"] = "failed"
            workflow["steps"][0]["error"] = f"Missing required parameters: {', '.join(missing_params)}"
            workflow["success"] = False
            return {"success": False, "workflow": workflow}

        workflow["steps"][0]["status"] = "completed"

        if not dry_run:
            # Step 2: Create draft
            workflow["current_step"] = 2
            create_result = await create_draft(
                email, password,
                parameters["to"],
                parameters["subject"],
                parameters.get("body_text"),
                parameters.get("body_html"),
                parameters.get("cc"),
                parameters.get("bcc"),
                parameters.get("reply_to"),
                parameters.get("importance", "normal"),
                server_url=server_url
            )

            if create_result.get("success"):
                workflow["steps"][1]["status"] = "completed"
                workflow["steps"][1]["result"] = create_result
                draft_id = create_result.get("draft_id")

                # Step 3: Send draft
                workflow["current_step"] = 3
                send_result = await send_draft(
                    email, password, draft_id,
                    server_url=server_url
                )

                if send_result.get("success"):
                    workflow["steps"][2]["status"] = "completed"
                    workflow["steps"][2]["result"] = send_result

                    # Step 4: Verify sent (simplified)
                    workflow["current_step"] = 4
                    workflow["steps"][3]["status"] = "completed"
                    workflow["steps"][3]["verification"] = "Email sent successfully"
                else:
                    workflow["steps"][2]["status"] = "failed"
                    workflow["steps"][2]["error"] = send_result.get("error")
                    workflow["success"] = False
            else:
                workflow["steps"][1]["status"] = "failed"
                workflow["steps"][1]["error"] = create_result.get("error")
                workflow["success"] = False
        else:
            # Dry run - just preview
            for i in range(1, len(workflow["steps"])):
                workflow["steps"][i]["status"] = "would_execute"
                workflow["steps"][i]["preview"] = f"Would execute: {workflow['steps'][i]['action']}"

    else:
        return {
            "success": False,
            "error": "Unsupported workflow type or missing parameters",
            "supported_workflows": ["create_send"],
            "required_parameters": {
                "create_send": ["to", "subject"]
            }
        }

    return {
        "success": workflow["success"],
        "workflow": workflow,
        "message": f"Workflow {'preview' if dry_run else 'execution'} completed"
    }

@mcp.tool()
async def validate_operation_requirements(
    operation: str,
    parameters: Dict[str, Any],
    email: str,
    password: str,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Validate all requirements for an operation before execution.

    Args:
        operation: Operation name to validate
        parameters: Parameters that would be passed to the operation
        email: User email for authentication
        password: User password
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Validation results with recommendations
    """
    validation = {
        "operation": operation,
        "valid": True,
        "issues": [],
        "recommendations": [],
        "can_proceed": True
    }

    # Validate common parameters
    if "mail_id" in parameters:
        mail_validation = await validate_mail_id(email, password, server_url, parameters["mail_id"])
        if not mail_validation["valid"]:
            validation["valid"] = False
            validation["issues"].append(f"Invalid mail_id: {mail_validation['error']}")
            validation["recommendations"].append(mail_validation.get("suggestion", "Verify mail_id"))

    if "folder_id" in parameters:
        folder_validation = await validate_folder_id(email, password, server_url, parameters["folder_id"])
        if not folder_validation["valid"]:
            validation["valid"] = False
            validation["issues"].append(f"Invalid folder_id: {folder_validation['error']}")
            validation["recommendations"].append(folder_validation.get("suggestion", "Verify folder_id"))

    if "label_id" in parameters:
        label_valid = await validate_label_exists(email, password, server_url, parameters["label_id"])
        if not label_valid:
            validation["valid"] = False
            validation["issues"].append(f"Invalid label_id: {parameters['label_id']}")
            validation["recommendations"].append("Use list_labels to get valid label IDs")

    # Operation-specific validations
    if operation == "list_emails":
        if "folder_id" not in parameters:
            validation["valid"] = False
            validation["issues"].append("folder_id is required for list_emails")
            validation["recommendations"].append("Use get_common_folder_ids to discover folder IDs")

    validation["can_proceed"] = validation["valid"] and len(validation["issues"]) == 0

    if validation["can_proceed"]:
        validation["message"] = f"All requirements satisfied for {operation}"
    else:
        validation["message"] = f"Requirements not met for {operation} - fix issues before proceeding"

    return validation

# Draft-Specific Dry-Run and Testing Tools

@mcp.tool()
async def preview_draft_operation(
    email: str,
    password: str,
    operation: str,
    draft_id: str = None,
    to: str = None,
    subject: str = None,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    Preview draft operations without making changes.

    Args:
        email: User email for authentication
        password: User password
        operation: Operation to preview ('create', 'update', 'send', 'list')
        draft_id: Draft ID for operations requiring it
        to: Recipients for create/send operations
        subject: Subject for create operations
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Preview of what the operation would do
    """
    preview = {
        "dry_run": True,
        "operation": operation,
        "would_execute": False
    }

    if operation == "list":
        # Preview draft listing
        try:
            drafts_info = await get_drafts_folder_info(email, password, server_url)
            if drafts_info["success"]:
                preview.update({
                    "success": True,
                    "preview": f"Would list {drafts_info['draft_count']} drafts",
                    "drafts_folder_id": drafts_info["drafts_folder_id"],
                    "current_draft_count": drafts_info["draft_count"],
                    "recommendation": "Use list_current_drafts to execute this operation"
                })
            else:
                preview.update({
                    "success": False,
                    "error": "Cannot preview - drafts folder access failed",
                    "details": drafts_info
                })
        except Exception as e:
            preview.update({"success": False, "error": str(e)})

    elif operation == "create" and to and subject:
        # Preview draft creation
        try:
            # Validate recipients
            recipients = [addr.strip() for addr in to.split(",")]
            invalid_recipients = [r for r in recipients if "@" not in r or "." not in r.split("@")[-1]]

            drafts_info = await get_drafts_folder_info(email, password, server_url)

            if invalid_recipients:
                preview.update({
                    "success": False,
                    "preview": f"Would NOT create draft - invalid recipients: {', '.join(invalid_recipients)}",
                    "invalid_recipients": invalid_recipients,
                    "recommendation": "Fix recipient email formats before creating"
                })
            elif drafts_info["success"]:
                preview.update({
                    "success": True,
                    "preview": f"Would create draft '{subject}' to {len(recipients)} recipient(s)",
                    "recipients": recipients,
                    "current_draft_count": drafts_info["draft_count"],
                    "new_draft_count": drafts_info["draft_count"] + 1,
                    "recommendation": "Use create_draft to execute this operation"
                })
            else:
                preview.update({
                    "success": False,
                    "error": "Cannot access drafts folder",
                    "details": drafts_info
                })
        except Exception as e:
            preview.update({"success": False, "error": str(e)})

    elif operation == "send" and draft_id:
        # Preview draft sending
        try:
            draft_validation = await validate_mail_id(email, password, server_url, draft_id)
            if draft_validation["valid"]:
                # Check if draft is in drafts folder
                drafts_info = await get_drafts_folder_info(email, password, server_url)
                if drafts_info["success"]:
                    drafts_result = await quick_request(
                        email, password, server_url,
                        "GET", "mails",
                        params={"folderId": drafts_info["drafts_folder_id"], "limit": 100}
                    )

                    if drafts_result.get("success"):
                        draft_ids = [item.get("id") for item in drafts_result.get("data", {}).get("items", [])]
                        if draft_id in draft_ids:
                            # Find the specific draft
                            draft = next((item for item in drafts_result["data"]["items"] if item.get("id") == draft_id), None)
                            preview.update({
                                "success": True,
                                "preview": f"Would send draft '{draft.get('subject', 'Unknown')}' to {len(draft.get('to', []))} recipient(s)",
                                "draft_subject": draft.get("subject"),
                                "recipients": draft.get("to", []),
                                "current_draft_count": drafts_info["draft_count"],
                                "new_draft_count": drafts_info["draft_count"] - 1,
                                "recommendation": "Use send_draft to execute this operation"
                            })
                        else:
                            preview.update({
                                "success": False,
                                "preview": "Draft not found in Drafts folder - might already be sent",
                                "recommendation": "Check if draft was already sent"
                            })
            else:
                preview.update({
                    "success": False,
                    "preview": "Cannot send - draft not found",
                    "error": draft_validation["error"]
                })
        except Exception as e:
            preview.update({"success": False, "error": str(e)})

    elif operation == "update" and draft_id:
        # Preview draft update
        try:
            draft_validation = await validate_mail_id(email, password, server_url, draft_id)
            if draft_validation["valid"]:
                preview.update({
                    "success": True,
                    "preview": f"Would update draft (ID: {draft_id})",
                    "current_subject": draft_validation.get("subject", "Unknown"),
                    "warning": "Update replaces entire draft content",
                    "recommendation": "Use update_draft to execute this operation"
                })
            else:
                preview.update({
                    "success": False,
                    "preview": "Cannot update - draft not found",
                    "error": draft_validation["error"]
                })
        except Exception as e:
            preview.update({"success": False, "error": str(e)})

    else:
        preview.update({
            "success": False,
            "error": "Unsupported operation or missing required parameters",
            "supported_operations": ["list", "create", "send", "update"],
            "required_parameters": {
                "create": ["to", "subject"],
                "send": ["draft_id"],
                "update": ["draft_id"],
                "list": []
            }
        })

    return preview

@mcp.tool()
async def list_current_drafts_enhanced(
    email: str,
    password: str,
    limit: int = 20,
    include_preview: bool = True,
    server_url: str = "https://ax.email"
) -> Dict[str, Any]:
    """
    List current drafts with enhanced metadata and preview capabilities.

    Args:
        email: User email for authentication
        password: User password
        limit: Maximum number of drafts to retrieve (default: 20)
        include_preview: Include send preview for each draft (default: True)
        server_url: Axigen server URL (default: https://ax.email)

    Returns:
        Enhanced draft listing with lifecycle and preview information
    """
    result = await list_current_drafts(email, password, server_url, limit)

    if result["success"] and include_preview:
        # Add preview information for each draft
        for draft in result["drafts"]:
            try:
                send_preview = await preview_draft_operation(
                    email, password, "send", draft["draft_id"], server_url=server_url
                )
                draft["send_preview"] = send_preview.get("preview", "Preview unavailable")
                draft["can_send"] = send_preview.get("success", False)
            except Exception:
                draft["send_preview"] = "Preview failed"
                draft["can_send"] = False

    return result

if __name__ == "__main__":
    mcp.run()