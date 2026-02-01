"""
Google Docs Helper Functions

This module provides utility functions for common Google Docs operations
to simplify the implementation of document editing tools.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def _normalize_color(
    color: Optional[str], param_name: str
) -> Optional[Dict[str, float]]:
    """
    Normalize a user-supplied color into Docs API rgbColor format.

    Supports only hex strings in the form "#RRGGBB".
    """
    if color is None:
        return None

    if not isinstance(color, str):
        raise ValueError(f"{param_name} must be a hex string like '#RRGGBB'")

    if len(color) != 7 or not color.startswith("#"):
        raise ValueError(f"{param_name} must be a hex string like '#RRGGBB'")

    hex_color = color[1:]
    if any(c not in "0123456789abcdefABCDEF" for c in hex_color):
        raise ValueError(f"{param_name} must be a hex string like '#RRGGBB'")

    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return {"red": r, "green": g, "blue": b}


def build_text_style(
    bold: bool = None,
    italic: bool = None,
    underline: bool = None,
    font_size: int = None,
    font_family: str = None,
    text_color: str = None,
    background_color: str = None,
) -> tuple[Dict[str, Any], list[str]]:
    """
    Build text style object for Google Docs API requests.

    Args:
        bold: Whether text should be bold
        italic: Whether text should be italic
        underline: Whether text should be underlined
        font_size: Font size in points
        font_family: Font family name
        text_color: Text color as hex string "#RRGGBB"
        background_color: Background (highlight) color as hex string "#RRGGBB"

    Returns:
        Tuple of (text_style_dict, list_of_field_names)
    """
    text_style = {}
    fields = []

    if bold is not None:
        text_style["bold"] = bold
        fields.append("bold")

    if italic is not None:
        text_style["italic"] = italic
        fields.append("italic")

    if underline is not None:
        text_style["underline"] = underline
        fields.append("underline")

    if font_size is not None:
        text_style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
        fields.append("fontSize")

    if font_family is not None:
        text_style["weightedFontFamily"] = {"fontFamily": font_family}
        fields.append("weightedFontFamily")

    if text_color is not None:
        rgb = _normalize_color(text_color, "text_color")
        text_style["foregroundColor"] = {"color": {"rgbColor": rgb}}
        fields.append("foregroundColor")

    if background_color is not None:
        rgb = _normalize_color(background_color, "background_color")
        text_style["backgroundColor"] = {"color": {"rgbColor": rgb}}
        fields.append("backgroundColor")

    return text_style, fields


def create_insert_text_request(index: int, text: str) -> Dict[str, Any]:
    """
    Create an insertText request for Google Docs API.

    Args:
        index: Position to insert text
        text: Text to insert

    Returns:
        Dictionary representing the insertText request
    """
    return {"insertText": {"location": {"index": index}, "text": text}}


def create_insert_text_segment_request(
    index: int, text: str, segment_id: str
) -> Dict[str, Any]:
    """
    Create an insertText request for Google Docs API with segmentId (for headers/footers).

    Args:
        index: Position to insert text
        text: Text to insert
        segment_id: Segment ID (for targeting headers/footers)

    Returns:
        Dictionary representing the insertText request with segmentId
    """
    return {
        "insertText": {
            "location": {"segmentId": segment_id, "index": index},
            "text": text,
        }
    }


def create_delete_range_request(start_index: int, end_index: int) -> Dict[str, Any]:
    """
    Create a deleteContentRange request for Google Docs API.

    Args:
        start_index: Start position of content to delete
        end_index: End position of content to delete

    Returns:
        Dictionary representing the deleteContentRange request
    """
    return {
        "deleteContentRange": {
            "range": {"startIndex": start_index, "endIndex": end_index}
        }
    }


def create_format_text_request(
    start_index: int,
    end_index: int,
    bold: bool = None,
    italic: bool = None,
    underline: bool = None,
    font_size: int = None,
    font_family: str = None,
    text_color: str = None,
    background_color: str = None,
) -> Optional[Dict[str, Any]]:
    """
    Create an updateTextStyle request for Google Docs API.

    Args:
        start_index: Start position of text to format
        end_index: End position of text to format
        bold: Whether text should be bold
        italic: Whether text should be italic
        underline: Whether text should be underlined
        font_size: Font size in points
        font_family: Font family name
        text_color: Text color as hex string "#RRGGBB"
        background_color: Background (highlight) color as hex string "#RRGGBB"

    Returns:
        Dictionary representing the updateTextStyle request, or None if no styles provided
    """
    text_style, fields = build_text_style(
        bold, italic, underline, font_size, font_family, text_color, background_color
    )

    if not text_style:
        return None

    return {
        "updateTextStyle": {
            "range": {"startIndex": start_index, "endIndex": end_index},
            "textStyle": text_style,
            "fields": ",".join(fields),
        }
    }


def create_find_replace_request(
    find_text: str, replace_text: str, match_case: bool = False
) -> Dict[str, Any]:
    """
    Create a replaceAllText request for Google Docs API.

    Args:
        find_text: Text to find
        replace_text: Text to replace with
        match_case: Whether to match case exactly

    Returns:
        Dictionary representing the replaceAllText request
    """
    return {
        "replaceAllText": {
            "containsText": {"text": find_text, "matchCase": match_case},
            "replaceText": replace_text,
        }
    }


def create_insert_table_request(index: int, rows: int, columns: int) -> Dict[str, Any]:
    """
    Create an insertTable request for Google Docs API.

    Args:
        index: Position to insert table
        rows: Number of rows
        columns: Number of columns

    Returns:
        Dictionary representing the insertTable request
    """
    return {
        "insertTable": {"location": {"index": index}, "rows": rows, "columns": columns}
    }


def create_insert_page_break_request(index: int) -> Dict[str, Any]:
    """
    Create an insertPageBreak request for Google Docs API.

    Args:
        index: Position to insert page break

    Returns:
        Dictionary representing the insertPageBreak request
    """
    return {"insertPageBreak": {"location": {"index": index}}}


def create_insert_image_request(
    index: int, image_uri: str, width: int = None, height: int = None
) -> Dict[str, Any]:
    """
    Create an insertInlineImage request for Google Docs API.

    Args:
        index: Position to insert image
        image_uri: URI of the image (Drive URL or public URL)
        width: Image width in points
        height: Image height in points

    Returns:
        Dictionary representing the insertInlineImage request
    """
    request = {"insertInlineImage": {"location": {"index": index}, "uri": image_uri}}

    # Add size properties if specified
    object_size = {}
    if width is not None:
        object_size["width"] = {"magnitude": width, "unit": "PT"}
    if height is not None:
        object_size["height"] = {"magnitude": height, "unit": "PT"}

    if object_size:
        request["insertInlineImage"]["objectSize"] = object_size

    return request


def create_bullet_list_request(
    start_index: int, end_index: int, list_type: str = "UNORDERED"
) -> Dict[str, Any]:
    """
    Create a createParagraphBullets request for Google Docs API.

    Args:
        start_index: Start of text range to convert to list
        end_index: End of text range to convert to list
        list_type: Type of list ("UNORDERED" or "ORDERED")

    Returns:
        Dictionary representing the createParagraphBullets request
    """
    bullet_preset = (
        "BULLET_DISC_CIRCLE_SQUARE"
        if list_type == "UNORDERED"
        else "NUMBERED_DECIMAL_ALPHA_ROMAN"
    )

    return {
        "createParagraphBullets": {
            "range": {"startIndex": start_index, "endIndex": end_index},
            "bulletPreset": bullet_preset,
        }
    }


def create_delete_paragraph_bullets_request(
    start_index: int, end_index: int
) -> Dict[str, Any]:
    """
    Create a deleteParagraphBullets request for Google Docs API.

    Args:
        start_index: Start of text range to remove bullets from
        end_index: End of text range to remove bullets from

    Returns:
        Dictionary representing the deleteParagraphBullets request
    """
    return {
        "deleteParagraphBullets": {
            "range": {"startIndex": start_index, "endIndex": end_index}
        }
    }


# ==============================================================================
# TABLE ROW/COLUMN MANIPULATION HELPERS
# ==============================================================================


def create_insert_table_row_request(
    table_start_index: int, row_index: int, insert_below: bool = True
) -> Dict[str, Any]:
    """
    Create an insertTableRow request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts (from find_tables)
        row_index: The row index to insert relative to (0-based)
        insert_below: If True, insert below the specified row; if False, insert above

    Returns:
        Dictionary representing the insertTableRow request
    """
    return {
        "insertTableRow": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": 0,
            },
            "insertBelow": insert_below,
        }
    }


def create_delete_table_row_request(
    table_start_index: int, row_index: int
) -> Dict[str, Any]:
    """
    Create a deleteTableRow request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts (from find_tables)
        row_index: The row index to delete (0-based)

    Returns:
        Dictionary representing the deleteTableRow request
    """
    return {
        "deleteTableRow": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": 0,
            }
        }
    }


def create_insert_table_column_request(
    table_start_index: int, column_index: int, insert_right: bool = True
) -> Dict[str, Any]:
    """
    Create an insertTableColumn request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts (from find_tables)
        column_index: The column index to insert relative to (0-based)
        insert_right: If True, insert to the right; if False, insert to the left

    Returns:
        Dictionary representing the insertTableColumn request
    """
    return {
        "insertTableColumn": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": 0,
                "columnIndex": column_index,
            },
            "insertRight": insert_right,
        }
    }


def create_delete_table_column_request(
    table_start_index: int, column_index: int
) -> Dict[str, Any]:
    """
    Create a deleteTableColumn request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts (from find_tables)
        column_index: The column index to delete (0-based)

    Returns:
        Dictionary representing the deleteTableColumn request
    """
    return {
        "deleteTableColumn": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": 0,
                "columnIndex": column_index,
            }
        }
    }


def create_update_table_cell_style_request(
    table_start_index: int,
    row_index: int,
    column_index: int,
    background_color: Optional[str] = None,
    padding_top: Optional[float] = None,
    padding_bottom: Optional[float] = None,
    padding_left: Optional[float] = None,
    padding_right: Optional[float] = None,
    border_width: Optional[float] = None,
    border_color: Optional[str] = None,
    content_alignment: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Create an updateTableCellStyle request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts
        row_index: The row index of the cell (0-based)
        column_index: The column index of the cell (0-based)
        background_color: Cell background color as hex string "#RRGGBB"
        padding_top: Top padding in points
        padding_bottom: Bottom padding in points
        padding_left: Left padding in points
        padding_right: Right padding in points
        border_width: Width of all borders in points
        border_color: Border color as hex string "#RRGGBB"
        content_alignment: Vertical alignment - "TOP", "MIDDLE", or "BOTTOM"

    Returns:
        Dictionary representing the updateTableCellStyle request, or None if no styles provided
    """
    table_cell_style = {}
    fields = []

    # Background color
    if background_color is not None:
        rgb = _normalize_color(background_color, "background_color")
        table_cell_style["backgroundColor"] = {"color": {"rgbColor": rgb}}
        fields.append("backgroundColor")

    # Padding
    if padding_top is not None:
        table_cell_style["paddingTop"] = {"magnitude": padding_top, "unit": "PT"}
        fields.append("paddingTop")

    if padding_bottom is not None:
        table_cell_style["paddingBottom"] = {"magnitude": padding_bottom, "unit": "PT"}
        fields.append("paddingBottom")

    if padding_left is not None:
        table_cell_style["paddingLeft"] = {"magnitude": padding_left, "unit": "PT"}
        fields.append("paddingLeft")

    if padding_right is not None:
        table_cell_style["paddingRight"] = {"magnitude": padding_right, "unit": "PT"}
        fields.append("paddingRight")

    # Content alignment
    if content_alignment is not None:
        valid_alignments = ["TOP", "MIDDLE", "BOTTOM"]
        if content_alignment.upper() not in valid_alignments:
            raise ValueError(
                f"content_alignment must be one of {valid_alignments}, got '{content_alignment}'"
            )
        table_cell_style["contentAlignment"] = content_alignment.upper()
        fields.append("contentAlignment")

    # Border styling (applies to all borders)
    if border_width is not None or border_color is not None:
        border_style = {}
        if border_width is not None:
            border_style["width"] = {"magnitude": border_width, "unit": "PT"}
        if border_color is not None:
            rgb = _normalize_color(border_color, "border_color")
            border_style["color"] = {"color": {"rgbColor": rgb}}
        border_style["dashStyle"] = "SOLID"

        # Apply to all four borders
        for border_name in ["borderTop", "borderBottom", "borderLeft", "borderRight"]:
            table_cell_style[border_name] = border_style
            fields.append(border_name)

    if not table_cell_style:
        return None

    return {
        "updateTableCellStyle": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": column_index,
            },
            "tableCellStyle": table_cell_style,
            "fields": ",".join(fields),
        }
    }


