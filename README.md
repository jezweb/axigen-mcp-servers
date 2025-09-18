# Axigen MCP Servers

FastMCP servers for managing Axigen email accounts via REST API - providing settings management, email filtering, and security features not available through IMAP.

## 📦 Servers Included

### 1. Settings Server (`fastmcp-axigen-settings`)
- Account preferences (language, timezone, themes)
- Email signatures management
- Vacation/auto-reply configuration
- Contact information and avatar management

### 2. Filters Server (`fastmcp-axigen-filters`)
- Whitelist/blacklist management
- Anti-spam settings (AVAS)
- Bulk operations for filtering
- Domain blocking support (@domain.com)

### 3. Security Server (`fastmcp-axigen-security`)
- Temporary email aliases
- Password management
- Security policies and quotas
- Account limits monitoring

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
# Example with working test server
result = await get_account_settings(
    email="user@example.com",
    password="password123",
    server_url="https://ax.email"  # or your Axigen server
)
```

## 🔒 Security

- No environment variables required
- Credentials passed per-request
- Session caching for performance
- Automatic re-authentication

## 📋 Requirements

- Axigen X4 10.4 or later with Mailbox REST API enabled
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