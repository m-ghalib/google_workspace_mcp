"""
Unit tests for Google Docs table operation helpers and tools.

Tests all table row/column manipulation and cell styling request builders.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from gdocs.docs_helpers import (
    create_insert_table_row_request,
    create_delete_table_row_request,
    create_insert_table_column_request,
    create_delete_table_column_request,
    create_update_table_cell_style_request,
    create_delete_paragraph_bullets_request,
    # New request builders
    create_delete_header_request,
    create_delete_footer_request,
    create_merge_table_cells_request,
    create_unmerge_table_cells_request,
    create_update_table_row_style_request,
    create_update_table_column_properties_request,
    create_pin_table_header_rows_request,
)


# ==============================================================================
# HELPER FUNCTION TESTS - Request Builders
# ==============================================================================


class TestInsertTableRowRequest:
    """Test create_insert_table_row_request helper function."""

    def test_insert_below_default(self):
        """Test inserting row below (default behavior)."""
        result = create_insert_table_row_request(100, 0)

        assert "insertTableRow" in result
        assert result["insertTableRow"]["insertBelow"] is True
        assert result["insertTableRow"]["tableCellLocation"]["tableStartLocation"]["index"] == 100
        assert result["insertTableRow"]["tableCellLocation"]["rowIndex"] == 0
        assert result["insertTableRow"]["tableCellLocation"]["columnIndex"] == 0

    def test_insert_below_explicit(self):
        """Test inserting row below with explicit True."""
        result = create_insert_table_row_request(100, 2, insert_below=True)

        assert result["insertTableRow"]["insertBelow"] is True
        assert result["insertTableRow"]["tableCellLocation"]["rowIndex"] == 2

    def test_insert_above(self):
        """Test inserting row above."""
        result = create_insert_table_row_request(100, 0, insert_below=False)

        assert result["insertTableRow"]["insertBelow"] is False

    def test_different_table_start_index(self):
        """Test with different table start indices."""
        result = create_insert_table_row_request(500, 3, True)

        assert result["insertTableRow"]["tableCellLocation"]["tableStartLocation"]["index"] == 500
        assert result["insertTableRow"]["tableCellLocation"]["rowIndex"] == 3


class TestDeleteTableRowRequest:
    """Test create_delete_table_row_request helper function."""

    def test_delete_first_row(self):
        """Test deleting the first row."""
        result = create_delete_table_row_request(100, 0)

        assert "deleteTableRow" in result
        assert result["deleteTableRow"]["tableCellLocation"]["tableStartLocation"]["index"] == 100
        assert result["deleteTableRow"]["tableCellLocation"]["rowIndex"] == 0
        assert result["deleteTableRow"]["tableCellLocation"]["columnIndex"] == 0

    def test_delete_middle_row(self):
        """Test deleting a middle row."""
        result = create_delete_table_row_request(200, 5)

        assert result["deleteTableRow"]["tableCellLocation"]["rowIndex"] == 5

    def test_different_table_start_index(self):
        """Test with different table start indices."""
        result = create_delete_table_row_request(350, 2)

        assert result["deleteTableRow"]["tableCellLocation"]["tableStartLocation"]["index"] == 350


class TestInsertTableColumnRequest:
    """Test create_insert_table_column_request helper function."""

    def test_insert_right_default(self):
        """Test inserting column to the right (default behavior)."""
        result = create_insert_table_column_request(100, 0)

        assert "insertTableColumn" in result
        assert result["insertTableColumn"]["insertRight"] is True
        assert result["insertTableColumn"]["tableCellLocation"]["tableStartLocation"]["index"] == 100
        assert result["insertTableColumn"]["tableCellLocation"]["columnIndex"] == 0
        assert result["insertTableColumn"]["tableCellLocation"]["rowIndex"] == 0

    def test_insert_right_explicit(self):
        """Test inserting column to the right with explicit True."""
        result = create_insert_table_column_request(100, 2, insert_right=True)

        assert result["insertTableColumn"]["insertRight"] is True
        assert result["insertTableColumn"]["tableCellLocation"]["columnIndex"] == 2

    def test_insert_left(self):
        """Test inserting column to the left."""
        result = create_insert_table_column_request(100, 0, insert_right=False)

        assert result["insertTableColumn"]["insertRight"] is False


class TestDeleteTableColumnRequest:
    """Test create_delete_table_column_request helper function."""

    def test_delete_first_column(self):
        """Test deleting the first column."""
        result = create_delete_table_column_request(100, 0)

        assert "deleteTableColumn" in result
        assert result["deleteTableColumn"]["tableCellLocation"]["tableStartLocation"]["index"] == 100
        assert result["deleteTableColumn"]["tableCellLocation"]["columnIndex"] == 0
        assert result["deleteTableColumn"]["tableCellLocation"]["rowIndex"] == 0

    def test_delete_middle_column(self):
        """Test deleting a middle column."""
        result = create_delete_table_column_request(200, 3)

        assert result["deleteTableColumn"]["tableCellLocation"]["columnIndex"] == 3


class TestDeleteParagraphBulletsRequest:
    """Test create_delete_paragraph_bullets_request helper function."""

    def test_basic_range(self):
        """Test deleting bullets from a range."""
        result = create_delete_paragraph_bullets_request(10, 50)

        assert "deleteParagraphBullets" in result
        assert result["deleteParagraphBullets"]["range"]["startIndex"] == 10
        assert result["deleteParagraphBullets"]["range"]["endIndex"] == 50

    def test_different_range(self):
        """Test with different index range."""
        result = create_delete_paragraph_bullets_request(100, 200)

        assert result["deleteParagraphBullets"]["range"]["startIndex"] == 100
        assert result["deleteParagraphBullets"]["range"]["endIndex"] == 200


class TestUpdateTableCellStyleRequest:
    """Test create_update_table_cell_style_request helper function."""

    def test_background_color_only(self):
        """Test setting only background color."""
        result = create_update_table_cell_style_request(
            table_start_index=100,
            row_index=0,
            column_index=0,
            background_color="#FF0000",
        )

        assert result is not None
        assert "updateTableCellStyle" in result
        assert "tableCellLocation" in result["updateTableCellStyle"]
        assert result["updateTableCellStyle"]["tableCellLocation"]["tableStartLocation"]["index"] == 100
        assert result["updateTableCellStyle"]["tableCellLocation"]["rowIndex"] == 0
        assert result["updateTableCellStyle"]["tableCellLocation"]["columnIndex"] == 0
        assert "backgroundColor" in result["updateTableCellStyle"]["tableCellStyle"]
        assert "backgroundColor" in result["updateTableCellStyle"]["fields"]

    def test_padding_settings(self):
        """Test setting padding on all sides."""
        result = create_update_table_cell_style_request(
            table_start_index=100,
            row_index=1,
            column_index=2,
            padding_top=5.0,
            padding_bottom=5.0,
            padding_left=10.0,
            padding_right=10.0,
        )

        assert result is not None
        style = result["updateTableCellStyle"]["tableCellStyle"]
        assert style["paddingTop"]["magnitude"] == 5.0
        assert style["paddingBottom"]["magnitude"] == 5.0
        assert style["paddingLeft"]["magnitude"] == 10.0
        assert style["paddingRight"]["magnitude"] == 10.0

        fields = result["updateTableCellStyle"]["fields"]
        assert "paddingTop" in fields
        assert "paddingBottom" in fields
        assert "paddingLeft" in fields
        assert "paddingRight" in fields

    def test_content_alignment(self):
        """Test setting content alignment."""
        for alignment in ["TOP", "MIDDLE", "BOTTOM"]:
            result = create_update_table_cell_style_request(
                table_start_index=100,
                row_index=0,
                column_index=0,
                content_alignment=alignment,
            )

            assert result is not None
            assert result["updateTableCellStyle"]["tableCellStyle"]["contentAlignment"] == alignment
            assert "contentAlignment" in result["updateTableCellStyle"]["fields"]

    def test_border_styling(self):
        """Test setting border width and color."""
        result = create_update_table_cell_style_request(
            table_start_index=100,
            row_index=0,
            column_index=0,
            border_width=2.0,
            border_color="#000000",
        )

        assert result is not None
        style = result["updateTableCellStyle"]["tableCellStyle"]

        # Check all four borders are set
        for border_name in ["borderTop", "borderBottom", "borderLeft", "borderRight"]:
            assert border_name in style
            assert style[border_name]["width"]["magnitude"] == 2.0
            assert "color" in style[border_name]
            assert style[border_name]["dashStyle"] == "SOLID"

    def test_no_styles_returns_none(self):
        """Test that providing no styles returns None."""
        result = create_update_table_cell_style_request(
            table_start_index=100,
            row_index=0,
            column_index=0,
        )

        assert result is None

    def test_combined_styles(self):
        """Test combining multiple style options."""
        result = create_update_table_cell_style_request(
            table_start_index=100,
            row_index=0,
            column_index=0,
            background_color="#FFFF00",
            padding_top=5.0,
            content_alignment="MIDDLE",
        )

        assert result is not None
        style = result["updateTableCellStyle"]["tableCellStyle"]
        assert "backgroundColor" in style
        assert "paddingTop" in style
        assert "contentAlignment" in style

    def test_invalid_alignment_raises(self):
        """Test that invalid alignment raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            create_update_table_cell_style_request(
                table_start_index=100,
                row_index=0,
                column_index=0,
                content_alignment="INVALID",
            )

        assert "content_alignment must be one of" in str(exc_info.value)

    def test_case_insensitive_alignment(self):
        """Test that alignment is case-insensitive."""
        result = create_update_table_cell_style_request(
            table_start_index=100,
            row_index=0,
            column_index=0,
            content_alignment="middle",  # lowercase
        )

        assert result is not None
        assert result["updateTableCellStyle"]["tableCellStyle"]["contentAlignment"] == "MIDDLE"


