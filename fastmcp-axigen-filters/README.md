# FastMCP Axigen Filters Server

MCP server for managing Axigen email filters including whitelist/blacklist management and domain blocking.

## Features

### Whitelist Management
- Add/remove trusted email addresses
- Bulk operations for multiple addresses
- List all whitelisted contacts

### Blacklist Management
- Block unwanted senders
- Support for domain blocking (@domain.com)
- Bulk add/remove operations
- List all blocked addresses

### Filter Management
- Get current filter configuration
- Clear all filters at once

## Installation

```bash
pip install -r requirements.txt
```

## Usage with FastMCP

```bash
fastmcp run server.py
```

## Available Tools

1. **get_filters** - Get all filter settings
2. **get_whitelist** - List whitelisted addresses
3. **add_to_whitelist** - Add address to whitelist
4. **remove_from_whitelist** - Remove from whitelist
5. **bulk_add_whitelist** - Add multiple addresses to whitelist
6. **get_blacklist** - List blacklisted addresses
7. **add_to_blacklist** - Add address/domain to blacklist
8. **remove_from_blacklist** - Remove from blacklist
9. **bulk_add_blacklist** - Add multiple addresses to blacklist
10. **bulk_remove_blacklist** - Remove multiple from blacklist
11. **clear_all_filters** - Clear all whitelist and blacklist entries

## Authentication

All tools require:
- `email`: Your Axigen email address
- `password`: Your account password
- `server_url`: Axigen server URL (e.g., https://mail.example.com)

Sessions are cached for 30 minutes to improve performance.

## Domain Blocking

To block entire domains, use the @domain.com format:
```
@spam-domain.com
@unwanted.org
```

## Requirements

- Axigen X4 10.4 or later
- REST API enabled on server
- Valid user credentials