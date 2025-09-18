# FastMCP Axigen Email Server

MCP server for Axigen email operations, providing comprehensive email management through the Axigen REST API.

## Features

This server provides 16 tools for email operations:

### Email Reading & Search
- `list_emails` - List emails with pagination and sorting
- `search_emails` - Search emails using Axigen search syntax
- `get_email` - Get full email details
- `get_email_body` - Get email body in text/HTML format
- `get_email_headers` - Get email headers

### Email Composition & Sending
- `create_draft` - Create a new draft email
- `update_draft` - Update an existing draft
- `send_email` - Send a new email directly
- `send_draft` - Send an existing draft

### Email Management
- `delete_email` - Delete email (trash or permanent)
- `move_email` - Move email to another folder
- `update_email_flags` - Mark as read/unread, flagged/unflagged
- `mark_as_spam` - Mark email as spam
- `mark_as_not_spam` - Mark email as not spam

### Attachments & Folders
- `list_attachments` - List email attachments
- `list_folders` - List email folders with unread counts

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

### List Recent Emails
```javascript
// List 20 most recent emails
await use_tool("list_emails", {
  email: "user@example.com",
  password: "password",
  limit: 20
});
```

### Search Emails
```javascript
// Search for emails from a specific sender
await use_tool("search_emails", {
  email: "user@example.com",
  password: "password",
  query: "from:john@example.com"
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

// Move to folder
await use_tool("move_email", {
  email: "user@example.com",
  password: "password",
  mail_id: "12345",
  folder_id: "67890"
});
```

## Search Query Syntax

The search tool supports various query operators:
- `from:email` - Search by sender
- `to:email` - Search by recipient
- `subject:text` - Search in subject
- `body:text` - Search in body
- `has:attachment` - Emails with attachments
- `is:unread` - Unread emails
- `is:flagged` - Flagged emails

## Requirements

- Axigen server with REST API enabled (Axigen X4 10.4+)
- Valid email account credentials
- Network access to Axigen server (default: https://ax.email)

## Notes

- All tools use `https://ax.email` as the default server
- The server URL can be overridden in each tool call
- Supports session-based authentication with Basic Auth
- Maximum email listing limit is 500 per request