# ==============================================================================
# COLOR VALIDATION TESTS
# ==============================================================================


class TestColorValidation:
    """Test color validation in cell style requests."""

    def test_valid_hex_colors(self):
        """Test various valid hex color formats."""
        valid_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#AbCdEf"]

        for color in valid_colors:
            result = create_update_table_cell_style_request(
                table_start_index=100,
                row_index=0,
                column_index=0,
                background_color=color,
            )
            assert result is not None, f"Color {color} should be valid"

    def test_invalid_hex_color_no_hash(self):
        """Test that color without # raises error."""
        with pytest.raises(ValueError):
            create_update_table_cell_style_request(
                table_start_index=100,
                row_index=0,
                column_index=0,
                background_color="FF0000",  # Missing #
            )

    def test_invalid_hex_color_wrong_length(self):
        """Test that short/long hex colors raise error."""
        with pytest.raises(ValueError):
            create_update_table_cell_style_request(
                table_start_index=100,
                row_index=0,
                column_index=0,
                background_color="#FFF",  # Too short
            )

    def test_invalid_hex_color_non_hex_chars(self):
        """Test that non-hex characters raise error."""
        with pytest.raises(ValueError):
            create_update_table_cell_style_request(
                table_start_index=100,
                row_index=0,
                column_index=0,
                background_color="#GGGGGG",  # Invalid hex chars
            )


