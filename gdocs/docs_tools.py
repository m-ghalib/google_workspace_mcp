"""
Google Docs MCP Tools

Primary execution path: REST API (documents.get, documents.create, documents.batchUpdate).
Three RED tools (unmerge_table_cells, update_table_row_style, pin_table_header_rows)
use REST API via TableOperationManager.
"""

import asyncio
import json
import logging
from typing import Any

from auth.service_decorator import require_google_service
from core.utils import handle_http_errors
from core.server import server

from gdocs.managers import TableOperationManager
from gdocs.docs_structure import (
    extract_doc_text,
    find_header_footer_ids,
    find_paragraphs,
    find_tables,
    get_body_elements,
    get_table_cell_range,
    get_table_debug_info,
)
from gdocs.docs_helpers import (
    build_paragraph_style,
    build_table_cell_style,
    build_text_style,
    create_delete_content_range_request,
    create_delete_footer_request,
    create_delete_header_request,
    create_delete_paragraph_bullets_request,
    create_delete_table_column_request,
    create_delete_table_row_request,
    create_footer_request,
    create_header_request,
    create_insert_inline_image_request,
    create_insert_page_break_request,
    create_insert_table_request,
    create_insert_table_column_request,
    create_insert_table_row_request,
    create_insert_text_request,
    create_merge_table_cells_request,
    create_paragraph_bullets_request,
    create_replace_all_text_request,
    create_update_paragraph_style_request,
    create_update_table_cell_style_request,
    create_update_table_column_properties_request,
    create_update_text_style_request,
)

logger = logging.getLogger(__name__)


# =============================================================================
# SHARED HELPERS
# =============================================================================


async def _get_doc(service: Any, document_id: str) -> dict[str, Any]:
    """Fetch the full document JSON via documents.get()."""
    return await asyncio.to_thread(
        service.documents().get(documentId=document_id).execute
    )


async def _batch_update(
    service: Any, document_id: str, requests: list[dict[str, Any]]
) -> dict[str, Any]:
    """Execute a batchUpdate with the given request list."""
    return await asyncio.to_thread(
        service.documents()
        .batchUpdate(documentId=document_id, body={"requests": requests})
        .execute
    )


async def _create_populated_table(
    service: Any,
    document_id: str,
    table_data: list[list[str]],
    bold_headers: bool,
    insert_index: int | None,
) -> dict[str, Any]:
    """Create a table and populate it with data.

    1. Insert an empty table
    2. Re-fetch doc to get new cell byte offsets
    3. Build insertText requests (backwards) + optional bold for row 0
    4. Execute all in one batchUpdate

    Returns:
        Dict with rows, columns, message keys.
    """
    num_rows = len(table_data)
    num_cols = len(table_data[0])

    # Step 1: Insert empty table
    insert_req = create_insert_table_request(num_rows, num_cols, index=insert_index)
    await _batch_update(service, document_id, [insert_req])

    # Step 2: Re-fetch to get cell offsets
    doc = await _get_doc(service, document_id)

    # Find the newly inserted table — it's the last one if no index,
    # or we find it by scanning tables near the insertion point
    tables = find_tables(doc)
    if not tables:
        return {"rows": num_rows, "columns": num_cols, "message": "Table created but no tables found for population"}

    if insert_index is not None:
        # Find table closest to insert_index
        target_table = min(tables, key=lambda t: abs(t["start_index"] - insert_index))
    else:
        # Appended to end — last table
        target_table = tables[-1]

    table_idx = target_table["index"]

    # Step 3: Build cell population requests (backwards to preserve offsets)
    requests: list[dict[str, Any]] = []
    for r in range(num_rows - 1, -1, -1):
        for c in range(num_cols - 1, -1, -1):
            cell_text = table_data[r][c]
            if not cell_text:
                continue
            content_start, cell_end = get_table_cell_range(doc, table_idx, r, c)
            # Delete the default newline in the empty cell, then insert our text
            # Each empty cell has a single "\n" character
            requests.append(create_insert_text_request(cell_text, index=content_start))

    # Step 3b: Bold headers (row 0) — must come after text insertion in the batch
    # but since we're building requests for a second batchUpdate after population,
    # we handle bold separately
    if requests:
        await _batch_update(service, document_id, requests)

    if bold_headers and num_rows > 0:
        # Re-fetch to get updated offsets after text insertion
        doc = await _get_doc(service, document_id)
        bold_requests: list[dict[str, Any]] = []
        for c in range(num_cols):
            cell_text = table_data[0][c]
            if not cell_text:
                continue
            content_start, cell_end = get_table_cell_range(doc, table_idx, 0, c)
            text_style, fields = build_text_style(bold=True)
            bold_requests.append(
                create_update_text_style_request(
                    content_start, content_start + len(cell_text), text_style, fields
                )
            )
        if bold_requests:
            await _batch_update(service, document_id, bold_requests)

    return {
        "rows": num_rows,
        "columns": num_cols,
        "message": f"Created {num_rows}x{num_cols} table with data",
    }


def _doc_link(document_id: str) -> str:
    return f"https://docs.google.com/document/d/{document_id}/edit"


# =============================================================================
# DOCUMENT READING
# =============================================================================


@server.tool()
@handle_http_errors("get_doc_content", is_read_only=True, service_type="docs")
@require_google_service("docs", "docs_read")
async def get_doc_content(
    service: Any,
    user_google_email: str,
    document_id: str,
) -> str:
    """
    Retrieves content of a native Google Doc identified by document_id.

    Returns:
        str: The document content with metadata header.
    """
    logger.info(
        f"[get_doc_content] Invoked. Document ID: '{document_id}' for user '{user_google_email}'"
    )

    doc = await _get_doc(service, document_id)
    title = doc.get("title", "Untitled")
    content = extract_doc_text(doc)
    link = _doc_link(document_id)

    header = (
        f'File: "{title}" (ID: {document_id})\n'
        f"Link: {link}\n\n--- CONTENT ---\n"
    )
    return header + content