# ==============================================================================
# HEADER/FOOTER DELETION HELPERS
# ==============================================================================


def create_delete_header_request(header_id: str) -> Dict[str, Any]:
    """
    Create a deleteHeader request for Google Docs API.

    Args:
        header_id: The ID of the header to delete (e.g., "kix.abc123")

    Returns:
        Dictionary representing the deleteHeader request
    """
    return {"deleteHeader": {"headerId": header_id}}


def create_delete_footer_request(footer_id: str) -> Dict[str, Any]:
    """
    Create a deleteFooter request for Google Docs API.

    Args:
        footer_id: The ID of the footer to delete (e.g., "kix.abc123")

    Returns:
        Dictionary representing the deleteFooter request
    """
    return {"deleteFooter": {"footerId": footer_id}}


# ==============================================================================
# ADVANCED TABLE OPERATIONS HELPERS
# ==============================================================================


def create_merge_table_cells_request(
    table_start_index: int,
    start_row: int,
    start_col: int,
    row_span: int,
    col_span: int,
) -> Dict[str, Any]:
    """
    Create a mergeTableCells request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts
        start_row: Starting row index for the merge (0-based)
        start_col: Starting column index for the merge (0-based)
        row_span: Number of rows to merge (must be >= 1)
        col_span: Number of columns to merge (must be >= 1)

    Returns:
        Dictionary representing the mergeTableCells request
    """
    return {
        "mergeTableCells": {
            "tableRange": {
                "tableCellLocation": {
                    "tableStartLocation": {"index": table_start_index},
                    "rowIndex": start_row,
                    "columnIndex": start_col,
                },
                "rowSpan": row_span,
                "columnSpan": col_span,
            }
        }
    }