# ==============================================================================
# INTEGRATION STRUCTURE TESTS
# ==============================================================================


class TestRequestStructureIntegrity:
    """Test that all requests have correct Google Docs API structure."""

    def test_insert_row_structure(self):
        """Verify insertTableRow matches Google Docs API spec."""
        result = create_insert_table_row_request(100, 1, True)

        # Verify required fields exist
        assert "insertTableRow" in result
        insert_req = result["insertTableRow"]
        assert "tableCellLocation" in insert_req
        assert "insertBelow" in insert_req

        # Verify tableCellLocation structure
        cell_loc = insert_req["tableCellLocation"]
        assert "tableStartLocation" in cell_loc
        assert "index" in cell_loc["tableStartLocation"]
        assert "rowIndex" in cell_loc
        assert "columnIndex" in cell_loc

    def test_delete_row_structure(self):
        """Verify deleteTableRow matches Google Docs API spec."""
        result = create_delete_table_row_request(100, 1)

        assert "deleteTableRow" in result
        delete_req = result["deleteTableRow"]
        assert "tableCellLocation" in delete_req

        cell_loc = delete_req["tableCellLocation"]
        assert "tableStartLocation" in cell_loc
        assert "rowIndex" in cell_loc

    def test_insert_column_structure(self):
        """Verify insertTableColumn matches Google Docs API spec."""
        result = create_insert_table_column_request(100, 1, False)

        assert "insertTableColumn" in result
        insert_req = result["insertTableColumn"]
        assert "tableCellLocation" in insert_req
        assert "insertRight" in insert_req

    def test_delete_column_structure(self):
        """Verify deleteTableColumn matches Google Docs API spec."""
        result = create_delete_table_column_request(100, 1)

        assert "deleteTableColumn" in result
        delete_req = result["deleteTableColumn"]
        assert "tableCellLocation" in delete_req

    def test_cell_style_structure(self):
        """Verify updateTableCellStyle matches Google Docs API spec."""
        result = create_update_table_cell_style_request(
            100, 0, 0, background_color="#FFFFFF"
        )

        assert "updateTableCellStyle" in result
        update_req = result["updateTableCellStyle"]
        assert "tableCellLocation" in update_req
        assert "tableCellStyle" in update_req
        assert "fields" in update_req

    def test_delete_bullets_structure(self):
        """Verify deleteParagraphBullets matches Google Docs API spec."""
        result = create_delete_paragraph_bullets_request(10, 50)

        assert "deleteParagraphBullets" in result
        delete_req = result["deleteParagraphBullets"]
        assert "range" in delete_req
        assert "startIndex" in delete_req["range"]
        assert "endIndex" in delete_req["range"]


