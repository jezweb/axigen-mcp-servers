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
- Anti-spam settings
- Bulk operations for filtering
- Domain blocking support

### 3. Security Server (`fastmcp-axigen-security`)
- Temporary email aliases
- Password management
- Security policies and quotas
- Account limits monitoring

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/jezweb/fastmcp-axigen.git
cd fastmcp-axigen
```

2. Install dependencies for each server:
```bash
cd fastmcp-axigen-settings
pip install -r requirements.txt
```

3. Run a server:
```bash
python server.py
```

## 💻 Usage

All servers follow the same authentication pattern - credentials are passed with each request:

```python
result = await get_account_settings(
    email="user@example.com",
    password="password123",
    server_url="https://mail.example.com"
)
```

## 🔒 Security

- No environment variables required
- Credentials passed per-request
- Session caching for performance
- Automatic re-authentication

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please ensure all tools follow the existing authentication pattern and return standardized responses.

## ⚡ Built With

- [FastMCP](https://github.com/jlowin/fastmcp)
- [Axigen Mail Server](https://www.axigen.com)

---

**Note:** These servers complement the existing [fastmcp-imap](https://github.com/jezweb/fastmcp-imap) server by providing functionality not available through IMAP protocol.