@server.tool()
@handle_http_errors("inspect_doc_structure", is_read_only=True, service_type="docs")
@require_google_service("docs", "docs_read")
async def inspect_doc_structure(
    service: Any,
    user_google_email: str,
    document_id: str,
    detailed: bool = False,
) -> str:
    """
    Essential tool for understanding document structure before making changes.

    USE THIS FOR:
    - Understanding document layout before making changes
    - Locating existing tables and their positions
    - Getting document statistics

    WHAT THE OUTPUT SHOWS:
    - totalElements: Number of document elements
    - tables: Number and dimensions of existing tables
    - structure: Element-by-element breakdown (paragraphs, tables, list items)

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to inspect
        detailed: Whether to return detailed structure information

    Returns:
        str: JSON string containing document structure
    """
    logger.debug(f"[inspect_doc_structure] Doc={document_id}, detailed={detailed}")

    doc = await _get_doc(service, document_id)
    elements = get_body_elements(doc)
    tables = find_tables(doc)

    result = {
        "title": doc.get("title", "Untitled"),
        "totalElements": len(elements),
        "tables": [
            {"index": t["index"], "rows": t["rows"], "columns": t["columns"]}
            for t in tables
        ],
        "structure": elements,
    }

    link = _doc_link(document_id)
    return f"Document structure analysis for {document_id}:\n\n{json.dumps(result, indent=2)}\n\nLink: {link}"


@server.tool()
@handle_http_errors("debug_table_structure", is_read_only=True, service_type="docs")
@require_google_service("docs", "docs_read")
async def debug_table_structure(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int = 0,
) -> str:
    """
    ESSENTIAL DEBUGGING TOOL - Use this whenever tables don't work as expected.

    USE THIS IMMEDIATELY WHEN:
    - Table population put data in wrong cells
    - You get "table not found" errors
    - Need to understand existing table structure

    WHAT THIS SHOWS YOU:
    - Exact table dimensions (rows x columns)
    - Each cell's position coordinates (row,col)
    - Current content in each cell

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to inspect
        table_index: Which table to debug (0 = first table, 1 = second table, etc.)

    Returns:
        str: Detailed JSON structure showing table layout and current content
    """
    logger.debug(
        f"[debug_table_structure] Doc={document_id}, table_index={table_index}"
    )

    doc = await _get_doc(service, document_id)
    result = get_table_debug_info(doc, table_index)

    link = _doc_link(document_id)
    return f"Table structure debug for table {table_index}:\n\n{json.dumps(result, indent=2)}\n\nLink: {link}"


# =============================================================================
# DOCUMENT CREATION
# =============================================================================


@server.tool()
@handle_http_errors("create_doc", service_type="docs")
@require_google_service("docs", "docs_write")
async def create_doc(
    service: Any,
    user_google_email: str,
    title: str,
    content: str = "",
) -> str:
    """
    Creates a new Google Doc and optionally inserts initial content.

    Returns:
        str: Confirmation message with document ID and link.
    """
    logger.info(f"[create_doc] Invoked. Email: '{user_google_email}', Title='{title}'")

    result = await asyncio.to_thread(
        service.documents().create(body={"title": title}).execute
    )
    doc_id = result.get("documentId")

    if content:
        # Insert text at index 1 (after the implicit newline at index 0)
        req = create_insert_text_request(content, index=1)
        await _batch_update(service, doc_id, [req])

    link = _doc_link(doc_id)
    msg = f"Created Google Doc '{title}' (ID: {doc_id}) for {user_google_email}. Link: {link}"
    logger.info(msg)
    return msg


# =============================================================================
# TEXT OPERATIONS
# =============================================================================


