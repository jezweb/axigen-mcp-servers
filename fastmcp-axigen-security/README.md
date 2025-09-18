# FastMCP Axigen Security Server

MCP server for managing Axigen email account security settings including passwords, temporary aliases, and login limits.

## Features

### Password Management
- Change account password
- Generate secure passwords
- Validate password policy compliance

### Temporary Aliases
- Create disposable email aliases
- List active aliases
- Delete aliases when no longer needed

### Security Settings
- Configure login attempt limits
- Set account lockout policies
- Manage security preferences

## Installation

```bash
pip install -r requirements.txt
```

## Usage with FastMCP

```bash
fastmcp run server.py
```

## Available Tools

1. **change_password** - Change account password
2. **validate_password** - Check if password meets policy
3. **generate_secure_password** - Generate a secure password
4. **get_temporary_aliases** - List all temporary aliases
5. **create_temporary_alias** - Create a new temporary alias
6. **delete_temporary_alias** - Delete a temporary alias
7. **get_security_settings** - Get security configuration
8. **update_security_settings** - Update security settings
9. **get_login_limits** - Get login attempt limits

## Authentication

All tools require:
- `email`: Your Axigen email address
- `password`: Your current account password
- `server_url`: Axigen server URL (e.g., https://mail.example.com)

Sessions are cached for 30 minutes to improve performance.

## Password Policy

Default password requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Temporary Aliases

Temporary aliases are useful for:
- Online shopping and registrations
- Testing and development
- Avoiding spam on your main address

## Requirements

- Axigen X4 10.4 or later
- REST API enabled on server
- Valid user credentials