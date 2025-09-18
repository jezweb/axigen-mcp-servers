# Axigen MCP Servers - Development Scratchpad

## Current Status
- ✅ Three MCP servers working (settings, filters, security)
- ✅ Default server set to https://ax.email
- ✅ All Account API endpoints tested and working
- ✅ Documentation updated and accurate
- ✅ Email server created (but requires Mailbox API)
- ⚠️ ax.email only has Account API, not full Mailbox API

## API Endpoints Analysis

### Already Implemented (33 tools across 3 servers)
**Settings Server (13 tools):**
- Account info, settings, UI settings
- Signatures (CRUD)
- Contact info
- Vacation settings
- Account limits

**Filters Server (11 tools):**
- Spam settings
- Whitelist/Blacklist (CRUD, bulk operations)
- Filter info

**Security Server (9 tools):**
- Password management
- Temporary aliases (CRUD)
- Permanent aliases
- Security info

### To Be Implemented

#### 1. Email Operations (High Priority)
**Core Email:**
- `GET /api/v1/mails` - List emails
- `POST /api/v1/mails/search` - Search emails
- `GET /api/v1/mails/{mailId}` - Get email details
- `PATCH /api/v1/mails/{mailId}` - Update flags (read/unread/flagged)
- `DELETE /api/v1/mails/{mailId}` - Delete email
- `POST /api/v1/mails/{mailId}/move` - Move email
- `POST /api/v1/mails/{mailId}/copy` - Copy email

**Compose & Send:**
- `POST /api/v1/mails` - Create draft
- `PUT /api/v1/drafts/{mailId}` - Update draft
- `POST /api/v1/mails/send` - Send new email
- `POST /api/v1/drafts/{mailId}/send` - Send draft
- `POST /api/v1/mails/send/undo` - Undo send
- `POST /api/v1/mails/send/scheduled` - Schedule send

**Attachments:**
- `GET /api/v1/mails/{mailId}/attachments` - List attachments
- `GET /api/v1/mails/{mailId}/attachments/{partId}` - Download attachment
- `POST /api/v1/temporaryattachments` - Upload temp attachment
- `DELETE /api/v1/temporaryattachments/{id}` - Delete temp attachment

**Email Content:**
- `GET /api/v1/mails/{mailId}/body` - Get email body
- `GET /api/v1/mails/{mailId}/source` - Get raw source
- `GET /api/v1/mails/{mailId}/headers` - Get headers

**Labels & Spam:**
- `POST /api/v1/mails/{mailId}/labels/add` - Add label
- `POST /api/v1/mails/{mailId}/labels/remove` - Remove label
- `POST /api/v1/mails/{mailId}/spam` - Mark as spam
- `POST /api/v1/mails/{mailId}/notspam` - Mark as not spam

#### 2. Folder Operations
- `GET /api/v1/folders` - List folders
- `POST /api/v1/folders` - Create folder
- `PATCH /api/v1/folders/{folderId}` - Update folder
- `DELETE /api/v1/folders/{folderId}` - Delete folder
- `POST /api/v1/folders/{folderId}/move` - Move folder
- `GET /api/v1/folders/delta` - Get folder changes

#### 3. Contact Operations
- `GET /api/v1/contacts` - List contacts
- `GET /api/v1/contacts/autocomplete` - Autocomplete for email
- `GET /api/v1/contacts/avatars` - Get avatars
- `GET /api/v1/contacts/delta` - Get contact changes

#### 4. Additional Features
- `GET /api/v1/mails/counters` - Get unread counts
- `GET /api/v1/conversations` - List conversations
- `POST /api/v1/batch` - Batch operations

## Server Organization Plan

### New: `fastmcp-axigen-email` (Primary email operations)
- List, search, read emails
- Send, reply, forward
- Drafts management
- Attachments
- Move, delete, flag operations
- Labels and spam marking

### New: `fastmcp-axigen-folders` (Folder management)
- CRUD operations for folders
- Folder organization

### New: `fastmcp-axigen-contacts` (Contact management)
- List and search contacts
- Autocomplete for composition

### Existing servers remain as-is
- Settings, Filters, Security servers already comprehensive

## Technical Notes
- All endpoints use `/api/v1/` prefix
- Account API uses Basic Auth directly on each request
- Mailbox API requires login first, then session-based auth
- Default server: https://ax.email (Account API only)
- Test account: jeremy@jezweb.org / Demo7-Email

## Important Discovery
The ax.email server only implements the Account API endpoints (/api/v1/account/*), not the full Mailbox API (/api/v1/mails, /api/v1/folders, etc).

The Mailbox API requires:
1. POST /api/v1/login with Basic Auth to get session ID
2. Use X-Axigen-Session header for subsequent requests
3. Access to mail, folder, contact endpoints

This means the email server we created will only work with Axigen installations that have the full Mailbox API enabled, not with ax.email.

## Completed
1. ✅ Created fastmcp-axigen-email server with 16 tools
2. ✅ Documented all capabilities
3. ✅ Updated main README with server information
4. ✅ Identified API limitations of ax.email

## Summary
We now have 4 MCP servers with 49 total tools:
- Settings: 13 tools (working with ax.email)
- Filters: 11 tools (working with ax.email)
- Security: 9 tools (working with ax.email)
- Email: 16 tools (requires full Mailbox API, not available on ax.email)