@server.tool()
@handle_http_errors("modify_doc_text", service_type="docs")
@require_google_service("docs", "docs_write")
async def modify_doc_text(
    service: Any,
    user_google_email: str,
    document_id: str,
    start_index: int,
    end_index: int = None,
    text: str = None,
    bold: bool = None,
    italic: bool = None,
    underline: bool = None,
    font_size: int = None,
    font_family: str = None,
    text_color: str = None,
    background_color: str = None,
) -> str:
    """
    Modifies text in a Google Doc - can insert/replace text and/or apply formatting in a single operation.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        start_index: Start position for operation (0-based)
        end_index: End position for text replacement/formatting (if not provided with text, text is inserted)
        text: New text to insert or replace with (optional - can format existing text without changing it)
        bold: Whether to make text bold (True/False/None to leave unchanged)
        italic: Whether to make text italic (True/False/None to leave unchanged)
        underline: Whether to underline text (True/False/None to leave unchanged)
        font_size: Font size in points
        font_family: Font family name (e.g., "Arial", "Times New Roman")
        text_color: Foreground text color (#RRGGBB)
        background_color: Background/highlight color (#RRGGBB)

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[modify_doc_text] Doc={document_id}, start={start_index}, end={end_index}"
    )

    has_formatting = any([
        bold is not None, italic is not None, underline is not None,
        font_size, font_family, text_color, background_color,
    ])

    if text is None and not has_formatting:
        return "Error: Must provide either 'text' to insert/replace, or formatting parameters."

    if has_formatting and end_index is None and text is None:
        return "Error: 'end_index' is required when applying formatting to existing text."

    requests: list[dict[str, Any]] = []

    # Determine formatting range
    fmt_start = start_index
    fmt_end = end_index

    if text is not None:
        if end_index is not None and end_index > start_index:
            # Replace: delete then insert
            requests.append(create_delete_content_range_request(start_index, end_index))
            requests.append(create_insert_text_request(text, index=start_index))
            fmt_end = start_index + len(text)
        else:
            # Insert
            requests.append(create_insert_text_request(text, index=start_index))
            fmt_end = start_index + len(text)

    if has_formatting:
        text_style, fields = build_text_style(
            bold=bold, italic=italic, underline=underline,
            font_size=font_size, font_family=font_family,
            text_color=text_color, background_color=background_color,
        )
        requests.append(
            create_update_text_style_request(fmt_start, fmt_end, text_style, fields)
        )

    await _batch_update(service, document_id, requests)

    link = _doc_link(document_id)
    ops = []
    if text is not None:
        ops.append("text modified")
    if has_formatting:
        ops.append("formatting applied")
    message = " and ".join(ops).capitalize()
    return f"{message} in document {document_id}. Link: {link}"


@server.tool()
@handle_http_errors("find_and_replace_doc", service_type="docs")
@require_google_service("docs", "docs_write")
async def find_and_replace_doc(
    service: Any,
    user_google_email: str,
    document_id: str,
    find_text: str,
    replace_text: str,
    match_case: bool = False,
) -> str:
    """
    Finds and replaces text throughout a Google Doc.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        find_text: Text to search for
        replace_text: Text to replace with
        match_case: Whether to match case exactly

    Returns:
        str: Confirmation message with replacement details
    """
    logger.info(
        f"[find_and_replace_doc] Doc={document_id}, find='{find_text}', replace='{replace_text}'"
    )

    req = create_replace_all_text_request(find_text, replace_text, match_case)
    result = await _batch_update(service, document_id, [req])

    # Extract replacement count from API response
    replies = result.get("replies", [])
    occurrences = 0
    if replies:
        occurrences = replies[0].get("replaceAllText", {}).get("occurrencesChanged", 0)

    link = _doc_link(document_id)
    return f"Replaced {occurrences} occurrence(s) of '{find_text}' with '{replace_text}' in document {document_id}. Link: {link}"


@server.tool()
@handle_http_errors("delete_doc_content", service_type="docs")
@require_google_service("docs", "docs_write")
async def delete_doc_content(
    service: Any,
    user_google_email: str,
    document_id: str,
    start_index: int,
    end_index: int,
) -> str:
    """
    Deletes content from a Google Doc within a specified index range.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to modify
        start_index: Start position of content to delete (0-based, inclusive)
        end_index: End position of content to delete (exclusive)

    Returns:
        str: Confirmation message with deletion details
    """
    logger.info(
        f"[delete_doc_content] Doc={document_id}, start={start_index}, end={end_index}"
    )

    if start_index < 0:
        return "Error: start_index must be >= 0"
    if end_index <= start_index:
        return "Error: end_index must be greater than start_index"

    req = create_delete_content_range_request(start_index, end_index)
    await _batch_update(service, document_id, [req])

    chars_deleted = end_index - start_index
    link = _doc_link(document_id)
    return f"Deleted {chars_deleted} character(s) from indices {start_index} to {end_index} in document {document_id}. Link: {link}"


# =============================================================================
# TABLE OPERATIONS
# =============================================================================


@server.tool()
@handle_http_errors("create_table_with_data", service_type="docs")
@require_google_service("docs", "docs_write")
async def create_table_with_data(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_data: list[list[str]],
    index: int = None,
    bold_headers: bool = True,
) -> str:
    """
    Creates a table and populates it with data in one reliable operation.

    EXAMPLE DATA FORMAT:
    table_data = [
        ["Header1", "Header2", "Header3"],    # Row 0 - headers
        ["Data1", "Data2", "Data3"],          # Row 1 - first data row
        ["Data4", "Data5", "Data6"]           # Row 2 - second data row
    ]

    DATA FORMAT REQUIREMENTS:
    - Must be 2D list of strings only
    - Each inner list = one table row
    - All rows MUST have same number of columns
    - Use empty strings "" for empty cells, never None

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        table_data: 2D list of strings - EXACT format: [["col1", "col2"], ["row1col1", "row1col2"]]
        index: Element index for insertion (optional, appends to end if not provided)
        bold_headers: Whether to make first row bold (default: true)

    Returns:
        str: Confirmation with table details and link
    """
    logger.debug(f"[create_table_with_data] Doc={document_id}, index={index}")

    if not table_data or not table_data[0]:
        return "ERROR: Table data cannot be empty"

    col_counts = [len(row) for row in table_data]
    if len(set(col_counts)) > 1:
        return f"ERROR: All rows must have same column count. Found: {col_counts}"

    # Convert element index to byte offset if provided
    insert_index = None
    if index is not None:
        doc = await _get_doc(service, document_id)
        body = doc.get("body", {})
        content = body.get("content", [])
        if index < len(content):
            insert_index = content[index].get("startIndex", 1)
        else:
            insert_index = None  # Append to end

    result = await _create_populated_table(
        service, document_id, table_data, bold_headers, insert_index
    )

    message = result.get("message", f"Created {result['rows']}x{result['columns']} table")
    link = _doc_link(document_id)
    return f"SUCCESS: {message}. Link: {link}"


@server.tool()
@handle_http_errors("insert_table_row", service_type="docs")
@require_google_service("docs", "docs_write")
async def insert_table_row(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    row_index: int,
    insert_below: bool = True,
) -> str:
    """
    Inserts a new row into an existing table in a Google Doc.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        row_index: Row position to insert relative to (0-based)
        insert_below: If True, insert below the specified row; if False, insert above

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[insert_table_row] Doc={document_id}, table={table_index}, row={row_index}, below={insert_below}"
    )

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_insert_table_row_request(table_start, row_index, insert_below=insert_below)
    await _batch_update(service, document_id, [req])

    # Re-fetch to get new dimensions
    doc = await _get_doc(service, document_id)
    new_tables = find_tables(doc)
    new_dims = f"{new_tables[table_index]['rows']}x{new_tables[table_index]['columns']}" if table_index < len(new_tables) else "unknown"

    link = _doc_link(document_id)
    position = "below" if insert_below else "above"
    return f"Inserted row {position} row {row_index} in table {table_index}. New dimensions: {new_dims}. Link: {link}"


