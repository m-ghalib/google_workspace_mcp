"""
Google Workspace OAuth Scopes

This module centralizes OAuth scope definitions for Google Workspace integration.
Separated from service_decorator.py to avoid circular imports.
"""

import logging

logger = logging.getLogger(__name__)

# Global variable to store enabled tools (set by main.py)
_ENABLED_TOOLS = None

# Individual OAuth Scope Constants
USERINFO_EMAIL_SCOPE = "https://www.googleapis.com/auth/userinfo.email"
USERINFO_PROFILE_SCOPE = "https://www.googleapis.com/auth/userinfo.profile"
OPENID_SCOPE = "openid"
CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar"
CALENDAR_READONLY_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"
CALENDAR_EVENTS_SCOPE = "https://www.googleapis.com/auth/calendar.events"

# Google Docs scopes
DOCS_READONLY_SCOPE = "https://www.googleapis.com/auth/documents.readonly"
DOCS_WRITE_SCOPE = "https://www.googleapis.com/auth/documents"

# Gmail API scopes
GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
GMAIL_COMPOSE_SCOPE = "https://www.googleapis.com/auth/gmail.compose"
GMAIL_MODIFY_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
GMAIL_LABELS_SCOPE = "https://www.googleapis.com/auth/gmail.labels"
GMAIL_SETTINGS_BASIC_SCOPE = "https://www.googleapis.com/auth/gmail.settings.basic"

# Google Sheets API scopes
SHEETS_READONLY_SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"
SHEETS_WRITE_SCOPE = "https://www.googleapis.com/auth/spreadsheets"

# Google Slides API scopes
SLIDES_SCOPE = "https://www.googleapis.com/auth/presentations"
SLIDES_READONLY_SCOPE = "https://www.googleapis.com/auth/presentations.readonly"

# Apps Script API scopes
SCRIPT_PROJECTS_SCOPE = "https://www.googleapis.com/auth/script.projects"
SCRIPT_EXTERNAL_REQUEST_SCOPE = "https://www.googleapis.com/auth/script.external_request"

# Base OAuth scopes required for user identification
BASE_SCOPES = [USERINFO_EMAIL_SCOPE, USERINFO_PROFILE_SCOPE, OPENID_SCOPE]

# Service-specific scope groups
DOCS_SCOPES = [DOCS_READONLY_SCOPE, DOCS_WRITE_SCOPE, SCRIPT_PROJECTS_SCOPE, SCRIPT_EXTERNAL_REQUEST_SCOPE]

CALENDAR_SCOPES = [CALENDAR_SCOPE, CALENDAR_READONLY_SCOPE, CALENDAR_EVENTS_SCOPE]

GMAIL_SCOPES = [
    GMAIL_READONLY_SCOPE,
    GMAIL_SEND_SCOPE,
    GMAIL_COMPOSE_SCOPE,
    GMAIL_MODIFY_SCOPE,
    GMAIL_LABELS_SCOPE,
    GMAIL_SETTINGS_BASIC_SCOPE,
]

SHEETS_SCOPES = [SHEETS_READONLY_SCOPE, SHEETS_WRITE_SCOPE]

SLIDES_SCOPES = [SLIDES_SCOPE, SLIDES_READONLY_SCOPE]

SCRIPT_SCOPES = [SCRIPT_PROJECTS_SCOPE, SCRIPT_EXTERNAL_REQUEST_SCOPE]

# Tool-to-scopes mapping
TOOL_SCOPES_MAP = {
    "gmail": GMAIL_SCOPES,
    "calendar": CALENDAR_SCOPES,
    "docs": DOCS_SCOPES,
    "sheets": SHEETS_SCOPES,
    "slides": SLIDES_SCOPES,
}

# Tool-to-read-only-scopes mapping
TOOL_READONLY_SCOPES_MAP = {
    "gmail": [GMAIL_READONLY_SCOPE],
    "calendar": [CALENDAR_READONLY_SCOPE],
    "docs": [DOCS_READONLY_SCOPE],
    "sheets": [SHEETS_READONLY_SCOPE],
    "slides": [SLIDES_READONLY_SCOPE],
}


def set_enabled_tools(enabled_tools):
    """
    Set the globally enabled tools list.

    Args:
        enabled_tools: List of enabled tool names.
    """
    global _ENABLED_TOOLS
    _ENABLED_TOOLS = enabled_tools
    logger.info(f"Enabled tools set for scope management: {enabled_tools}")


# Global variable to store read-only mode (set by main.py)
_READ_ONLY_MODE = False


def set_read_only(enabled: bool):
    """
    Set the global read-only mode.

    Args:
        enabled: Boolean indicating if read-only mode should be enabled.
    """
    global _READ_ONLY_MODE
    _READ_ONLY_MODE = enabled
    logger.info(f"Read-only mode set to: {enabled}")


def is_read_only_mode() -> bool:
    """Check if read-only mode is enabled."""
    return _READ_ONLY_MODE


def get_all_read_only_scopes() -> list[str]:
    """Get all possible read-only scopes across all tools."""
    all_scopes = set(BASE_SCOPES)
    for scopes in TOOL_READONLY_SCOPES_MAP.values():
        all_scopes.update(scopes)
    return list(all_scopes)


def get_current_scopes():
    """
    Returns scopes for currently enabled tools.
    Uses globally set enabled tools or all tools if not set.

    .. deprecated::
        This function is a thin wrapper around get_scopes_for_tools() and exists
        for backwards compatibility. Prefer using get_scopes_for_tools() directly
        for new code, which allows explicit control over the tool list parameter.

    Returns:
        List of unique scopes for the enabled tools plus base scopes.
    """
    return get_scopes_for_tools(_ENABLED_TOOLS)


def get_scopes_for_tools(enabled_tools=None):
    """
    Returns scopes for enabled tools only.

    Args:
        enabled_tools: List of enabled tool names. If None, returns all scopes.

    Returns:
        List of unique scopes for the enabled tools plus base scopes.
    """
    if enabled_tools is None:
        # Default behavior - return all scopes
        enabled_tools = TOOL_SCOPES_MAP.keys()

    # Start with base scopes (always required)
    scopes = BASE_SCOPES.copy()

    # Determine which map to use based on read-only mode
    scope_map = TOOL_READONLY_SCOPES_MAP if _READ_ONLY_MODE else TOOL_SCOPES_MAP
    mode_str = "read-only" if _READ_ONLY_MODE else "full"

    # Add scopes for each enabled tool
    for tool in enabled_tools:
        if tool in scope_map:
            scopes.extend(scope_map[tool])

    logger.debug(
        f"Generated {mode_str} scopes for tools {list(enabled_tools)}: {len(set(scopes))} unique scopes"
    )
    # Return unique scopes
    return list(set(scopes))


# Combined scopes for all supported Google Workspace operations (backwards compatibility)
SCOPES = get_scopes_for_tools()
