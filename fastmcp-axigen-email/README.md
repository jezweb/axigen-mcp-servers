# FastMCP Axigen Email Server

MCP server for Axigen email operations, providing comprehensive email management through the Axigen REST API.

✅ **UPDATE**: This server has been tested and **DOES work with ax.email**! The Mailbox API is available on ax.email with specific parameter requirements documented below.

## Features

This server provides 18 working tools for email operations on ax.email:

### Email Reading & Search
- `list_emails` - List emails with pagination and sorting (**requires folder_id**)
- `search_emails` - Search emails using field-based queries (text fields: from, to, subject, body; boolean: unread)
- `get_email` - Get full email details
- `get_email_body` - Get email body (automatically decodes base64)
- `get_email_headers` - Get email headers

### Email Composition & Sending
- `create_draft` - Create a new draft email
- `update_draft` - Replace an existing draft (complete replacement via PUT)
- `send_email` - Send a new email directly
- `send_draft` - Send an existing draft

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
- `get_common_folder_ids` - Helper to get IDs for Inbox, Sent, Drafts, etc.

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
- ⚠️ **folder_id is required** for `list_emails` - use `get_common_folder_ids` first
- ⚠️ **Move operations** use `destinationFolderId` internally (handled by the tool)
- ⚠️ **Email bodies** are base64-encoded (automatically decoded by the tool)
- ❌ **Unmark spam** doesn't work - move from spam folder instead
- ❌ **Flagged/attachment search** not supported
- ❌ **Scheduled send** operations not available
- ❌ **Undo send** not available
- ❌ **Temporary attachments** not available

## Notes

- Default server is `https://ax.email` which now works with proper parameters
- Supports session-based authentication with Basic Auth fallback
- Maximum email listing limit is 500 per request
- Email bodies are automatically decoded from base64
- For account settings, filters, and security operations, use the respective specialized servers