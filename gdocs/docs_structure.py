"""
Google Docs Document Structure — REST API structure parsing

Provides functions to parse Google Docs API JSON responses into structured
element data with byte offsets, enabling tools to translate between
user-facing element indices and the byte-offset addressing the REST API requires.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


# =============================================================================
# TABLE FINDING (original — used by TableOperationManager + new tools)
# =============================================================================


def find_tables(doc_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Find all tables in the document with their positions and dimensions.

    Args:
        doc_data: Raw document data from Google Docs API

    Returns:
        List of table information dictionaries with start_index, rows, columns
    """
    tables = []
    body = doc_data.get("body", {})
    content = body.get("content", [])

    for element in content:
        if "table" not in element:
            continue

        table = element["table"]
        table_rows = table.get("tableRows", [])

        tables.append({
            "index": len(tables),
            "start_index": element.get("startIndex", 0),
            "end_index": element.get("endIndex", 0),
            "rows": len(table_rows),
            "columns": len(table_rows[0].get("tableCells", [])) if table_rows else 0,
        })

    return tables


# =============================================================================
# BODY ELEMENT PARSING
# =============================================================================


def get_body_elements(doc_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Parse document body into a flat list of elements with types and byte offsets.

    Each element in body.content[] becomes one entry. Paragraphs include their
    text content and named style; tables include dimensions; list items include
    bullet metadata.

    Args:
        doc_data: Raw document data from Google Docs API

    Returns:
        List of element dicts with keys: element_index, type, start_index, end_index, ...
    """
    elements = []
    body = doc_data.get("body", {})
    content = body.get("content", [])

    table_counter = 0
    for i, element in enumerate(content):
        start = element.get("startIndex", 0)
        end = element.get("endIndex", 0)

        if "paragraph" in element:
            para = element["paragraph"]
            style = para.get("paragraphStyle", {})
            named_style = style.get("namedStyleType", "NORMAL_TEXT")
            bullet = para.get("bullet")

            elem_info: dict[str, Any] = {
                "element_index": i,
                "type": "list_item" if bullet else "paragraph",
                "start_index": start,
                "end_index": end,
                "named_style": named_style,
            }
            if bullet:
                elem_info["list_id"] = bullet.get("listId", "")
                elem_info["nesting_level"] = bullet.get("nestingLevel", 0)

            # Extract text content
            text_parts = []
            for pe in para.get("elements", []):
                if "textRun" in pe:
                    text_parts.append(pe["textRun"].get("content", ""))
            elem_info["text"] = "".join(text_parts)

            elements.append(elem_info)

        elif "table" in element:
            table = element["table"]
            table_rows = table.get("tableRows", [])
            elements.append({
                "element_index": i,
                "type": "table",
                "start_index": start,
                "end_index": end,
                "table_index": table_counter,
                "rows": len(table_rows),
                "columns": len(table_rows[0].get("tableCells", [])) if table_rows else 0,
            })
            table_counter += 1

        elif "sectionBreak" in element:
            elements.append({
                "element_index": i,
                "type": "section_break",
                "start_index": start,
                "end_index": end,
            })

        elif "tableOfContents" in element:
            elements.append({
                "element_index": i,
                "type": "table_of_contents",
                "start_index": start,
                "end_index": end,
            })

        else:
            elements.append({
                "element_index": i,
                "type": "unknown",
                "start_index": start,
                "end_index": end,
            })

    return elements


def find_paragraphs(doc_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Find all paragraphs in the document with their byte offsets and styles.

    Args:
        doc_data: Raw document data from Google Docs API

    Returns:
        List of paragraph dicts: {element_index, start_index, end_index, named_style}
    """
    paragraphs = []
    body = doc_data.get("body", {})
    content = body.get("content", [])

    for i, element in enumerate(content):
        if "paragraph" not in element:
            continue

        para = element["paragraph"]
        style = para.get("paragraphStyle", {})

        paragraphs.append({
            "element_index": i,
            "start_index": element.get("startIndex", 0),
            "end_index": element.get("endIndex", 0),
            "named_style": style.get("namedStyleType", "NORMAL_TEXT"),
        })

    return paragraphs


# =============================================================================
# TABLE CELL ADDRESSING
# =============================================================================


def get_table_cell_range(
    doc_data: dict[str, Any], table_index: int, row: int, col: int
) -> tuple[int, int]:
    """
    Get the byte offset range for a specific table cell's content area.

    The content area starts at the first paragraph inside the cell
    (typically cell.startIndex + 1) and ends at cell.endIndex.

    Args:
        doc_data: Raw document data from Google Docs API
        table_index: Which table (0-based)
        row: Row index (0-based)
        col: Column index (0-based)

    Returns:
        Tuple of (content_start_index, cell_end_index)

    Raises:
        IndexError: If table, row, or column index is out of range
    """
    body = doc_data.get("body", {})
    content = body.get("content", [])

    current_table = 0
    for element in content:
        if "table" not in element:
            continue
        if current_table == table_index:
            table = element["table"]
            table_rows = table.get("tableRows", [])
            if row >= len(table_rows):
                raise IndexError(
                    f"Row {row} out of range (table has {len(table_rows)} rows)"
                )
            cells = table_rows[row].get("tableCells", [])
            if col >= len(cells):
                raise IndexError(
                    f"Column {col} out of range (row has {len(cells)} columns)"
                )
            cell = cells[col]
            cell_end = cell.get("endIndex", 0)
            # Content starts at first paragraph's startIndex inside the cell
            cell_content = cell.get("content", [])
            if cell_content:
                content_start = cell_content[0].get("startIndex", cell.get("startIndex", 0) + 1)
            else:
                content_start = cell.get("startIndex", 0) + 1
            return (content_start, cell_end)
        current_table += 1

    raise IndexError(f"Table {table_index} not found (document has {current_table} tables)")


# =============================================================================
# HEADER / FOOTER
# =============================================================================


def find_header_footer_ids(doc_data: dict[str, Any]) -> dict[str, str | None]:
    """
    Extract header and footer IDs from the document style.

    Args:
        doc_data: Raw document data from Google Docs API

    Returns:
        Dict with keys: default_header_id, default_footer_id,
        first_page_header_id, first_page_footer_id,
        even_page_header_id, even_page_footer_id
    """
    doc_style = doc_data.get("documentStyle", {})

    return {
        "default_header_id": doc_style.get("defaultHeaderId"),
        "default_footer_id": doc_style.get("defaultFooterId"),
        "first_page_header_id": doc_style.get("firstPageHeaderId"),
        "first_page_footer_id": doc_style.get("firstPageFooterId"),
        "even_page_header_id": doc_style.get("evenPageHeaderId"),
        "even_page_footer_id": doc_style.get("evenPageFooterId"),
    }


# =============================================================================
# TEXT EXTRACTION
# =============================================================================


def _extract_text_from_elements(elements: list[dict[str, Any]]) -> str:
    """Recursively extract text from structural elements."""
    parts: list[str] = []
    for element in elements:
        if "paragraph" in element:
            para = element["paragraph"]
            for pe in para.get("elements", []):
                if "textRun" in pe:
                    parts.append(pe["textRun"].get("content", ""))
                elif "inlineObjectElement" in pe:
                    parts.append("[image]")
        elif "table" in element:
            table = element["table"]
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    parts.append(_extract_text_from_elements(cell.get("content", [])))
        elif "tableOfContents" in element:
            toc_content = element["tableOfContents"].get("content", [])
            parts.append(_extract_text_from_elements(toc_content))
    return "".join(parts)


def extract_doc_text(doc_data: dict[str, Any]) -> str:
    """
    Extract all text content from the document body.

    Walks body.content[] and concatenates all textRun content.
    Table cell text is included inline.

    Args:
        doc_data: Raw document data from Google Docs API

    Returns:
        Full text content of the document
    """
    body = doc_data.get("body", {})
    content = body.get("content", [])
    return _extract_text_from_elements(content)


# =============================================================================
# TABLE DEBUG INFO
# =============================================================================


def get_table_debug_info(
    doc_data: dict[str, Any], table_index: int
) -> dict[str, Any]:
    """
    Get detailed debug information about a specific table.

    Returns cell-by-cell content, positions, and merge spans.

    Args:
        doc_data: Raw document data from Google Docs API
        table_index: Which table to inspect (0-based)

    Returns:
        Dict with table dimensions and per-cell details

    Raises:
        IndexError: If table_index is out of range
    """
    body = doc_data.get("body", {})
    content = body.get("content", [])

    current_table = 0
    for element in content:
        if "table" not in element:
            continue
        if current_table == table_index:
            table = element["table"]
            table_rows = table.get("tableRows", [])
            num_rows = len(table_rows)
            num_cols = len(table_rows[0].get("tableCells", [])) if table_rows else 0

            cells: list[list[dict[str, Any]]] = []
            for r, row in enumerate(table_rows):
                row_cells: list[dict[str, Any]] = []
                for c, cell in enumerate(row.get("tableCells", [])):
                    cell_text = _extract_text_from_elements(cell.get("content", []))
                    cell_style = cell.get("tableCellStyle", {})
                    row_cells.append({
                        "row": r,
                        "col": c,
                        "content": cell_text.rstrip("\n"),
                        "start_index": cell.get("startIndex", 0),
                        "end_index": cell.get("endIndex", 0),
                        "row_span": cell_style.get("rowSpan", 1),
                        "col_span": cell_style.get("columnSpan", 1),
                    })
                cells.append(row_cells)

            return {
                "table_index": table_index,
                "start_index": element.get("startIndex", 0),
                "end_index": element.get("endIndex", 0),
                "rows": num_rows,
                "columns": num_cols,
                "cells": cells,
            }
        current_table += 1

    raise IndexError(f"Table {table_index} not found (document has {current_table} tables)")


# =============================================================================
# COLOR CONVERSION
# =============================================================================


def hex_to_rgb_color(hex_str: str) -> dict[str, Any]:
    """
    Convert hex color string to Google Docs API OptionalColor format.

    Args:
        hex_str: Color as "#RRGGBB" (e.g., "#FF0000" for red)

    Returns:
        OptionalColor dict: {"color": {"rgbColor": {"red": float, "green": float, "blue": float}}}
    """
    hex_str = hex_str.lstrip("#")
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: #{hex_str}. Expected #RRGGBB format.")

    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0

    return {
        "color": {
            "rgbColor": {"red": r, "green": g, "blue": b}
        }
    }
