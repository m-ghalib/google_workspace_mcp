"""
Unit tests for Google Docs REST API request builders — RED tools only.

Tests the 3 batchUpdate request types that remain on REST API
(no Apps Script equivalent):
- unmergeTableCells
- updateTableRowStyle
- pinTableHeaderRows
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from gdocs.docs_helpers import (
    create_unmerge_table_cells_request,
    create_update_table_row_style_request,
    create_pin_table_header_rows_request,
)


# ==============================================================================
# UNMERGE TABLE CELLS
# ==============================================================================


class TestUnmergeTableCellsRequest:
    """Test create_unmerge_table_cells_request helper function."""

    def test_unmerge_basic(self):
        """Test basic cell unmerge request."""
        result = create_unmerge_table_cells_request(
            table_start_index=100,
            row_index=0,
            col_index=0,
            row_span=2,
            col_span=3,
        )

        assert "unmergeTableCells" in result
        unmerge_req = result["unmergeTableCells"]
        assert "tableRange" in unmerge_req

        table_range = unmerge_req["tableRange"]
        assert table_range["rowSpan"] == 2
        assert table_range["columnSpan"] == 3

    def test_unmerge_different_positions(self):
        """Test unmerge at different positions."""
        result = create_unmerge_table_cells_request(
            table_start_index=250,
            row_index=1,
            col_index=2,
            row_span=4,
            col_span=1,
        )

        table_range = result["unmergeTableCells"]["tableRange"]
        assert table_range["tableCellLocation"]["rowIndex"] == 1
        assert table_range["tableCellLocation"]["columnIndex"] == 2

    def test_unmerge_structure(self):
        """Verify unmergeTableCells matches Google Docs API spec."""
        result = create_unmerge_table_cells_request(100, 0, 0, 2, 2)

        assert "unmergeTableCells" in result
        unmerge_req = result["unmergeTableCells"]
        assert "tableRange" in unmerge_req

        table_range = unmerge_req["tableRange"]
        assert "tableCellLocation" in table_range
        assert "rowSpan" in table_range
        assert "columnSpan" in table_range

        cell_loc = table_range["tableCellLocation"]
        assert "tableStartLocation" in cell_loc
        assert "index" in cell_loc["tableStartLocation"]
        assert "rowIndex" in cell_loc
        assert "columnIndex" in cell_loc


# ==============================================================================
# UPDATE TABLE ROW STYLE
# ==============================================================================


class TestUpdateTableRowStyleRequest:
    """Test create_update_table_row_style_request helper function."""

    def test_min_row_height_only(self):
        """Test setting only minimum row height."""
        result = create_update_table_row_style_request(
            table_start_index=100,
            row_indices=[0],
            min_row_height=36.0,
        )

        assert "updateTableRowStyle" in result
        req = result["updateTableRowStyle"]
        assert req["tableStartLocation"]["index"] == 100
        assert req["rowIndices"] == [0]
        assert req["tableRowStyle"]["minRowHeight"]["magnitude"] == 36.0
        assert req["tableRowStyle"]["minRowHeight"]["unit"] == "PT"
        assert "minRowHeight" in req["fields"]

    def test_prevent_overflow_only(self):
        """Test setting only prevent overflow."""
        result = create_update_table_row_style_request(
            table_start_index=100,
            row_indices=[0, 1],
            prevent_overflow=True,
        )

        req = result["updateTableRowStyle"]
        assert req["tableRowStyle"]["preventOverflow"] is True
        assert "preventOverflow" in req["fields"]

    def test_combined_row_style(self):
        """Test combining min height and prevent overflow."""
        result = create_update_table_row_style_request(
            table_start_index=100,
            row_indices=[0, 1, 2],
            min_row_height=48.0,
            prevent_overflow=False,
        )

        req = result["updateTableRowStyle"]
        assert req["rowIndices"] == [0, 1, 2]
        assert req["tableRowStyle"]["minRowHeight"]["magnitude"] == 48.0
        assert req["tableRowStyle"]["preventOverflow"] is False
        assert "minRowHeight" in req["fields"]
        assert "preventOverflow" in req["fields"]

    def test_no_styles_returns_none(self):
        """Test that providing no styles returns None."""
        result = create_update_table_row_style_request(
            table_start_index=100,
            row_indices=[0],
        )
        assert result is None

    def test_row_style_structure(self):
        """Verify updateTableRowStyle matches Google Docs API spec."""
        result = create_update_table_row_style_request(100, [0], min_row_height=36.0)

        assert "updateTableRowStyle" in result
        req = result["updateTableRowStyle"]
        assert "tableStartLocation" in req
        assert "index" in req["tableStartLocation"]
        assert "rowIndices" in req
        assert "tableRowStyle" in req
        assert "fields" in req


# ==============================================================================
# PIN TABLE HEADER ROWS
# ==============================================================================


class TestPinTableHeaderRowsRequest:
    """Test create_pin_table_header_rows_request helper function."""

    def test_pin_single_row(self):
        """Test pinning a single header row."""
        result = create_pin_table_header_rows_request(
            table_start_index=100,
            pinned_header_rows_count=1,
        )

        assert "pinTableHeaderRows" in result
        req = result["pinTableHeaderRows"]
        assert req["tableStartLocation"]["index"] == 100
        assert req["pinnedHeaderRowsCount"] == 1

    def test_pin_multiple_rows(self):
        """Test pinning multiple header rows."""
        result = create_pin_table_header_rows_request(
            table_start_index=100,
            pinned_header_rows_count=3,
        )

        assert result["pinTableHeaderRows"]["pinnedHeaderRowsCount"] == 3

    def test_unpin_all_rows(self):
        """Test unpinning all rows (count=0)."""
        result = create_pin_table_header_rows_request(
            table_start_index=100,
            pinned_header_rows_count=0,
        )

        assert result["pinTableHeaderRows"]["pinnedHeaderRowsCount"] == 0

    def test_pin_header_rows_structure(self):
        """Verify pinTableHeaderRows matches Google Docs API spec."""
        result = create_pin_table_header_rows_request(100, 1)

        assert "pinTableHeaderRows" in result
        req = result["pinTableHeaderRows"]
        assert "tableStartLocation" in req
        assert "index" in req["tableStartLocation"]
        assert "pinnedHeaderRowsCount" in req
