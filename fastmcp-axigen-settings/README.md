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

1. **get_signature** - Get primary signature
2. **update_signature** - Update primary signature
3. **get_reply_signature** - Get reply signature
4. **update_reply_signature** - Update reply signature
5. **get_vacation_settings** - Get vacation/out-of-office settings
6. **update_vacation_settings** - Update vacation settings
7. **enable_vacation** - Enable vacation auto-responder
8. **disable_vacation** - Disable vacation auto-responder
9. **get_ui_settings** - Get UI preferences
10. **update_ui_settings** - Update UI preferences
11. **get_user_info** - Get user contact information
12. **update_user_info** - Update user contact information
13. **get_all_settings** - Get all settings at once

## Authentication

All tools require:
- `email`: Your Axigen email address
- `password`: Your account password
- `server_url`: Axigen server URL (e.g., https://mail.example.com)

Sessions are cached for 30 minutes to improve performance.

## Requirements

- Axigen X4 10.4 or later
- REST API enabled on server
- Valid user credentials