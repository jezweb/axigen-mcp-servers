# FastMCP Axigen Email Server

MCP server for Axigen email operations, providing comprehensive email management through the Axigen REST API.

✅ **UPDATE**: This server has been tested and **DOES work with ax.email**! The Mailbox API is available on ax.email with specific parameter requirements documented below.

## Features

This server provides 35 working tools for email operations on ax.email with enhanced reliability features:

### Email Reading & Search
- `list_emails` - List emails with pagination and sorting (**requires folder_id**)
- `search_emails` - Search emails using field-based queries (text fields: from, to, subject, body; boolean: unread)
- `get_email` - Get full email details
- `get_email_body` - Get email body (automatically decodes base64)
- `get_email_headers` - Get email headers
- `get_email_source` - Get raw email source (suitable for saving as .eml file)

### Email Composition & Sending
- `create_draft` - Create a new draft email
- `update_draft` - Replace an existing draft (complete replacement via PUT)
- `send_email` - Send a new email directly
- `send_draft` - Send an existing draft
- `schedule_send_email` - Schedule an email to be sent at a specific time
- `schedule_send_draft` - Schedule an existing draft to be sent
- `cancel_scheduled_send` - Cancel a scheduled email send

### Email Management
- `delete_email` - Delete email (trash or permanent)
- `move_email` - Move email to another folder (**uses destinationFolderId**)
- `copy_email` - Copy email to another folder
- `update_email_flags` - Mark as read/unread, flagged/unflagged
- `mark_as_spam` - Mark email as spam (moves to spam folder)
- ~~`mark_as_not_spam`~~ - Not supported on ax.email

### Attachments & Folders
- `get_email_attachments` - List email attachments
- `list_folders` - List email folders with unread counts
- `create_folder` - Create new email folder
- `update_folder` - Rename/update folder (uses PATCH method)
- `delete_folder` - Delete empty folder
- `get_common_folder_ids` - Helper to get IDs for Inbox, Sent, Drafts, etc.

### Labels (Enhanced with Smart Workflows)
- `list_labels` - List all available labels
- `get_label` - Get details of a specific label
- `create_label` - Create a new label (returns new label ID)
- `update_label` - Update an existing label
- `delete_label` - Delete a label
- `add_label_to_email` - Add a label to an email (**enhanced with validation**)
- `remove_label_from_email` - Remove a label from an email (**idempotent**)
- `add_label_by_name` - 🆕 **Smart labeling** - add by name, auto-creates if missing
- `bulk_label_emails` - 🆕 **Bulk operations** - label multiple emails at once

### 🚀 **Bulk & Efficiency Operations**
- `bulk_get_emails` - 🆕 **Retrieve multiple emails** efficiently with configurable detail levels
- `batch_email_search` - 🆕 **Execute multiple search queries** in one operation

### 🔍 **Reliability & Validation Tools**
- `get_common_folder_ids` - **Enhanced discovery** with intelligent folder mapping
- `preview_folder_operation` - 🆕 **Dry-run mode** for folder operations
- `validate_operation_requirements` - 🆕 **Pre-validate** operation parameters

**🎯 Smart Workflows & Reliability Features:**
- **Auto-Discovery**: Folder/label IDs automatically discovered and validated
- **Intelligent Fallbacks**: Headers endpoint fallback to source extraction
- **Bulk Operations**: Efficient batch processing for multiple emails/searches
- **Idempotent Design**: All operations safe to repeat without errors
- **Dry-Run Mode**: Preview operations before execution
- **Enhanced Error Handling**: Actionable error messages with suggestions
- **Standardized Responses**: Consistent response format across all operations

## Installation

```bash
cd fastmcp-axigen-email
pip install -e .
```

## Configuration

Add to your MCP client configuration:

```json
{
  "mcp": {
    "servers": {
      "axigen-email": {
        "command": "python",
        "args": ["/path/to/fastmcp-axigen-email/server.py"]
      }
    }
  }
}
```

## Usage Examples

### Get Folder IDs First
```javascript
// Get common folder IDs to use with other operations
await use_tool("get_common_folder_ids", {
  email: "user@example.com",
  password: "password"
});
// Returns: { inbox: "39_39", sent: "39_40", drafts: "39_41", ... }
```

### List Recent Emails
```javascript
// List 20 most recent emails from Inbox
// Note: folder_id is REQUIRED on ax.email
await use_tool("list_emails", {
  email: "user@example.com",
  password: "password",
  folder_id: "39_39",  // Required! Use get_common_folder_ids to find this
  limit: 20
});
```

### Send an Email
```javascript
// Send a new email
await use_tool("send_email", {
  email: "user@example.com",
  password: "password",
  to: "recipient@example.com",
  subject: "Meeting Tomorrow",
  body_text: "Let's meet at 2 PM tomorrow."
});
```

### Manage Emails
```javascript
// Mark email as read
await use_tool("update_email_flags", {
  email: "user@example.com",
  password: "password",
  mail_id: "12345",
  is_unread: false
});

// Move to folder (note: uses folder_id parameter)
await use_tool("move_email", {
  email: "user@example.com",
  password: "password",
  mail_id: "12345",
  folder_id: "67890"  // This becomes destinationFolderId in the API
});
```

