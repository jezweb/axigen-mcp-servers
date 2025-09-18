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

1. **get_security_info** - Get comprehensive security information
2. **get_temporary_aliases** - List all temporary email aliases
3. **create_temporary_alias** - Create a new temporary alias
4. **delete_temporary_alias** - Delete a temporary alias
5. **cleanup_expired_aliases** - Remove expired temporary aliases
6. **get_permanent_aliases** - List permanent account aliases
7. **change_password** - Change account password
8. **get_password_policy** - Get password policy requirements
9. **get_account_limits** - Get account quotas and limits

## Authentication

All tools require:
- `email`: Your Axigen email address
- `password`: Your current account password
- `server_url`: Axigen server URL (optional, defaults to https://ax.email)

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