# ==============================================================================
# NEW REQUEST BUILDER TESTS - Header/Footer & Advanced Table Operations
# ==============================================================================


class TestDeleteHeaderRequest:
    """Test create_delete_header_request helper function."""

    def test_delete_header_basic(self):
        """Test basic header deletion request."""
        result = create_delete_header_request("kix.abc123")

        assert "deleteHeader" in result
        assert result["deleteHeader"]["headerId"] == "kix.abc123"

    def test_delete_header_different_ids(self):
        """Test with different header IDs."""
        for header_id in ["kix.header1", "kix.firstpage", "kix.evenpage"]:
            result = create_delete_header_request(header_id)
            assert result["deleteHeader"]["headerId"] == header_id


class TestDeleteFooterRequest:
    """Test create_delete_footer_request helper function."""

    def test_delete_footer_basic(self):
        """Test basic footer deletion request."""
        result = create_delete_footer_request("kix.def456")

        assert "deleteFooter" in result
        assert result["deleteFooter"]["footerId"] == "kix.def456"

    def test_delete_footer_different_ids(self):
        """Test with different footer IDs."""
        for footer_id in ["kix.footer1", "kix.firstpage", "kix.evenpage"]:
            result = create_delete_footer_request(footer_id)
            assert result["deleteFooter"]["footerId"] == footer_id


class TestMergeTableCellsRequest:
    """Test create_merge_table_cells_request helper function."""

    def test_merge_basic(self):
        """Test basic cell merge request."""
        result = create_merge_table_cells_request(
            table_start_index=100,
            start_row=0,
            start_col=0,
            row_span=2,
            col_span=3,
        )

        assert "mergeTableCells" in result
        merge_req = result["mergeTableCells"]
        assert "tableRange" in merge_req

        table_range = merge_req["tableRange"]
        assert table_range["rowSpan"] == 2
        assert table_range["columnSpan"] == 3

        cell_loc = table_range["tableCellLocation"]
        assert cell_loc["tableStartLocation"]["index"] == 100
        assert cell_loc["rowIndex"] == 0
        assert cell_loc["columnIndex"] == 0

    def test_merge_different_positions(self):
        """Test merge at different table positions."""
        result = create_merge_table_cells_request(
            table_start_index=500,
            start_row=2,
            start_col=1,
            row_span=3,
            col_span=2,
        )

        table_range = result["mergeTableCells"]["tableRange"]
        assert table_range["tableCellLocation"]["tableStartLocation"]["index"] == 500
        assert table_range["tableCellLocation"]["rowIndex"] == 2
        assert table_range["tableCellLocation"]["columnIndex"] == 1


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