@server.tool()
@handle_http_errors("delete_table_row", service_type="docs")
@require_google_service("docs", "docs_write")
async def delete_table_row(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    row_index: int,
) -> str:
    """
    Deletes a row from an existing table in a Google Doc.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        row_index: Row to delete (0-based)

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[delete_table_row] Doc={document_id}, table={table_index}, row={row_index}"
    )

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_delete_table_row_request(table_start, row_index)
    await _batch_update(service, document_id, [req])

    # Re-fetch to get new dimensions
    doc = await _get_doc(service, document_id)
    new_tables = find_tables(doc)
    new_dims = f"{new_tables[table_index]['rows']}x{new_tables[table_index]['columns']}" if table_index < len(new_tables) else "unknown"

    link = _doc_link(document_id)
    return f"Deleted row {row_index} from table {table_index}. New dimensions: {new_dims}. Link: {link}"


@server.tool()
@handle_http_errors("insert_table_column", service_type="docs")
@require_google_service("docs", "docs_write")
async def insert_table_column(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    column_index: int,
    insert_right: bool = True,
) -> str:
    """
    Inserts a new column into an existing table in a Google Doc.

    Note: Google Docs limits tables to 20 columns maximum.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        column_index: Column position to insert relative to (0-based)
        insert_right: If True, insert to the right; if False, insert to the left

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[insert_table_column] Doc={document_id}, table={table_index}, col={column_index}, right={insert_right}"
    )

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_insert_table_column_request(table_start, col_index=column_index, insert_right=insert_right)
    await _batch_update(service, document_id, [req])

    # Re-fetch to get new dimensions
    doc = await _get_doc(service, document_id)
    new_tables = find_tables(doc)
    new_dims = f"{new_tables[table_index]['rows']}x{new_tables[table_index]['columns']}" if table_index < len(new_tables) else "unknown"

    link = _doc_link(document_id)
    position = "right of" if insert_right else "left of"
    return f"Inserted column {position} column {column_index} in table {table_index}. New dimensions: {new_dims}. Link: {link}"


@server.tool()
@handle_http_errors("delete_table_column", service_type="docs")
@require_google_service("docs", "docs_write")
async def delete_table_column(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    column_index: int,
) -> str:
    """
    Deletes a column from an existing table in a Google Doc.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        column_index: Column to delete (0-based)

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[delete_table_column] Doc={document_id}, table={table_index}, col={column_index}"
    )

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_delete_table_column_request(table_start, col_index=column_index)
    await _batch_update(service, document_id, [req])

    # Re-fetch to get new dimensions
    doc = await _get_doc(service, document_id)
    new_tables = find_tables(doc)
    new_dims = f"{new_tables[table_index]['rows']}x{new_tables[table_index]['columns']}" if table_index < len(new_tables) else "unknown"

    link = _doc_link(document_id)
    return f"Deleted column {column_index} from table {table_index}. New dimensions: {new_dims}. Link: {link}"


# =============================================================================
# PARAGRAPH STYLING
# =============================================================================


@server.tool()
@handle_http_errors("update_paragraph_style", service_type="docs")
@require_google_service("docs", "docs_write")
async def update_paragraph_style(
    service: Any,
    user_google_email: str,
    document_id: str,
    paragraph_index: int,
    heading_level: int = None,
    alignment: str = None,
    line_spacing: float = None,
    indent_first_line: float = None,
    indent_start: float = None,
    indent_end: float = None,
    space_above: float = None,
    space_below: float = None,
) -> str:
    """
    Apply paragraph-level formatting and/or heading styles to a paragraph.

    Args:
        user_google_email: User's Google email address
        document_id: Document ID to modify
        paragraph_index: Element index of the paragraph in the document body (0-based).
                        Use inspect_doc_structure to find element indices.
        heading_level: Heading level 0-6 (0 = NORMAL_TEXT, 1 = H1, 2 = H2, etc.)
        alignment: Text alignment - 'START' (left), 'CENTER', 'END' (right), or 'JUSTIFIED'
        line_spacing: Line spacing multiplier (1.0 = single, 1.5 = 1.5x, 2.0 = double)
        indent_first_line: First line indent in points
        indent_start: Left/start indent in points
        indent_end: Right/end indent in points
        space_above: Space above paragraph in points
        space_below: Space below paragraph in points

    Returns:
        str: Confirmation message with formatting details
    """
    logger.info(
        f"[update_paragraph_style] Doc={document_id}, paragraph={paragraph_index}"
    )

    style, fields = build_paragraph_style(
        heading_level=heading_level, alignment=alignment,
        line_spacing=line_spacing, indent_first_line=indent_first_line,
        indent_start=indent_start, indent_end=indent_end,
        space_above=space_above, space_below=space_below,
    )

    if not fields:
        return f"No paragraph style changes specified for document {document_id}"

    doc = await _get_doc(service, document_id)
    body = doc.get("body", {})
    content = body.get("content", [])

    if paragraph_index >= len(content):
        return f"Error: paragraph_index {paragraph_index} out of range (document has {len(content)} elements)"

    element = content[paragraph_index]
    if "paragraph" not in element:
        return f"Error: Element at index {paragraph_index} is not a paragraph"

    start = element.get("startIndex", 0)
    end = element.get("endIndex", 0)

    req = create_update_paragraph_style_request(start, end, style, fields)
    await _batch_update(service, document_id, [req])

    link = _doc_link(document_id)
    return f"Paragraph style updated at index {paragraph_index} in document {document_id}. Link: {link}"


# =============================================================================
# LIST FORMATTING
# =============================================================================


@server.tool()
@handle_http_errors("create_paragraph_bullets", service_type="docs")
@require_google_service("docs", "docs_write")
async def create_paragraph_bullets(
    service: Any,
    user_google_email: str,
    document_id: str,
    paragraph_indices: list[int],
    list_type: str = "UNORDERED",
) -> str:
    """
    Converts existing paragraphs to bullet points or numbered lists.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to modify
        paragraph_indices: List of element indices of paragraphs to convert.
                          Use inspect_doc_structure to find element indices.
        list_type: Type of list ("UNORDERED" or "ORDERED"). Defaults to "UNORDERED".

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[create_paragraph_bullets] Doc={document_id}, paragraphs={paragraph_indices}, type={list_type}"
    )

    valid_list_types = ["UNORDERED", "ORDERED"]
    list_type_upper = list_type.upper()
    if list_type_upper not in valid_list_types:
        return f"Error: Invalid list_type '{list_type}'. Must be 'UNORDERED' or 'ORDERED'."

    preset_map = {
        "UNORDERED": "BULLET_DISC_CIRCLE_SQUARE",
        "ORDERED": "NUMBERED_DECIMAL_ALPHA_ROMAN",
    }
    bullet_preset = preset_map[list_type_upper]

    doc = await _get_doc(service, document_id)
    body = doc.get("body", {})
    content = body.get("content", [])

    requests: list[dict[str, Any]] = []
    for idx in paragraph_indices:
        if idx >= len(content):
            return f"Error: paragraph_index {idx} out of range (document has {len(content)} elements)"
        element = content[idx]
        if "paragraph" not in element:
            return f"Error: Element at index {idx} is not a paragraph"
        start = element.get("startIndex", 0)
        end = element.get("endIndex", 0)
        requests.append(create_paragraph_bullets_request(start, end, bullet_preset))

    await _batch_update(service, document_id, requests)

    link = _doc_link(document_id)
    return f"Applied {list_type_upper} list formatting to {len(paragraph_indices)} paragraph(s) in document {document_id}. Link: {link}"