def create_unmerge_table_cells_request(
    table_start_index: int,
    row_index: int,
    col_index: int,
    row_span: int,
    col_span: int,
) -> Dict[str, Any]:
    """
    Create an unmergeTableCells request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts
        row_index: Row index of the merged cell (0-based)
        col_index: Column index of the merged cell (0-based)
        row_span: Number of rows the merged cell spans
        col_span: Number of columns the merged cell spans

    Returns:
        Dictionary representing the unmergeTableCells request
    """
    return {
        "unmergeTableCells": {
            "tableRange": {
                "tableCellLocation": {
                    "tableStartLocation": {"index": table_start_index},
                    "rowIndex": row_index,
                    "columnIndex": col_index,
                },
                "rowSpan": row_span,
                "columnSpan": col_span,
            }
        }
    }


def create_update_table_row_style_request(
    table_start_index: int,
    row_indices: list[int],
    min_row_height: Optional[float] = None,
    prevent_overflow: Optional[bool] = None,
) -> Optional[Dict[str, Any]]:
    """
    Create an updateTableRowStyle request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts
        row_indices: List of row indices to update (0-based)
        min_row_height: Minimum row height in points
        prevent_overflow: Whether to prevent row content from overflowing

    Returns:
        Dictionary representing the updateTableRowStyle request, or None if no styles provided
    """
    table_row_style = {}
    fields = []

    if min_row_height is not None:
        table_row_style["minRowHeight"] = {"magnitude": min_row_height, "unit": "PT"}
        fields.append("minRowHeight")

    if prevent_overflow is not None:
        table_row_style["preventOverflow"] = prevent_overflow
        fields.append("preventOverflow")

    if not table_row_style:
        return None

    return {
        "updateTableRowStyle": {
            "tableStartLocation": {"index": table_start_index},
            "rowIndices": row_indices,
            "tableRowStyle": table_row_style,
            "fields": ",".join(fields),
        }
    }