### Use Labels (Smart Workflows)
```javascript
// 🎯 RECOMMENDED: Smart labeling by name (auto-creates if missing)
await use_tool("add_label_by_name", {
  email: "user@example.com",
  password: "password",
  mail_id: "12345",
  label_name: "Important",
  create_if_missing: true  // Will create the label if it doesn't exist
});

// 🚀 Bulk labeling for multiple emails
await use_tool("bulk_label_emails", {
  email: "user@example.com",
  password: "password",
  mail_ids: ["12345", "12346", "12347"],
  label_name: "Project Alpha",
  create_if_missing: true
});

// Traditional workflow (if you need full control)
// 1. List available labels first
await use_tool("list_labels", {
  email: "user@example.com",
  password: "password"
});

// 2. Add label by ID
await use_tool("add_label_to_email", {
  email: "user@example.com",
  password: "password",
  mail_id: "12345",
  label_id: "label_123"  // Use ID from list_labels
});
```

### Schedule Emails
```javascript
// Schedule an email (delivery_time is unix timestamp)
const deliveryTime = Math.floor(Date.now() / 1000) + 3600; // 1 hour from now
await use_tool("schedule_send_email", {
  email: "user@example.com",
  password: "password",
  to: "recipient@example.com",
  subject: "Scheduled Message",
  body_text: "This will be sent later",
  delivery_time: deliveryTime
});

// Cancel scheduled send
await use_tool("cancel_scheduled_send", {
  email: "user@example.com",
  password: "password",
  mail_id: "scheduled_mail_id"
});
```

## Search Query Syntax

Search uses field-based queries with the following structure:
```javascript
search_criteria = [
  {"field": "fieldname", "value": "searchvalue"},
  {"field": "fieldname", "value": "searchvalue", "negate": true}  // NOT operator
]
```

### Working Search Fields on ax.email:
- **Text fields**: `from`, `to`, `subject`, `body` - Search for text in these fields
- **Boolean field**: `unread` - Use `"true"` or `"false"` as value

### Not Supported on ax.email:
- `flagged` - Returns 400 error
- `attachment` or `hasAttachment` - Returns 400 error

### Example Searches:
```javascript
// Unread emails from a specific sender
[
  {"field": "from", "value": "john@example.com"},
  {"field": "unread", "value": "true"}
]

// Emails with "meeting" in subject
[{"field": "subject", "value": "meeting"}]

// NOT from a specific domain
[{"field": "from", "value": "@spam.com", "negate": true}]
```

## Requirements

- Axigen server with **Mailbox REST API** enabled (Axigen X4 10.4+)
- Valid email account credentials
- Network access to Axigen server

## 🚀 Enhanced Reliability Features

### **Auto-Discovery & Validation**
- **Smart folder discovery**: `get_common_folder_ids` intelligently maps folder names with variations
- **ID validation**: All operations pre-validate mail_id/folder_id/label_id before execution
- **Auto-creation**: Labels can be created automatically when adding by name

### **Endpoint Resilience**
- **Intelligent fallbacks**: `get_email_headers` falls back to source extraction if headers endpoint fails
- **Error taxonomy**: 404/400 errors mapped to actionable guidance
- **Graceful degradation**: Operations continue with partial data when possible

### **Bulk Processing & Efficiency**
- **Concurrent processing**: `bulk_get_emails` processes multiple emails with configurable concurrency
- **Batch operations**: Execute multiple searches or label operations efficiently
- **Request optimization**: Minimize round-trips with intelligent batching

### **Developer Experience**
- **Dry-run mode**: Preview operations with `preview_folder_operation`
- **Requirement validation**: `validate_operation_requirements` checks prerequisites
- **Standardized responses**: Consistent error handling with suggestions
- **Idempotent operations**: Safe to repeat without side effects

## Important Notes for ax.email

When using with ax.email (the default server):
- ✅ **All 35 operations tested and working** with reliability enhancements
- ✅ **Auto-discovery handles folder/label ID resolution** automatically
- ✅ **Intelligent fallbacks** ensure operations succeed even with endpoint issues
- ✅ **Bulk operations** provide efficient processing for multiple items
- ⚠️ **Some endpoints may be unreliable** - fallbacks and validation handle this
- ⚠️ **Use validation tools** before batch operations for best results
- ❌ **Some advanced features** (undo send, temporary attachments) not available on ax.email

## 🏆 Performance & Reliability Notes

- **Server**: `https://ax.email` with full reliability enhancements
- **Authentication**: Session-based with automatic re-authentication
- **Limits**: 500 emails per request, 5 concurrent bulk operations by default
- **Error handling**: Comprehensive fallbacks and actionable error messages
- **Response format**: Standardized across all operations with metadata
- **Body handling**: Automatic base64 decoding and format detection
- **Validation**: Pre-operation validation prevents failed requests
- **For specialized operations**: Use respective servers (settings, filters, security)