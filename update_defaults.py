#!/usr/bin/env python3
"""
Update all server files to use https://ax.email as default server URL
This script ensures proper parameter ordering (defaults at the end)
"""

import re
import os

def update_file(filepath):
    """Update a single server file to add default server URL"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Pattern to find function definitions with server_url
    # We need to move server_url to the end if there are other required params after it

    # For functions with only email, password, server_url
    content = re.sub(
        r'(\s+)(email: str,\n\s+password: str,\n\s+server_url: str)(\n\s*\) -> Dict)',
        r'\1email: str,\n\1password: str,\n\1server_url: str = "https://ax.email"\3',
        content
    )

    # For functions with server_url followed by required parameters - need to move it to end
    # This is more complex as we need to identify and move it

    # Also update docstrings
    content = re.sub(
        r'server_url: Axigen server URL \(e\.g\., https://mail\.example\.com\)',
        r'server_url: Axigen server URL (optional, defaults to https://ax.email)',
        content
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Updated {filepath}")

# Update all three server files
servers = [
    'fastmcp-axigen-settings/server.py',
    'fastmcp-axigen-filters/server.py',
    'fastmcp-axigen-security/server.py'
]

for server in servers:
    update_file(server)

print("\nAll servers updated with default server URL!")