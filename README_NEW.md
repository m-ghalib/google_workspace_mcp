<div align="center">

# Google Workspace MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/workspace-mcp.svg)](https://pypi.org/project/workspace-mcp/)

**Complete Google Workspace control through natural language.** Gmail, Calendar, Docs, Sheets, and Slides—all via MCP.

[Quick Start](#-quick-start) • [Tools Reference](#-tools-reference) • [Configuration](#-configuration) • [OAuth Setup](#-oauth-setup)

</div>

---

## ⚡ Quick Start

### One-Click Install (Claude Desktop)

1. Download `google_workspace_mcp.dxt` from [Releases](https://github.com/taylorwilsdon/google_workspace_mcp/releases)
2. Double-click → Claude Desktop installs automatically
3. Add your Google OAuth credentials in Settings → Extensions

### CLI Install

```bash
# Instant run (no install)
uvx workspace-mcp

# With specific tools only
uvx workspace-mcp --tools gmail calendar docs

# With tool tier
uvx workspace-mcp --tool-tier core
```

### Environment Variables

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
export OAUTHLIB_INSECURE_TRANSPORT=1  # Development only
```

---

## 🛠 Tools Reference

### Gmail (13 tools)

| Tool | Tier | Description |
|------|------|-------------|
| `search_gmail_messages` | Core | Search with Gmail operators, returns message/thread IDs with web links |
| `get_gmail_message_content` | Core | Get message(s): subject, sender, body, attachments. Accepts single ID or list |
| `send_gmail_message` | Core | Send emails with HTML support, CC/BCC, threading |
| `get_gmail_thread_content` | Extended | Get conversation thread(s). Accepts single ID or list |
| `draft_gmail_message` | Extended | Create drafts with threading support |
| `list_gmail_labels` | Extended | List all system and user labels |
| `manage_gmail_label` | Extended | Create, update, delete labels |
| `modify_gmail_message_labels` | Extended | Add/remove labels (archive, trash, etc.). Accepts single ID or list |

**Also includes:** `get_gmail_attachment_content`, `list_gmail_filters`, `create_gmail_filter`, `delete_gmail_filter`, `start_google_auth`

### Google Calendar (5 tools)

| Tool | Tier | Description |
|------|------|-------------|
| `list_calendars` | Core | List all accessible calendars |
| `get_events` | Core | Query events by time range, search, or specific ID |
| `create_event` | Core | Create events with attendees, reminders, Google Meet, attachments |
| `modify_event` | Core | Update any event property including conferencing |
| `delete_event` | Extended | Remove events |

**Event features:** Timezone support, transparency (busy/free), visibility settings, up to 5 custom reminders

### Google Docs (10 tools)

| Tool | Tier | Description |
|------|------|-------------|
| `get_doc_content` | Core | Extract text from native Google Docs (supports tabs) |
| `create_doc` | Core | Create new documents with optional initial content |
| `modify_doc_text` | Core | Insert, replace, format text (bold, italic, colors, fonts) |
| `find_and_replace_doc` | Extended | Global find/replace with case matching |
| `insert_doc_elements` | Extended | Add tables, lists, page breaks |
| `insert_doc_image` | Complete | Insert images from URLs |
| `update_doc_headers_footers` | Complete | Modify headers/footers |
| `batch_update_doc` | Complete | Execute multiple operations atomically |
| `inspect_doc_structure` | Complete | Analyze document structure for safe insertion points |
| `create_table_with_data` | Complete | Create and populate tables in one operation |
| `debug_table_structure` | Complete | Debug table cell positions and content |

### Google Sheets (13 tools)

| Tool | Tier | Description |
|------|------|-------------|
| `read_sheet_values` | Core | Read cell ranges with formatted output |
| `modify_sheet_values` | Core | Write, update, or clear cell values |
| `create_spreadsheet` | Core | Create new spreadsheets with multiple sheets |
| `get_spreadsheet_info` | Extended | Get metadata, sheets, conditional formats |
| `create_sheet` | Complete | Add sheets to existing spreadsheets |
| `format_sheet_range` | Complete | Apply colors and number formats |
| `add_conditional_formatting` | Complete | Add boolean or gradient rules |
| `update_conditional_formatting` | Complete | Modify existing rules |
| `delete_conditional_formatting` | Complete | Remove formatting rules |

### Google Slides (5 tools)

| Tool | Tier | Description |
|------|------|-------------|
| `create_presentation` | Core | Create new presentations |
| `get_presentation` | Core | Get presentation details with slide text extraction |
| `batch_update_presentation` | Extended | Apply multiple updates (create slides, shapes, etc.) |
| `get_page` | Extended | Get specific slide details and elements |
| `get_page_thumbnail` | Extended | Generate PNG thumbnails |

---

## 📊 Tool Tiers

Choose a tier based on your needs:

| Tier | Tools | Use Case |
|------|-------|----------|
| **Core** | ~30 | Essential operations: search, read, create, send |
| **Extended** | ~50 | Core + management: labels, folders, batch ops |
| **Complete** | ~80 | Full API: comments, headers, admin functions |

```bash
uvx workspace-mcp --tool-tier core      # Start minimal
uvx workspace-mcp --tool-tier extended  # Add management
uvx workspace-mcp --tool-tier complete  # Everything
```

Mix tiers with specific services:
```bash
uvx workspace-mcp --tools gmail docs --tool-tier extended
```

---

## ⚙ Configuration

### Required

| Variable | Description |
|----------|-------------|
| `GOOGLE_OAUTH_CLIENT_ID` | OAuth client ID from Google Cloud |
| `GOOGLE_OAUTH_CLIENT_SECRET` | OAuth client secret |

### Optional

| Variable | Description |
|----------|-------------|
| `USER_GOOGLE_EMAIL` | Default email for single-user mode |
| `MCP_ENABLE_OAUTH21` | Enable OAuth 2.1 multi-user support |
| `WORKSPACE_MCP_STATELESS_MODE` | No file writes (container-friendly) |
| `EXTERNAL_OAUTH21_PROVIDER` | External OAuth flow with bearer tokens |
| `WORKSPACE_MCP_BASE_URI` | Server base URL (default: `http://localhost`) |
| `WORKSPACE_MCP_PORT` | Server port (default: `8000`) |
| `WORKSPACE_EXTERNAL_URL` | External URL for reverse proxy setups |
| `GOOGLE_MCP_CREDENTIALS_DIR` | Custom credentials storage path |

---

## 🔐 OAuth Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Navigate to **APIs & Services → Credentials**
4. Click **Create Credentials → OAuth Client ID**
5. Select **Desktop Application**
6. Download credentials

### 2. Enable APIs

Click to enable each API:

- [Calendar](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
- [Gmail](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com)
- [Docs](https://console.cloud.google.com/flows/enableapi?apiid=docs.googleapis.com)
- [Sheets](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
- [Slides](https://console.cloud.google.com/flows/enableapi?apiid=slides.googleapis.com)

### 3. First Authentication

When you first call a tool:
1. Server returns an authorization URL
2. Open URL in browser, authorize access
3. Paste the authorization code when prompted
4. Credentials are cached for future use

---

## 🚀 Transport Modes

### Stdio (Default)

Best for Claude Desktop and local MCP clients:

```bash
uvx workspace-mcp
```

### HTTP (Streamable)

For web interfaces, debugging, or multi-client setups:

```bash
uvx workspace-mcp --transport streamable-http
```

Access at `http://localhost:8000/mcp/`

### Docker

```bash
docker build -t workspace-mcp .
docker run -p 8000:8000 \
  -e GOOGLE_OAUTH_CLIENT_ID="..." \
  -e GOOGLE_OAUTH_CLIENT_SECRET="..." \
  workspace-mcp --transport streamable-http
```

---

## 🔧 Client Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tool-tier", "core"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-secret",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    }
  }
}
```

### LM Studio

```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uvx",
      "args": ["workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-secret",
        "OAUTHLIB_INSECURE_TRANSPORT": "1",
        "USER_GOOGLE_EMAIL": "you@example.com"
      }
    }
  }
}
```

### VS Code

```json
{
  "servers": {
    "google-workspace": {
      "url": "http://localhost:8000/mcp/",
      "type": "http"
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http workspace-mcp http://localhost:8000/mcp
```

---

## 🏗 Architecture

```
google_workspace_mcp/
├── auth/                 # OAuth 2.0/2.1, credential storage, decorators
├── core/                 # MCP server, tool registry, utilities
├── gcalendar/           # Calendar tools
├── gdocs/               # Docs tools + managers (tables, headers, batch)
├── gmail/               # Gmail tools
├── gsheets/             # Sheets tools + helpers
├── gslides/             # Slides tools
└── main.py              # Entry point
```

### Key Patterns

**Service Decorator:** All tools use `@require_google_service()` for automatic authentication with 30-minute service caching.

```python
@server.tool()
@require_google_service("gmail", "gmail_read")
async def search_gmail_messages(service, user_google_email: str, query: str):
    # service is injected automatically
    ...
```

---

## 🧪 Development

```bash
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
cd google_workspace_mcp

# Install with dev dependencies
uv sync --group dev

# Run locally
uv run main.py

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**[Documentation](https://workspacemcp.com)** • **[Issues](https://github.com/taylorwilsdon/google_workspace_mcp/issues)** • **[PyPI](https://pypi.org/project/workspace-mcp/)**

</div>
