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

1. **get_spam_settings** - Get anti-spam (AVAS) filter settings
2. **update_spam_settings** - Update anti-spam filter settings
3. **get_whitelist** - List all whitelisted addresses
4. **add_to_whitelist** - Add an address to whitelist
5. **remove_from_whitelist** - Remove address from whitelist
6. **get_blacklist** - List all blacklisted addresses/domains
7. **add_to_blacklist** - Add address or @domain to blacklist
8. **remove_from_blacklist** - Remove from blacklist
9. **bulk_update_whitelist** - Add/remove multiple whitelist entries
10. **bulk_update_blacklist** - Add/remove multiple blacklist entries
11. **get_filter_info** - Get comprehensive filter information

## Authentication

All tools require:
- `email`: Your Axigen email address
- `password`: Your account password
- `server_url`: Axigen server URL (optional, defaults to https://ax.email)

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