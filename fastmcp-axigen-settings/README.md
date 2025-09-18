# FastMCP Axigen Settings Server

MCP server for managing Axigen email account settings including signatures, vacation messages, UI preferences, and contact information.

## Features

### Signature Management
- Get/update primary signatures (plain text and HTML)
- Get/update reply signatures
- Manage signature settings and selection

### Vacation/Out-of-Office
- Enable/disable vacation messages
- Set vacation period with start/end dates
- Configure auto-response messages

### UI Preferences
- Customize interface settings (theme, layout, language)
- Set timezone and date formats
- Configure inbox preferences

### Contact Information
- Update personal details
- Manage contact information

## Installation

```bash
pip install -r requirements.txt
```

## Usage with FastMCP

```bash
fastmcp run server.py
```

## Available Tools

1. **get_account_settings** - Get account preferences (theme, language, timezone, etc.)
2. **update_account_settings** - Update account preferences
3. **get_signatures** - List all email signatures
4. **create_signature** - Create a new signature
5. **update_signature** - Update an existing signature
6. **delete_signature** - Delete a signature
7. **get_vacation_settings** - Get vacation/out-of-office settings
8. **set_vacation_reply** - Configure vacation auto-reply
9. **get_contact_info** - Get user contact information
10. **update_contact_info** - Update user contact information
11. **get_ui_settings** - Get WebMail UI settings (JSON storage)
12. **save_ui_settings** - Save WebMail UI settings
13. **get_account_info** - Get comprehensive account information

## Authentication

All tools require:
- `email`: Your Axigen email address
- `password`: Your account password
- `server_url`: Axigen server URL (optional, defaults to https://ax.email)

Sessions are cached for 30 minutes to improve performance.

## Requirements

- Axigen X4 10.4 or later
- REST API enabled on server
- Valid user credentials