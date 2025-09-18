# Axigen MCP Servers

FastMCP servers for managing Axigen email accounts via REST API - providing settings management, email filtering, and security features not available through IMAP.

## 📦 Servers Included

### 1. Settings Server (`fastmcp-axigen-settings`)
- **13 tools** for account configuration
- Account preferences (language, timezone, themes)
- Email signatures management (CRUD operations)
- Vacation/auto-reply configuration
- Contact information and avatar management
- UI settings customization

### 2. Filters Server (`fastmcp-axigen-filters`)
- **11 tools** for spam and filter management
- Whitelist/blacklist management
- Anti-spam settings (AVAS)
- Bulk operations for filtering
- Domain blocking support (@domain.com)
- Filter presets and configurations

### 3. Security Server (`fastmcp-axigen-security`)
- **9 tools** for security management
- Temporary email aliases (create, delete, list)
- Password management and policies
- Security policies and quotas
- Account limits monitoring
- Permanent aliases listing

### 4. Email Server (`fastmcp-axigen-email`) - *Experimental*
- **16 tools** for email operations (when Mailbox API is available)
- List, search, and read emails
- Send, reply, forward functionality
- Draft management
- Move, delete, flag operations
- Attachment handling
- Folder management
- **Note**: Requires Axigen server with full Mailbox API enabled (not available on all servers)

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/jezweb/axigen-mcp-servers.git
cd axigen-mcp-servers
```

2. Install dependencies for each server:
```bash
cd fastmcp-axigen-settings
pip install -r requirements.txt
```

3. Run a server with FastMCP:
```bash
fastmcp run server.py
```

## 💻 Usage

All servers follow the same authentication pattern - credentials are passed with each request:

```python
# Using default server (https://ax.email)
result = await get_account_settings(
    email="user@example.com",
    password="password123"
)

# Or specify a custom server
result = await get_account_settings(
    email="user@example.com",
    password="password123",
    server_url="https://mail.yourdomain.com"
)
```

## 🔒 Security

- No environment variables required
- Credentials passed per-request
- Session caching for performance
- Automatic re-authentication

## 📋 Requirements

- Axigen X4 10.4 or later with REST API enabled
  - Account API endpoints (required for Settings, Filters, Security servers)
  - Mailbox API endpoints (optional, required for Email server functionality)
- Python 3.8+
- Valid Axigen user account credentials

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please ensure all tools follow the existing authentication pattern and return standardized responses.

## ⚡ Built With

- [FastMCP](https://github.com/jlowin/fastmcp)
- [Axigen Mail Server](https://www.axigen.com) - Mailbox REST API

## 🧪 Testing

The servers have been tested and confirmed working with:
- Server: `https://ax.email`
- Axigen Mailbox REST API v1

---

**Note:** These servers complement existing email tools by providing Axigen-specific functionality not available through standard protocols like IMAP.