class TestUpdateTableColumnPropertiesRequest:
    """Test create_update_table_column_properties_request helper function."""

    def test_fixed_width(self):
        """Test setting fixed column width."""
        result = create_update_table_column_properties_request(
            table_start_index=100,
            column_indices=[0],
            width=150.0,
            width_type="FIXED_WIDTH",
        )

        assert "updateTableColumnProperties" in result
        req = result["updateTableColumnProperties"]
        assert req["tableStartLocation"]["index"] == 100
        assert req["columnIndices"] == [0]
        assert req["tableColumnProperties"]["widthType"] == "FIXED_WIDTH"
        assert req["tableColumnProperties"]["width"]["magnitude"] == 150.0
        assert req["tableColumnProperties"]["width"]["unit"] == "PT"

    def test_evenly_distributed(self):
        """Test evenly distributed width type."""
        result = create_update_table_column_properties_request(
            table_start_index=100,
            column_indices=[0, 1, 2],
            width_type="EVENLY_DISTRIBUTED",
        )

        req = result["updateTableColumnProperties"]
        assert req["tableColumnProperties"]["widthType"] == "EVENLY_DISTRIBUTED"

    def test_multiple_columns(self):
        """Test setting width for multiple columns."""
        result = create_update_table_column_properties_request(
            table_start_index=200,
            column_indices=[0, 2, 4],
            width=100.0,
            width_type="FIXED_WIDTH",
        )

        req = result["updateTableColumnProperties"]
        assert req["columnIndices"] == [0, 2, 4]


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


# ==============================================================================
# NEW REQUEST STRUCTURE INTEGRITY TESTS
# ==============================================================================


class TestNewRequestStructureIntegrity:
    """Test that new requests match Google Docs API spec."""

    def test_delete_header_structure(self):
        """Verify deleteHeader matches Google Docs API spec."""
        result = create_delete_header_request("kix.test123")

        assert "deleteHeader" in result
        assert "headerId" in result["deleteHeader"]

    def test_delete_footer_structure(self):
        """Verify deleteFooter matches Google Docs API spec."""
        result = create_delete_footer_request("kix.test456")

        assert "deleteFooter" in result
        assert "footerId" in result["deleteFooter"]

    def test_merge_cells_structure(self):
        """Verify mergeTableCells matches Google Docs API spec."""
        result = create_merge_table_cells_request(100, 0, 0, 2, 2)

        assert "mergeTableCells" in result
        merge_req = result["mergeTableCells"]
        assert "tableRange" in merge_req

        table_range = merge_req["tableRange"]
        assert "tableCellLocation" in table_range
        assert "rowSpan" in table_range
        assert "columnSpan" in table_range

        cell_loc = table_range["tableCellLocation"]
        assert "tableStartLocation" in cell_loc
        assert "index" in cell_loc["tableStartLocation"]
        assert "rowIndex" in cell_loc
        assert "columnIndex" in cell_loc

    def test_unmerge_cells_structure(self):
        """Verify unmergeTableCells matches Google Docs API spec."""
        result = create_unmerge_table_cells_request(100, 0, 0, 2, 2)

        assert "unmergeTableCells" in result
        unmerge_req = result["unmergeTableCells"]
        assert "tableRange" in unmerge_req

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

    def test_column_properties_structure(self):
        """Verify updateTableColumnProperties matches Google Docs API spec."""
        result = create_update_table_column_properties_request(
            100, [0], width=100.0, width_type="FIXED_WIDTH"
        )

        assert "updateTableColumnProperties" in result
        req = result["updateTableColumnProperties"]
        assert "tableStartLocation" in req
        assert "columnIndices" in req
        assert "tableColumnProperties" in req
        assert "fields" in req

    def test_pin_header_rows_structure(self):
        """Verify pinTableHeaderRows matches Google Docs API spec."""
        result = create_pin_table_header_rows_request(100, 1)

        assert "pinTableHeaderRows" in result
        req = result["pinTableHeaderRows"]
        assert "tableStartLocation" in req
        assert "index" in req["tableStartLocation"]
        assert "pinnedHeaderRowsCount" in req