def create_update_table_column_properties_request(
    table_start_index: int,
    column_indices: list[int],
    width: Optional[float] = None,
    width_type: str = "FIXED_WIDTH",
) -> Optional[Dict[str, Any]]:
    """
    Create an updateTableColumnProperties request for Google Docs API.

    Args:
        table_start_index: The document index where the table starts
        column_indices: List of column indices to update (0-based)
        width: Column width in points (required if width_type is FIXED_WIDTH)
        width_type: Width type - "EVENLY_DISTRIBUTED" or "FIXED_WIDTH"

    Returns:
        Dictionary representing the updateTableColumnProperties request, or None if invalid
    """
    valid_width_types = ["EVENLY_DISTRIBUTED", "FIXED_WIDTH"]
    if width_type not in valid_width_types:
        raise ValueError(f"width_type must be one of {valid_width_types}, got '{width_type}'")

    table_column_properties = {"widthType": width_type}
    fields = ["widthType"]

    if width is not None:
        table_column_properties["width"] = {"magnitude": width, "unit": "PT"}
        fields.append("width")

    return {
        "updateTableColumnProperties": {
            "tableStartLocation": {"index": table_start_index},
            "columnIndices": column_indices,
            "tableColumnProperties": table_column_properties,
            "fields": ",".join(fields),
        }
    }