@server.tool()
@handle_http_errors("delete_paragraph_bullets", service_type="docs")
@require_google_service("docs", "docs_write")
async def delete_paragraph_bullets(
    service: Any,
    user_google_email: str,
    document_id: str,
    paragraph_indices: list[int],
) -> str:
    """
    Removes bullet points or numbered list formatting from paragraphs.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to modify
        paragraph_indices: List of element indices of paragraphs to remove formatting from.
                          Use inspect_doc_structure to find element indices.

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[delete_paragraph_bullets] Doc={document_id}, paragraphs={paragraph_indices}"
    )

    doc = await _get_doc(service, document_id)
    body = doc.get("body", {})
    content = body.get("content", [])

    requests: list[dict[str, Any]] = []
    for idx in paragraph_indices:
        if idx >= len(content):
            return f"Error: paragraph_index {idx} out of range (document has {len(content)} elements)"
        element = content[idx]
        if "paragraph" not in element:
            return f"Error: Element at index {idx} is not a paragraph"
        start = element.get("startIndex", 0)
        end = element.get("endIndex", 0)
        requests.append(create_delete_paragraph_bullets_request(start, end))

    await _batch_update(service, document_id, requests)

    link = _doc_link(document_id)
    return f"Removed list formatting from {len(paragraph_indices)} paragraph(s) in document {document_id}. Link: {link}"


# =============================================================================
# TABLE CELL STYLING
# =============================================================================


@server.tool()
@handle_http_errors("update_table_cell_style", service_type="docs")
@require_google_service("docs", "docs_write")
async def update_table_cell_style(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    row_index: int,
    column_index: int,
    background_color: str = None,
    padding_top: float = None,
    padding_bottom: float = None,
    padding_left: float = None,
    padding_right: float = None,
    content_alignment: str = None,
) -> str:
    """
    Updates the style of a specific table cell (background, padding, alignment).

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        row_index: Row of the cell (0-based)
        column_index: Column of the cell (0-based)
        background_color: Cell background color as hex "#RRGGBB" (e.g., "#FFFF00" for yellow)
        padding_top: Top padding in points
        padding_bottom: Bottom padding in points
        padding_left: Left padding in points
        padding_right: Right padding in points
        content_alignment: Vertical text alignment - "TOP", "MIDDLE", or "BOTTOM"

    Returns:
        str: Confirmation message with operation details
    """
    logger.info(
        f"[update_table_cell_style] Doc={document_id}, table={table_index}, cell=({row_index},{column_index})"
    )

    cell_style, fields = build_table_cell_style(
        background_color=background_color,
        padding_top=padding_top, padding_bottom=padding_bottom,
        padding_left=padding_left, padding_right=padding_right,
        content_alignment=content_alignment,
    )

    if not fields:
        return "Error: At least one style parameter must be provided."

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_update_table_cell_style_request(
        table_start, row_index, column_index, cell_style, fields
    )
    await _batch_update(service, document_id, [req])

    link = _doc_link(document_id)
    return f"Cell style updated for ({row_index},{column_index}) in table {table_index}. Link: {link}"


@server.tool()
@handle_http_errors("merge_table_cells", service_type="docs")
@require_google_service("docs", "docs_write")
async def merge_table_cells(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    start_row: int,
    start_col: int,
    row_span: int,
    col_span: int,
) -> str:
    """
    Merges a range of cells in a table.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        start_row: Starting row index for merge (0-based)
        start_col: Starting column index for merge (0-based)
        row_span: Number of rows to merge (must be >= 1)
        col_span: Number of columns to merge (must be >= 1)

    Returns:
        str: Confirmation message with merge details
    """
    logger.info(
        f"[merge_table_cells] Doc={document_id}, table={table_index}, "
        f"start=({start_row},{start_col}), span={row_span}x{col_span}"
    )

    if row_span < 1 or col_span < 1:
        return "Error: row_span and col_span must be >= 1"
    if row_span == 1 and col_span == 1:
        return "Error: Merging a single cell has no effect."

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_merge_table_cells_request(
        table_start, start_row, start_col, row_span, col_span
    )
    await _batch_update(service, document_id, [req])

    link = _doc_link(document_id)
    return f"Merged {row_span}x{col_span} cells starting at ({start_row},{start_col}) in table {table_index}. Link: {link}"


@server.tool()
@handle_http_errors("set_table_column_width", service_type="docs")
@require_google_service("docs", "docs_write")
async def set_table_column_width(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    column_indices: list[int],
    width: float = None,
    width_type: str = "FIXED_WIDTH",
) -> str:
    """
    Sets the width properties for one or more table columns.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        column_indices: List of column indices to modify (0-based)
        width: Column width in points (required for FIXED_WIDTH). 72 points = 1 inch.
        width_type: Width type - "FIXED_WIDTH" or "EVENLY_DISTRIBUTED"

    Returns:
        str: Confirmation message with width details
    """
    logger.info(
        f"[set_table_column_width] Doc={document_id}, table={table_index}, cols={column_indices}"
    )

    if not column_indices:
        return "Error: column_indices list cannot be empty"

    valid_width_types = ["FIXED_WIDTH", "EVENLY_DISTRIBUTED"]
    if width_type not in valid_width_types:
        return f"Error: width_type must be one of {valid_width_types}"

    if width_type == "FIXED_WIDTH" and width is None:
        return "Error: width is required when width_type is 'FIXED_WIDTH'"

    doc = await _get_doc(service, document_id)
    tables = find_tables(doc)

    if table_index >= len(tables):
        return f"Error: Table index {table_index} not found. Document has {len(tables)} tables."

    table_start = tables[table_index]["start_index"]
    req = create_update_table_column_properties_request(
        table_start, column_indices, width, width_type
    )
    await _batch_update(service, document_id, [req])

    link = _doc_link(document_id)
    return f"Column width updated for columns {column_indices} in table {table_index}. Link: {link}"


# =============================================================================
# DOCUMENT ELEMENTS (tables, page breaks, images)
# =============================================================================


@server.tool()
@handle_http_errors("insert_doc_elements", service_type="docs")
@require_google_service("docs", "docs_write")
async def insert_doc_elements(
    service: Any,
    user_google_email: str,
    document_id: str,
    element_type: str,
    rows: int = None,
    columns: int = None,
    data: list[list[str]] = None,
    image_url: str = None,
    width: int = None,
    height: int = None,
) -> str:
    """
    Inserts structural elements like tables, page breaks, or images into a Google Doc.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        element_type: Type of element to insert ("table", "page_break", "image")
        rows: Number of rows for table (required for empty table)
        columns: Number of columns for table (required for empty table)
        data: 2D list of data for table with content
        image_url: URL of image to insert (for image type)
        width: Width in points (for image)
        height: Height in points (for image)

    Returns:
        str: Confirmation message with insertion details
    """
    logger.info(
        f"[insert_doc_elements] Doc={document_id}, type={element_type}"
    )

    link = _doc_link(document_id)

    if element_type == "table":
        if data:
            # Table with data — use the populated table helper
            col_counts = [len(row) for row in data]
            if len(set(col_counts)) > 1:
                return f"ERROR: All rows must have same column count. Found: {col_counts}"
            result = await _create_populated_table(service, document_id, data, bold_headers=False, insert_index=None)
            return f"{result['message']} in document {document_id}. Link: {link}"
        elif rows and columns:
            # Empty table
            req = create_insert_table_request(rows, columns)
            await _batch_update(service, document_id, [req])
            return f"Inserted empty {rows}x{columns} table in document {document_id}. Link: {link}"
        else:
            return "Error: 'data' or 'rows'+'columns' required for table insertion."

    elif element_type == "page_break":
        req = create_insert_page_break_request()
        await _batch_update(service, document_id, [req])
        return f"Inserted page break in document {document_id}. Link: {link}"

    elif element_type == "image":
        if not image_url:
            return "Error: 'image_url' required for image insertion."
        req = create_insert_inline_image_request(
            image_url,
            width=float(width) if width else None,
            height=float(height) if height else None,
        )
        await _batch_update(service, document_id, [req])
        size_info = ""
        if width or height:
            size_info = f" (size: {width or 'auto'}x{height or 'auto'} points)"
        return f"Inserted image{size_info} in document {document_id}. Link: {link}"

    else:
        return f"Error: Unsupported element type '{element_type}'. Supported: 'table', 'page_break', 'image'."


@server.tool()
@handle_http_errors("insert_doc_image", service_type="docs")
@require_google_service("docs", "docs_write")
async def insert_doc_image(
    service: Any,
    user_google_email: str,
    document_id: str,
    image_url: str,
    width: int = 0,
    height: int = 0,
) -> str:
    """
    Inserts an image into a Google Doc from a URL.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        image_url: Image URL (public URL)
        width: Image width in points (optional)
        height: Image height in points (optional)

    Returns:
        str: Confirmation message with insertion details
    """
    logger.info(
        f"[insert_doc_image] Doc={document_id}, source={image_url}"
    )

    if not (image_url.startswith("http://") or image_url.startswith("https://")):
        return "Error: image_url must be a URL (http:// or https://)."

    req = create_insert_inline_image_request(
        image_url,
        width=float(width) if width else None,
        height=float(height) if height else None,
    )
    await _batch_update(service, document_id, [req])

    size_info = ""
    if width or height:
        size_info = f" (size: {width or 'auto'}x{height or 'auto'} points)"

    link = _doc_link(document_id)
    return f"Inserted image{size_info} in document {document_id}. Link: {link}"


# =============================================================================
# HEADER/FOOTER MANAGEMENT
# =============================================================================


@server.tool()
@handle_http_errors("update_doc_headers_footers", service_type="docs")
@require_google_service("docs", "docs_write")
async def update_doc_headers_footers(
    service: Any,
    user_google_email: str,
    document_id: str,
    section_type: str,
    content: str,
    header_footer_type: str = "DEFAULT",
) -> str:
    """
    Updates headers or footers in a Google Doc.

    Now supports all header/footer types including FIRST_PAGE and EVEN_PAGE.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        section_type: Type of section to update ("header" or "footer")
        content: Text content for the header/footer
        header_footer_type: Type of header/footer ("DEFAULT", "FIRST_PAGE_ONLY", "EVEN_PAGE")

    Returns:
        str: Confirmation message with update details
    """
    logger.info(f"[update_doc_headers_footers] Doc={document_id}, type={section_type}")

    if section_type not in ["header", "footer"]:
        return "Error: section_type must be 'header' or 'footer'"

    # Map tool types to REST API types
    type_map = {
        "DEFAULT": "DEFAULT",
        "FIRST_PAGE_ONLY": "FIRST_PAGE",
        "FIRST_PAGE": "FIRST_PAGE",
        "EVEN_PAGE": "EVEN_PAGE",
    }
    api_type = type_map.get(header_footer_type.upper(), "DEFAULT")

    doc = await _get_doc(service, document_id)
    hf_ids = find_header_footer_ids(doc)

    # Determine which ID to look for
    id_key_map = {
        ("header", "DEFAULT"): "default_header_id",
        ("footer", "DEFAULT"): "default_footer_id",
        ("header", "FIRST_PAGE"): "first_page_header_id",
        ("footer", "FIRST_PAGE"): "first_page_footer_id",
        ("header", "EVEN_PAGE"): "even_page_header_id",
        ("footer", "EVEN_PAGE"): "even_page_footer_id",
    }

    id_key = id_key_map.get((section_type, api_type))
    segment_id = hf_ids.get(id_key) if id_key else None

    requests: list[dict[str, Any]] = []

    if not segment_id:
        # Create the header/footer first
        if section_type == "header":
            requests.append(create_header_request(api_type))
        else:
            requests.append(create_footer_request(api_type))

        # For FIRST_PAGE / EVEN_PAGE, enable the document style flag
        if api_type == "FIRST_PAGE":
            requests.append({
                "updateDocumentStyle": {
                    "documentStyle": {"useFirstPageHeaderFooter": True},
                    "fields": "useFirstPageHeaderFooter",
                }
            })
        elif api_type == "EVEN_PAGE":
            requests.append({
                "updateDocumentStyle": {
                    "documentStyle": {"useEvenPageHeaderFooter": True},
                    "fields": "useEvenPageHeaderFooter",
                }
            })

        result = await _batch_update(service, document_id, requests)

        # Extract the newly created header/footer ID from the reply
        replies = result.get("replies", [])
        for reply in replies:
            if "createHeader" in reply:
                segment_id = reply["createHeader"].get("headerId")
            elif "createFooter" in reply:
                segment_id = reply["createFooter"].get("footerId")

    if not segment_id:
        return f"Error: Could not create or find {section_type} of type {header_footer_type}"

    # Now insert text into the header/footer
    # First, get the current content range to clear it
    doc = await _get_doc(service, document_id)

    # Get header/footer content for clearing
    if section_type == "header":
        sections = doc.get("headers", {})
    else:
        sections = doc.get("footers", {})

    section_data = sections.get(segment_id, {})
    section_content = section_data.get("content", [])

    clear_requests: list[dict[str, Any]] = []
    if section_content and len(section_content) > 0:
        # Find the text range in the header/footer
        first_start = None
        last_end = None
        for elem in section_content:
            s = elem.get("startIndex")
            e = elem.get("endIndex")
            if s is not None and (first_start is None or s < first_start):
                first_start = s
            if e is not None and (last_end is None or e > last_end):
                last_end = e

        # Clear existing content (but keep at least one newline)
        if first_start is not None and last_end is not None and last_end > first_start + 1:
            clear_requests.append(
                create_delete_content_range_request(first_start, last_end - 1, segment_id=segment_id)
            )

    # Insert new content
    insert_requests = [create_insert_text_request(content, index=0, segment_id=segment_id)]

    all_requests = clear_requests + insert_requests
    await _batch_update(service, document_id, all_requests)

    link = _doc_link(document_id)
    return f"Updated {section_type} ({header_footer_type}) in document {document_id}. Link: {link}"


@server.tool()
@handle_http_errors("delete_doc_header_footer", service_type="docs")
@require_google_service("docs", "docs_write")
async def delete_doc_header_footer(
    service: Any,
    user_google_email: str,
    document_id: str,
    section_type: str,
    header_footer_type: str = "DEFAULT",
) -> str:
    """
    Deletes a header or footer section from a Google Doc.

    Now supports all types including FIRST_PAGE and EVEN_PAGE.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        section_type: Type of section to delete ("header" or "footer")
        header_footer_type: Type of header/footer ("DEFAULT", "FIRST_PAGE", or "EVEN_PAGE")

    Returns:
        str: Confirmation message with deletion details
    """
    logger.info(
        f"[delete_doc_header_footer] Doc={document_id}, type={section_type}, hf_type={header_footer_type}"
    )

    if section_type not in ["header", "footer"]:
        return "Error: section_type must be 'header' or 'footer'"

    type_map = {
        "DEFAULT": "DEFAULT",
        "FIRST_PAGE_ONLY": "FIRST_PAGE",
        "FIRST_PAGE": "FIRST_PAGE",
        "EVEN_PAGE": "EVEN_PAGE",
    }
    api_type = type_map.get(header_footer_type.upper(), "DEFAULT")

    doc = await _get_doc(service, document_id)
    hf_ids = find_header_footer_ids(doc)

    id_key_map = {
        ("header", "DEFAULT"): "default_header_id",
        ("footer", "DEFAULT"): "default_footer_id",
        ("header", "FIRST_PAGE"): "first_page_header_id",
        ("footer", "FIRST_PAGE"): "first_page_footer_id",
        ("header", "EVEN_PAGE"): "even_page_header_id",
        ("footer", "EVEN_PAGE"): "even_page_footer_id",
    }

    id_key = id_key_map.get((section_type, api_type))
    segment_id = hf_ids.get(id_key) if id_key else None

    if not segment_id:
        return f"No {section_type} of type {header_footer_type} found in document {document_id}"

    if section_type == "header":
        req = create_delete_header_request(segment_id)
    else:
        req = create_delete_footer_request(segment_id)

    await _batch_update(service, document_id, [req])

    link = _doc_link(document_id)
    return f"Deleted {section_type} ({header_footer_type}) from document {document_id}. Link: {link}"


# =============================================================================
# BATCH OPERATIONS (atomic via REST API batchUpdate)
# =============================================================================


@server.tool()
@handle_http_errors("batch_update_doc", service_type="docs")
@require_google_service("docs", "docs_write")
async def batch_update_doc(
    service: Any,
    user_google_email: str,
    document_id: str,
    operations: list[dict[str, Any]],
) -> str:
    """
    Executes multiple document operations atomically in a single batchUpdate.

    All operations succeed or none are applied — true atomicity.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document to update
        operations: List of operation dictionaries. Each operation should contain:
                   - type: Operation type ('insert_text', 'delete_text', 'replace_text',
                          'format_text', 'find_replace')
                   - Additional parameters specific to each operation type

    Returns:
        str: Confirmation message with batch operation results
    """
    logger.debug(f"[batch_update_doc] Doc={document_id}, operations={len(operations)}")

    if not operations:
        return "Error: No operations provided."

    requests: list[dict[str, Any]] = []

    for op in operations:
        op_type = op.get("type")

        if op_type == "insert_text":
            requests.append(create_insert_text_request(op["text"], index=op["index"]))

        elif op_type == "delete_text":
            requests.append(
                create_delete_content_range_request(op["start_index"], op["end_index"])
            )

        elif op_type == "replace_text":
            # Delete then insert at same position
            requests.append(
                create_delete_content_range_request(op["start_index"], op["end_index"])
            )
            requests.append(
                create_insert_text_request(op["text"], index=op["start_index"])
            )

        elif op_type == "format_text":
            text_style, fields = build_text_style(
                bold=op.get("bold"),
                italic=op.get("italic"),
                underline=op.get("underline"),
                font_size=op.get("font_size"),
                font_family=op.get("font_family"),
                text_color=op.get("text_color"),
                background_color=op.get("background_color"),
            )
            requests.append(
                create_update_text_style_request(
                    op["start_index"], op["end_index"], text_style, fields
                )
            )

        elif op_type == "find_replace":
            requests.append(
                create_replace_all_text_request(
                    op["find_text"],
                    op["replace_text"],
                    op.get("match_case", False),
                )
            )

        else:
            return f"Error: Unsupported operation type '{op_type}'"

    await _batch_update(service, document_id, requests)

    link = _doc_link(document_id)
    return f"Successfully executed {len(operations)} operations (atomic) on document {document_id}. Link: {link}"


# =============================================================================
# RED TOOLS — Remain on REST API via TableOperationManager
# =============================================================================


@server.tool()
@handle_http_errors("unmerge_table_cells", service_type="docs")
@require_google_service("docs", "docs_write")
async def unmerge_table_cells(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    row_index: int,
    col_index: int,
    row_span: int,
    col_span: int,
) -> str:
    """
    Unmerges previously merged cells in a table.

    Splits a merged cell back into individual cells. The content remains in the
    top-left cell; other cells become empty.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        row_index: Row index of the merged cell (0-based)
        col_index: Column index of the merged cell (0-based)
        row_span: Number of rows the merged cell spans
        col_span: Number of columns the merged cell spans

    Returns:
        str: Confirmation message with unmerge details
    """
    logger.info(
        f"[unmerge_table_cells] Doc={document_id}, table={table_index}, "
        f"cell=({row_index},{col_index}), span={row_span}x{col_span}"
    )

    if row_span < 1 or col_span < 1:
        return "Error: row_span and col_span must be >= 1"

    table_manager = TableOperationManager(service)
    success, message, metadata = await table_manager.unmerge_cells(
        document_id, table_index, row_index, col_index, row_span, col_span
    )

    if success:
        link = _doc_link(document_id)
        return f"{message}. Link: {link}"
    else:
        return f"Error: {message}"


@server.tool()
@handle_http_errors("update_table_row_style", service_type="docs")
@require_google_service("docs", "docs_write")
async def update_table_row_style(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    row_indices: list[int],
    min_row_height: float = None,
    prevent_overflow: bool = None,
) -> str:
    """
    Updates the style of one or more table rows.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        row_indices: List of row indices to style (0-based)
        min_row_height: Minimum row height in points
        prevent_overflow: If True, prevents content from expanding row height

    Returns:
        str: Confirmation message with styling details
    """
    logger.info(
        f"[update_table_row_style] Doc={document_id}, table={table_index}, rows={row_indices}"
    )

    if not row_indices:
        return "Error: row_indices list cannot be empty"

    if min_row_height is None and prevent_overflow is None:
        return "Error: At least one style property must be provided"

    table_manager = TableOperationManager(service)
    success, message, metadata = await table_manager.update_row_style(
        document_id, table_index, row_indices, min_row_height, prevent_overflow
    )

    if success:
        link = _doc_link(document_id)
        return f"{message}. Link: {link}"
    else:
        return f"Error: {message}"


@server.tool()
@handle_http_errors("pin_table_header_rows", service_type="docs")
@require_google_service("docs", "docs_write")
async def pin_table_header_rows(
    service: Any,
    user_google_email: str,
    document_id: str,
    table_index: int,
    pinned_header_rows_count: int,
) -> str:
    """
    Pins rows as repeating table headers that appear at the top of each page.

    Args:
        user_google_email: User's Google email address
        document_id: ID of the document containing the table
        table_index: Which table to modify (0 = first table, 1 = second, etc.)
        pinned_header_rows_count: Number of rows to pin as headers (0 to unpin all)

    Returns:
        str: Confirmation message with pinning details
    """
    logger.info(
        f"[pin_table_header_rows] Doc={document_id}, table={table_index}, "
        f"pinned_rows={pinned_header_rows_count}"
    )

    if pinned_header_rows_count < 0:
        return "Error: pinned_header_rows_count cannot be negative"

    table_manager = TableOperationManager(service)
    success, message, metadata = await table_manager.pin_header_rows(
        document_id, table_index, pinned_header_rows_count
    )

    if success:
        link = _doc_link(document_id)
        return f"{message}. Link: {link}"
    else:
        return f"Error: {message}"


# Comment management tools are now unified in core/comments.py
# Use: read_comments, create_comment, reply_to_comment, resolve_comment with file_id parameter
