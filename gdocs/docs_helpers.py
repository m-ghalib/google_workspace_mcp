"""
Google Docs REST API Request Builders

Builds batchUpdate request dicts for the Google Docs REST API.
Each function returns a single request dict ready for inclusion in
a batchUpdate requests list.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


# =============================================================================
# RED TOOL BUILDERS (unchanged — used by TableOperationManager)
# =============================================================================


def create_unmerge_table_cells_request(
    table_start_index: int,
    row_index: int,
    col_index: int,
    row_span: int,
    col_span: int,
) -> dict[str, Any]:
    """Create an unmergeTableCells request for Google Docs API."""
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
    min_row_height: float | None = None,
    prevent_overflow: bool | None = None,
) -> dict[str, Any] | None:
    """Create an updateTableRowStyle request for Google Docs API."""
    table_row_style: dict[str, Any] = {}
    fields: list[str] = []

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


def create_pin_table_header_rows_request(
    table_start_index: int,
    pinned_header_rows_count: int,
) -> dict[str, Any]:
    """Create a pinTableHeaderRows request for Google Docs API."""
    return {
        "pinTableHeaderRows": {
            "tableStartLocation": {"index": table_start_index},
            "pinnedHeaderRowsCount": pinned_header_rows_count,
        }
    }


# =============================================================================
# TEXT OPERATIONS
# =============================================================================


def create_insert_text_request(
    text: str,
    index: int | None = None,
    segment_id: str | None = None,
) -> dict[str, Any]:
    """Create an insertText request.

    Args:
        text: Text to insert
        index: Byte offset to insert at. None = end of segment.
        segment_id: Header/footer/footnote ID. None = body.
    """
    req: dict[str, Any] = {"text": text}
    if index is not None:
        location: dict[str, Any] = {"index": index}
        if segment_id:
            location["segmentId"] = segment_id
        req["location"] = location
    else:
        req["endOfSegmentLocation"] = {"segmentId": segment_id or ""}
    return {"insertText": req}


def create_delete_content_range_request(
    start_index: int,
    end_index: int,
    segment_id: str | None = None,
) -> dict[str, Any]:
    """Create a deleteContentRange request."""
    range_dict: dict[str, Any] = {
        "startIndex": start_index,
        "endIndex": end_index,
    }
    if segment_id:
        range_dict["segmentId"] = segment_id
    return {"deleteContentRange": {"range": range_dict}}


def create_replace_all_text_request(
    find_text: str,
    replace_text: str,
    match_case: bool = False,
) -> dict[str, Any]:
    """Create a replaceAllText request."""
    return {
        "replaceAllText": {
            "containsText": {
                "text": find_text,
                "matchCase": match_case,
            },
            "replaceText": replace_text,
        }
    }


def create_update_text_style_request(
    start_index: int,
    end_index: int,
    text_style: dict[str, Any],
    fields: str,
    segment_id: str | None = None,
) -> dict[str, Any]:
    """Create an updateTextStyle request."""
    range_dict: dict[str, Any] = {
        "startIndex": start_index,
        "endIndex": end_index,
    }
    if segment_id:
        range_dict["segmentId"] = segment_id
    return {
        "updateTextStyle": {
            "textStyle": text_style,
            "fields": fields,
            "range": range_dict,
        }
    }


# =============================================================================
# PARAGRAPH OPERATIONS
# =============================================================================


def create_update_paragraph_style_request(
    start_index: int,
    end_index: int,
    paragraph_style: dict[str, Any],
    fields: str,
    segment_id: str | None = None,
) -> dict[str, Any]:
    """Create an updateParagraphStyle request."""
    range_dict: dict[str, Any] = {
        "startIndex": start_index,
        "endIndex": end_index,
    }
    if segment_id:
        range_dict["segmentId"] = segment_id
    return {
        "updateParagraphStyle": {
            "paragraphStyle": paragraph_style,
            "fields": fields,
            "range": range_dict,
        }
    }


def create_paragraph_bullets_request(
    start_index: int,
    end_index: int,
    bullet_preset: str,
) -> dict[str, Any]:
    """Create a createParagraphBullets request.

    Args:
        start_index: Start of paragraph range
        end_index: End of paragraph range
        bullet_preset: e.g. "BULLET_DISC_CIRCLE_SQUARE" or "NUMBERED_DECIMAL_ALPHA_ROMAN"
    """
    return {
        "createParagraphBullets": {
            "range": {
                "startIndex": start_index,
                "endIndex": end_index,
            },
            "bulletPreset": bullet_preset,
        }
    }


def create_delete_paragraph_bullets_request(
    start_index: int,
    end_index: int,
) -> dict[str, Any]:
    """Create a deleteParagraphBullets request."""
    return {
        "deleteParagraphBullets": {
            "range": {
                "startIndex": start_index,
                "endIndex": end_index,
            }
        }
    }


# =============================================================================
# TABLE OPERATIONS
# =============================================================================


def create_insert_table_request(
    rows: int,
    columns: int,
    index: int | None = None,
) -> dict[str, Any]:
    """Create an insertTable request.

    Args:
        rows: Number of rows
        columns: Number of columns
        index: Byte offset for insertion. None = end of body.
    """
    req: dict[str, Any] = {"rows": rows, "columns": columns}
    if index is not None:
        req["location"] = {"index": index}
    else:
        req["endOfSegmentLocation"] = {"segmentId": ""}
    return {"insertTable": req}


def create_insert_table_row_request(
    table_start_index: int,
    row_index: int,
    col_index: int = 0,
    insert_below: bool = True,
) -> dict[str, Any]:
    """Create an insertTableRow request."""
    return {
        "insertTableRow": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": col_index,
            },
            "insertBelow": insert_below,
        }
    }


def create_delete_table_row_request(
    table_start_index: int,
    row_index: int,
    col_index: int = 0,
) -> dict[str, Any]:
    """Create a deleteTableRow request."""
    return {
        "deleteTableRow": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": col_index,
            }
        }
    }


def create_insert_table_column_request(
    table_start_index: int,
    row_index: int = 0,
    col_index: int = 0,
    insert_right: bool = True,
) -> dict[str, Any]:
    """Create an insertTableColumn request."""
    return {
        "insertTableColumn": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": col_index,
            },
            "insertRight": insert_right,
        }
    }


def create_delete_table_column_request(
    table_start_index: int,
    row_index: int = 0,
    col_index: int = 0,
) -> dict[str, Any]:
    """Create a deleteTableColumn request."""
    return {
        "deleteTableColumn": {
            "tableCellLocation": {
                "tableStartLocation": {"index": table_start_index},
                "rowIndex": row_index,
                "columnIndex": col_index,
            }
        }
    }


def create_merge_table_cells_request(
    table_start_index: int,
    row_index: int,
    col_index: int,
    row_span: int,
    col_span: int,
) -> dict[str, Any]:
    """Create a mergeTableCells request.

    BUG FIX: REST API supports proper rectangular merge, unlike Apps Script's
    cell.merge() which only merged adjacent cells sequentially.
    """
    return {
        "mergeTableCells": {
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


def create_update_table_cell_style_request(
    table_start_index: int,
    row_index: int,
    col_index: int,
    table_cell_style: dict[str, Any],
    fields: str,
    row_span: int = 1,
    col_span: int = 1,
) -> dict[str, Any]:
    """Create an updateTableCellStyle request."""
    return {
        "updateTableCellStyle": {
            "tableRange": {
                "tableCellLocation": {
                    "tableStartLocation": {"index": table_start_index},
                    "rowIndex": row_index,
                    "columnIndex": col_index,
                },
                "rowSpan": row_span,
                "columnSpan": col_span,
            },
            "tableCellStyle": table_cell_style,
            "fields": fields,
        }
    }


def create_update_table_column_properties_request(
    table_start_index: int,
    column_indices: list[int],
    width: float | None = None,
    width_type: str = "FIXED_WIDTH",
) -> dict[str, Any]:
    """Create an updateTableColumnProperties request."""
    props: dict[str, Any] = {"widthType": width_type}
    fields = ["widthType"]

    if width is not None:
        props["width"] = {"magnitude": width, "unit": "PT"}
        fields.append("width")

    return {
        "updateTableColumnProperties": {
            "tableStartLocation": {"index": table_start_index},
            "columnIndices": column_indices,
            "tableColumnProperties": props,
            "fields": ",".join(fields),
        }
    }


# =============================================================================
# STRUCTURAL OPERATIONS
# =============================================================================


def create_insert_page_break_request(
    index: int | None = None,
) -> dict[str, Any]:
    """Create an insertPageBreak request."""
    req: dict[str, Any] = {}
    if index is not None:
        req["location"] = {"index": index}
    else:
        req["endOfSegmentLocation"] = {"segmentId": ""}
    return {"insertPageBreak": req}


def create_insert_inline_image_request(
    uri: str,
    index: int | None = None,
    width: float | None = None,
    height: float | None = None,
) -> dict[str, Any]:
    """Create an insertInlineImage request."""
    req: dict[str, Any] = {"uri": uri}
    if index is not None:
        req["location"] = {"index": index}
    else:
        req["endOfSegmentLocation"] = {"segmentId": ""}

    if width is not None or height is not None:
        size: dict[str, Any] = {}
        if width is not None:
            size["width"] = {"magnitude": width, "unit": "PT"}
        if height is not None:
            size["height"] = {"magnitude": height, "unit": "PT"}
        req["objectSize"] = size

    return {"insertInlineImage": req}


# =============================================================================
# HEADER / FOOTER OPERATIONS
# =============================================================================


def create_header_request(
    header_type: str = "DEFAULT",
) -> dict[str, Any]:
    """Create a createHeader request.

    BUG FIX: Now supports FIRST_PAGE and EVEN_PAGE types
    (Apps Script could only handle DEFAULT).
    """
    return {"createHeader": {"type": header_type}}


def create_footer_request(
    footer_type: str = "DEFAULT",
) -> dict[str, Any]:
    """Create a createFooter request."""
    return {"createFooter": {"type": footer_type}}


def create_delete_header_request(header_id: str) -> dict[str, Any]:
    """Create a deleteHeader request."""
    return {"deleteHeader": {"headerId": header_id}}


def create_delete_footer_request(footer_id: str) -> dict[str, Any]:
    """Create a deleteFooter request."""
    return {"deleteFooter": {"footerId": footer_id}}


# =============================================================================
# STYLE HELPERS — convert tool params to API format + FieldMask
# =============================================================================


def build_text_style(
    bold: bool | None = None,
    italic: bool | None = None,
    underline: bool | None = None,
    font_size: float | None = None,
    font_family: str | None = None,
    text_color: str | None = None,
    background_color: str | None = None,
) -> tuple[dict[str, Any], str]:
    """Build a TextStyle dict and FieldMask from tool-level parameters.

    Converts hex colors to OptionalColor and font_size to Dimension.

    Returns:
        Tuple of (text_style dict, comma-separated fields mask)
    """
    from gdocs.docs_structure import hex_to_rgb_color

    style: dict[str, Any] = {}
    fields: list[str] = []

    if bold is not None:
        style["bold"] = bold
        fields.append("bold")
    if italic is not None:
        style["italic"] = italic
        fields.append("italic")
    if underline is not None:
        style["underline"] = underline
        fields.append("underline")
    if font_size is not None:
        style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
        fields.append("fontSize")
    if font_family is not None:
        style["weightedFontFamily"] = {"fontFamily": font_family}
        fields.append("weightedFontFamily")
    if text_color is not None:
        style["foregroundColor"] = hex_to_rgb_color(text_color)
        fields.append("foregroundColor")
    if background_color is not None:
        style["backgroundColor"] = hex_to_rgb_color(background_color)
        fields.append("backgroundColor")

    return style, ",".join(fields)


def build_paragraph_style(
    heading_level: int | None = None,
    alignment: str | None = None,
    line_spacing: float | None = None,
    indent_first_line: float | None = None,
    indent_start: float | None = None,
    indent_end: float | None = None,
    space_above: float | None = None,
    space_below: float | None = None,
) -> tuple[dict[str, Any], str]:
    """Build a ParagraphStyle dict and FieldMask from tool-level parameters.

    Converts heading_level int to namedStyleType enum, line_spacing
    multiplier (1.0 = single) to API percentage (100), and indent/spacing
    floats to Dimension objects.

    Returns:
        Tuple of (paragraph_style dict, comma-separated fields mask)
    """
    _heading_map = {
        0: "NORMAL_TEXT",
        1: "HEADING_1",
        2: "HEADING_2",
        3: "HEADING_3",
        4: "HEADING_4",
        5: "HEADING_5",
        6: "HEADING_6",
    }

    style: dict[str, Any] = {}
    fields: list[str] = []

    if heading_level is not None:
        style["namedStyleType"] = _heading_map.get(heading_level, "NORMAL_TEXT")
        fields.append("namedStyleType")
    if alignment is not None:
        style["alignment"] = alignment.upper()
        fields.append("alignment")
    if line_spacing is not None:
        # Tool uses multiplier (1.0=single), API uses percentage (100=single)
        style["lineSpacing"] = line_spacing * 100
        fields.append("lineSpacing")
    if indent_first_line is not None:
        style["indentFirstLine"] = {"magnitude": indent_first_line, "unit": "PT"}
        fields.append("indentFirstLine")
    if indent_start is not None:
        style["indentStart"] = {"magnitude": indent_start, "unit": "PT"}
        fields.append("indentStart")
    if indent_end is not None:
        style["indentEnd"] = {"magnitude": indent_end, "unit": "PT"}
        fields.append("indentEnd")
    if space_above is not None:
        style["spaceAbove"] = {"magnitude": space_above, "unit": "PT"}
        fields.append("spaceAbove")
    if space_below is not None:
        style["spaceBelow"] = {"magnitude": space_below, "unit": "PT"}
        fields.append("spaceBelow")

    return style, ",".join(fields)


def build_table_cell_style(
    background_color: str | None = None,
    padding_top: float | None = None,
    padding_bottom: float | None = None,
    padding_left: float | None = None,
    padding_right: float | None = None,
    content_alignment: str | None = None,
) -> tuple[dict[str, Any], str]:
    """Build a TableCellStyle dict and FieldMask from tool-level parameters.

    Converts hex color to OptionalColor and padding to Dimensions.

    Returns:
        Tuple of (table_cell_style dict, comma-separated fields mask)
    """
    from gdocs.docs_structure import hex_to_rgb_color

    style: dict[str, Any] = {}
    fields: list[str] = []

    if background_color is not None:
        style["backgroundColor"] = hex_to_rgb_color(background_color)
        fields.append("backgroundColor")
    if padding_top is not None:
        style["paddingTop"] = {"magnitude": padding_top, "unit": "PT"}
        fields.append("paddingTop")
    if padding_bottom is not None:
        style["paddingBottom"] = {"magnitude": padding_bottom, "unit": "PT"}
        fields.append("paddingBottom")
    if padding_left is not None:
        style["paddingLeft"] = {"magnitude": padding_left, "unit": "PT"}
        fields.append("paddingLeft")
    if padding_right is not None:
        style["paddingRight"] = {"magnitude": padding_right, "unit": "PT"}
        fields.append("paddingRight")
    if content_alignment is not None:
        style["contentAlignment"] = content_alignment.upper()
        fields.append("contentAlignment")

    return style, ",".join(fields)