def create_pin_table_header_rows_request(
    table_start_index: int,
    pinned_header_rows_count: int,
) -> Dict[str, Any]:
    """
    Create a pinTableHeaderRows request for Google Docs API.

    This pins the specified number of rows as repeating header rows that
    appear at the top of each page when the table spans multiple pages.

    Args:
        table_start_index: The document index where the table starts
        pinned_header_rows_count: Number of rows to pin as headers (0 to unpin all)

    Returns:
        Dictionary representing the pinTableHeaderRows request
    """
    return {
        "pinTableHeaderRows": {
            "tableStartLocation": {"index": table_start_index},
            "pinnedHeaderRowsCount": pinned_header_rows_count,
        }
    }


def validate_operation(operation: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate a batch operation dictionary.

    Args:
        operation: Operation dictionary to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    op_type = operation.get("type")
    if not op_type:
        return False, "Missing 'type' field"

    # Validate required fields for each operation type
    required_fields = {
        "insert_text": ["index", "text"],
        "delete_text": ["start_index", "end_index"],
        "replace_text": ["start_index", "end_index", "text"],
        "format_text": ["start_index", "end_index"],
        "insert_table": ["index", "rows", "columns"],
        "insert_page_break": ["index"],
        "find_replace": ["find_text", "replace_text"],
    }

    if op_type not in required_fields:
        return False, f"Unsupported operation type: {op_type or 'None'}"

    for field in required_fields[op_type]:
        if field not in operation:
            return False, f"Missing required field: {field}"

    return True, ""
