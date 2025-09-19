# FastMCP Axigen Email Server

MCP server for Axigen email operations, providing comprehensive email management through the Axigen REST API.

✅ **UPDATE**: This server has been tested and **DOES work with ax.email**! The Mailbox API is available on ax.email with specific parameter requirements documented below.

## Features

This server provides 28 working tools for email operations on ax.email:

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

### Labels
- `list_labels` - List all available labels
- `get_label` - Get details of a specific label
- `create_label` - Create a new label
- `update_label` - Update an existing label
- `delete_label` - Delete a label
- `add_label_to_email` - Add a label to an email
- `remove_label_from_email` - Remove a label from an email

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

### Use Labels
```javascript
// List available labels
await use_tool("list_labels", {
  email: "user@example.com",
  password: "password"
});

// Create a new label
await use_tool("create_label", {
  email: "user@example.com",
  password: "password",
  name: "Important"
});

// Add label to email
await use_tool("add_label_to_email", {
  email: "user@example.com",
  password: "password",
  mail_id: "12345",
  label_id: "label_123"
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

## Important Notes for ax.email

When using with ax.email (the default server):
- ✅ **The Mailbox API IS available** on ax.email
- ✅ **Search works** with text fields (from, to, subject, body) and unread boolean
- ✅ **Copy email** works with `destinationFolderId`
- ✅ **Send operations** work for both new emails and drafts
- ✅ **Spam marking** works (moves to spam folder)
- ✅ **Update draft** works via PUT (complete replacement)
- ✅ **Folder update** works via PATCH method (rename folders)
- ✅ **Label operations** work with correct API parameters (no color support)
- ✅ **Scheduled send** works with correct endpoints and unix timestamps
- ⚠️ **folder_id is required** for `list_emails` - use `get_common_folder_ids` first
- ⚠️ **Move operations** use `destinationFolderId` internally (handled by the tool)
- ⚠️ **Email bodies** are base64-encoded (automatically decoded by the tool)
- ⚠️ **Scheduled send** requires unix timestamps, not ISO 8601 format
- ❌ **Unmark spam** doesn't work - move from spam folder instead
- ❌ **Flagged/attachment search** not supported
- ❌ **Undo send** not available
- ❌ **Temporary attachments** not available
- ❌ **Folder move** not available
- ❌ **Message parts** endpoints return unexpected format

## Notes

- Default server is `https://ax.email` which now works with proper parameters
- Supports session-based authentication with Basic Auth fallback
- Maximum email listing limit is 500 per request
- Email bodies are automatically decoded from base64
- For account settings, filters, and security operations, use the respective specialized servers