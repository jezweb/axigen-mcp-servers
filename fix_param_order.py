#!/usr/bin/env python3
"""
Fix parameter order for functions with server_url defaults
Move server_url to the end when there are required parameters after it
"""

import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        # Find function definitions with server_url followed by other parameters
        if 'server_url: str,' in lines[i]:
            # Find the function start
            func_start = i
            while func_start > 0 and '@mcp.tool()' not in lines[func_start]:
                func_start -= 1

            # Find the function end (closing parenthesis)
            func_end = i
            while func_end < len(lines) and ') -> Dict[str, Any]:' not in lines[func_end]:
                func_end += 1

            if func_end < len(lines):
                # Extract function lines
                func_lines = lines[func_start:func_end+1]

                # Check if this needs fixing (has required params after server_url)
                has_required_after = False
                for j in range(i - func_start + 1, len(func_lines)):
                    line = func_lines[j]
                    if ') -> Dict[str, Any]:' in line:
                        break
                    # Check if it's a required parameter (no = sign)
                    if ': str' in line and '=' not in line and 'Optional' not in line:
                        has_required_after = True
                        break
                    if ': int' in line and '=' not in line and 'Optional' not in line:
                        has_required_after = True
                        break
                    if ': bool' in line and '=' not in line and 'Optional' not in line:
                        has_required_after = True
                        break
                    if ': Dict' in line and '=' not in line and 'Optional' not in line:
                        has_required_after = True
                        break
                    if ': List' in line and '=' not in line and 'Optional' not in line:
                        has_required_after = True
                        break

                if has_required_after:
                    # Remove server_url line
                    server_line = lines[i]
                    del lines[i]

                    # Find where to insert it (before the closing parenthesis)
                    insert_pos = i
                    while insert_pos < len(lines) and ') -> Dict[str, Any]:' not in lines[insert_pos]:
                        insert_pos += 1

                    # Modify the server_url line to have default value and proper comma
                    server_line = server_line.replace('server_url: str,', 'server_url: str = "https://ax.email"')

                    # Fix the comma on the previous parameter
                    if insert_pos > 0:
                        prev_line = lines[insert_pos - 1]
                        if not prev_line.rstrip().endswith(','):
                            lines[insert_pos - 1] = prev_line.rstrip() + ',\n'

                    # Insert server_url line before closing parenthesis
                    lines.insert(insert_pos, server_line)

                    print(f"Fixed function at line {func_start} in {filepath}")

        i += 1

    with open(filepath, 'w') as f:
        f.writelines(lines)

# Fix all server files
servers = [
    'fastmcp-axigen-settings/server.py',
    'fastmcp-axigen-filters/server.py',
    'fastmcp-axigen-security/server.py'
]

for server in servers:
    print(f"\nProcessing {server}...")
    fix_file(server)

print("\nAll functions fixed!")