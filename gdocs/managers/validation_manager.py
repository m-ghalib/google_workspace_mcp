"""
Validation Manager

This module provides centralized validation logic for Google Docs operations,
extracting validation patterns from individual tool functions.
"""

import logging
from typing import Dict, Any, List, Tuple, Optional

from gdocs.docs_helpers import validate_operation

logger = logging.getLogger(__name__)


class ValidationManager:
    """
    Centralized validation manager for Google Docs operations.

    Provides consistent validation patterns and error messages across
    all document operations, reducing code duplication and improving
    error message quality.
    """

    def __init__(self):
        """Initialize the validation manager."""
        self.validation_rules = self._setup_validation_rules()

    def _setup_validation_rules(self) -> Dict[str, Any]:
        """Setup validation rules and constraints."""
        return {
            "table_max_rows": 1000,
            "table_max_columns": 20,
            "document_id_pattern": r"^[a-zA-Z0-9-_]+$",
            "max_text_length": 1000000,  # 1MB text limit
            "font_size_range": (1, 400),  # Google Docs font size limits
            "valid_header_footer_types": ["DEFAULT", "FIRST_PAGE_ONLY", "EVEN_PAGE"],
            "valid_section_types": ["header", "footer"],
            "valid_list_types": ["UNORDERED", "ORDERED"],
            "valid_element_types": ["table", "list", "page_break"],
        }

    def validate_document_id(self, document_id: str) -> Tuple[bool, str]:
        """
        Validate Google Docs document ID format.

        Args:
            document_id: Document ID to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not document_id:
            return False, "Document ID cannot be empty"

        if not isinstance(document_id, str):
            return (
                False,
                f"Document ID must be a string, got {type(document_id).__name__}",
            )

        # Basic length check (Google Docs IDs are typically 40+ characters)
        if len(document_id) < 20:
            return False, "Document ID appears too short to be valid"

        return True, ""

    def validate_table_data(self, table_data: List[List[str]]) -> Tuple[bool, str]:
        """
        Comprehensive validation for table data format.

        This extracts and centralizes table validation logic from multiple functions.

        Args:
            table_data: 2D array of data to validate

        Returns:
            Tuple of (is_valid, detailed_error_message)
        """
        if not table_data:
            return (
                False,
                "Table data cannot be empty. Required format: [['col1', 'col2'], ['row1col1', 'row1col2']]",
            )

        if not isinstance(table_data, list):
            return (
                False,
                f"Table data must be a list, got {type(table_data).__name__}. Required format: [['col1', 'col2'], ['row1col1', 'row1col2']]",
            )

        # Check if it's a 2D list
        if not all(isinstance(row, list) for row in table_data):
            non_list_rows = [
                i for i, row in enumerate(table_data) if not isinstance(row, list)
            ]
            return (
                False,
                f"All rows must be lists. Rows {non_list_rows} are not lists. Required format: [['col1', 'col2'], ['row1col1', 'row1col2']]",
            )

        # Check for empty rows
        if any(len(row) == 0 for row in table_data):
            empty_rows = [i for i, row in enumerate(table_data) if len(row) == 0]
            return (
                False,
                f"Rows cannot be empty. Empty rows found at indices: {empty_rows}",
            )

        # Check column consistency
        col_counts = [len(row) for row in table_data]
        if len(set(col_counts)) > 1:
            return (
                False,
                f"All rows must have the same number of columns. Found column counts: {col_counts}. Fix your data structure.",
            )

        rows = len(table_data)
        cols = col_counts[0]

        # Check dimension limits
        if rows > self.validation_rules["table_max_rows"]:
            return (
                False,
                f"Too many rows ({rows}). Maximum allowed: {self.validation_rules['table_max_rows']}",
            )

        if cols > self.validation_rules["table_max_columns"]:
            return (
                False,
                f"Too many columns ({cols}). Maximum allowed: {self.validation_rules['table_max_columns']}",
            )

        # Check cell content types
        for row_idx, row in enumerate(table_data):
            for col_idx, cell in enumerate(row):
                if cell is None:
                    return (
                        False,
                        f"Cell ({row_idx},{col_idx}) is None. All cells must be strings, use empty string '' for empty cells.",
                    )

                if not isinstance(cell, str):
                    return (
                        False,
                        f"Cell ({row_idx},{col_idx}) is {type(cell).__name__}, not string. All cells must be strings. Value: {repr(cell)}",
                    )

        return True, f"Valid table data: {rows}×{cols} table format"

    def validate_text_formatting_params(
        self,
        bold: Optional[bool] = None,
        italic: Optional[bool] = None,
        underline: Optional[bool] = None,
        font_size: Optional[int] = None,
        font_family: Optional[str] = None,
        text_color: Optional[str] = None,
        background_color: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Validate text formatting parameters.

        Args:
            bold: Bold setting
            italic: Italic setting
            underline: Underline setting
            font_size: Font size in points
            font_family: Font family name
            text_color: Text color in "#RRGGBB" format
            background_color: Background color in "#RRGGBB" format

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if at least one formatting option is provided
        formatting_params = [
            bold,
            italic,
            underline,
            font_size,
            font_family,
            text_color,
            background_color,
        ]
        if all(param is None for param in formatting_params):
            return (
                False,
                "At least one formatting parameter must be provided (bold, italic, underline, font_size, font_family, text_color, or background_color)",
            )

        # Validate boolean parameters
        for param, name in [
            (bold, "bold"),
            (italic, "italic"),
            (underline, "underline"),
        ]:
            if param is not None and not isinstance(param, bool):
                return (
                    False,
                    f"{name} parameter must be boolean (True/False), got {type(param).__name__}",
                )

        # Validate font size
        if font_size is not None:
            if not isinstance(font_size, int):
                return (
                    False,
                    f"font_size must be an integer, got {type(font_size).__name__}",
                )

            min_size, max_size = self.validation_rules["font_size_range"]
            if not (min_size <= font_size <= max_size):
                return (
                    False,
                    f"font_size must be between {min_size} and {max_size} points, got {font_size}",
                )

        # Validate font family
        if font_family is not None:
            if not isinstance(font_family, str):
                return (
                    False,
                    f"font_family must be a string, got {type(font_family).__name__}",
                )

            if not font_family.strip():
                return False, "font_family cannot be empty"

        # Validate colors
        is_valid, error_msg = self.validate_color_param(text_color, "text_color")
        if not is_valid:
            return False, error_msg

        is_valid, error_msg = self.validate_color_param(
            background_color, "background_color"
        )
        if not is_valid:
            return False, error_msg

        return True, ""

    def validate_color_param(
        self, color: Optional[str], param_name: str
    ) -> Tuple[bool, str]:
        """Validate color parameters (hex string "#RRGGBB")."""
        if color is None:
            return True, ""

        if not isinstance(color, str):
            return False, f"{param_name} must be a hex string like '#RRGGBB'"

        if len(color) != 7 or not color.startswith("#"):
            return False, f"{param_name} must be a hex string like '#RRGGBB'"

        hex_color = color[1:]
        if any(c not in "0123456789abcdefABCDEF" for c in hex_color):
            return False, f"{param_name} must be a hex string like '#RRGGBB'"

        return True, ""

    def validate_index(self, index: int, context: str = "Index") -> Tuple[bool, str]:
        """
        Validate a single document index.

        Args:
            index: Index to validate
            context: Context description for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(index, int):
            return False, f"{context} must be an integer, got {type(index).__name__}"

        if index < 0:
            return (
                False,
                f"{context} {index} is negative. You MUST call inspect_doc_structure first to get the proper insertion index.",
            )

        return True, ""

    def validate_index_range(
        self,
        start_index: int,
        end_index: Optional[int] = None,
        document_length: Optional[int] = None,
    ) -> Tuple[bool, str]:
        """
        Validate document index ranges.

        Args:
            start_index: Starting index
            end_index: Ending index (optional)
            document_length: Total document length for bounds checking

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate start_index
        if not isinstance(start_index, int):
            return (
                False,
                f"start_index must be an integer, got {type(start_index).__name__}",
            )

        if start_index < 0:
            return False, f"start_index cannot be negative, got {start_index}"

        # Validate end_index if provided
        if end_index is not None:
            if not isinstance(end_index, int):
                return (
                    False,
                    f"end_index must be an integer, got {type(end_index).__name__}",
                )

            if end_index <= start_index:
                return (
                    False,
                    f"end_index ({end_index}) must be greater than start_index ({start_index})",
                )

        # Validate against document length if provided
        if document_length is not None:
            if start_index >= document_length:
                return (
                    False,
                    f"start_index ({start_index}) exceeds document length ({document_length})",
                )

            if end_index is not None and end_index > document_length:
                return (
                    False,
                    f"end_index ({end_index}) exceeds document length ({document_length})",
                )

        return True, ""

    def validate_element_insertion_params(
        self, element_type: str, index: int, **kwargs
    ) -> Tuple[bool, str]:
        """
        Validate parameters for element insertion.

        Args:
            element_type: Type of element to insert
            index: Insertion index
            **kwargs: Additional parameters specific to element type

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate element type
        if element_type not in self.validation_rules["valid_element_types"]:
            valid_types = ", ".join(self.validation_rules["valid_element_types"])
            return (
                False,
                f"Invalid element_type '{element_type}'. Must be one of: {valid_types}",
            )

        # Validate index
        if not isinstance(index, int) or index < 0:
            return False, f"index must be a non-negative integer, got {index}"

        # Validate element-specific parameters
        if element_type == "table":
            rows = kwargs.get("rows")
            columns = kwargs.get("columns")

            if not rows or not columns:
                return False, "Table insertion requires 'rows' and 'columns' parameters"

            if not isinstance(rows, int) or not isinstance(columns, int):
                return False, "Table rows and columns must be integers"

            if rows <= 0 or columns <= 0:
                return False, "Table rows and columns must be positive integers"

            if rows > self.validation_rules["table_max_rows"]:
                return (
                    False,
                    f"Too many rows ({rows}). Maximum: {self.validation_rules['table_max_rows']}",
                )

            if columns > self.validation_rules["table_max_columns"]:
                return (
                    False,
                    f"Too many columns ({columns}). Maximum: {self.validation_rules['table_max_columns']}",
                )

        elif element_type == "list":
            list_type = kwargs.get("list_type")

            if not list_type:
                return False, "List insertion requires 'list_type' parameter"

            if list_type not in self.validation_rules["valid_list_types"]:
                valid_types = ", ".join(self.validation_rules["valid_list_types"])
                return (
                    False,
                    f"Invalid list_type '{list_type}'. Must be one of: {valid_types}",
                )

        return True, ""

    def validate_header_footer_params(
        self, section_type: str, header_footer_type: str = "DEFAULT"
    ) -> Tuple[bool, str]:
        """
        Validate header/footer operation parameters.

        Args:
            section_type: Type of section ("header" or "footer")
            header_footer_type: Specific header/footer type

        Returns:
            Tuple of (is_valid, error_message)
        """
        if section_type not in self.validation_rules["valid_section_types"]:
            valid_types = ", ".join(self.validation_rules["valid_section_types"])
            return (
                False,
                f"section_type must be one of: {valid_types}, got '{section_type}'",
            )

        if header_footer_type not in self.validation_rules["valid_header_footer_types"]:
            valid_types = ", ".join(self.validation_rules["valid_header_footer_types"])
            return (
                False,
                f"header_footer_type must be one of: {valid_types}, got '{header_footer_type}'",
            )

        return True, ""

    def validate_batch_operations(
        self, operations: List[Dict[str, Any]]
    ) -> Tuple[bool, str]:
        """
        Validate a list of batch operations.

        Args:
            operations: List of operation dictionaries

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not operations:
            return False, "Operations list cannot be empty"

        if not isinstance(operations, list):
            return False, f"Operations must be a list, got {type(operations).__name__}"

        # Validate each operation
        for i, op in enumerate(operations):
            if not isinstance(op, dict):
                return (
                    False,
                    f"Operation {i + 1} must be a dictionary, got {type(op).__name__}",
                )

            if "type" not in op:
                return False, f"Operation {i + 1} missing required 'type' field"

            # Validate required fields for the operation type
            is_valid, error_msg = validate_operation(op)
            if not is_valid:
                return False, f"Operation {i + 1}: {error_msg}"

            op_type = op["type"]

            if op_type == "format_text":
                is_valid, error_msg = self.validate_text_formatting_params(
                    op.get("bold"),
                    op.get("italic"),
                    op.get("underline"),
                    op.get("font_size"),
                    op.get("font_family"),
                    op.get("text_color"),
                    op.get("background_color"),
                )
                if not is_valid:
                    return False, f"Operation {i + 1} (format_text): {error_msg}"

                is_valid, error_msg = self.validate_index_range(
                    op["start_index"], op["end_index"]
                )
                if not is_valid:
                    return False, f"Operation {i + 1} (format_text): {error_msg}"

        return True, ""

    def validate_text_content(
        self, text: str, max_length: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Validate text content for insertion.

        Args:
            text: Text to validate
            max_length: Maximum allowed length

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(text, str):
            return False, f"Text must be a string, got {type(text).__name__}"

        max_len = max_length or self.validation_rules["max_text_length"]
        if len(text) > max_len:
            return False, f"Text too long ({len(text)} characters). Maximum: {max_len}"

        return True, ""

    def validate_cell_merge_params(
        self,
        table_index: int,
        start_row: int,
        start_col: int,
        row_span: int,
        col_span: int,
        table_rows: Optional[int] = None,
        table_cols: Optional[int] = None,
    ) -> Tuple[bool, str]:
        """
        Validate parameters for table cell merge/unmerge operations.

        Args:
            table_index: Index of the table (0-based)
            start_row: Starting row index for the merge (0-based)
            start_col: Starting column index for the merge (0-based)
            row_span: Number of rows to merge (must be >= 1)
            col_span: Number of columns to merge (must be >= 1)
            table_rows: Total rows in table (for bounds checking)
            table_cols: Total columns in table (for bounds checking)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate table_index
        if not isinstance(table_index, int) or table_index < 0:
            return False, f"table_index must be a non-negative integer, got {table_index}"

        # Validate start_row
        if not isinstance(start_row, int) or start_row < 0:
            return False, f"start_row must be a non-negative integer, got {start_row}"

        # Validate start_col
        if not isinstance(start_col, int) or start_col < 0:
            return False, f"start_col must be a non-negative integer, got {start_col}"

        # Validate row_span
        if not isinstance(row_span, int) or row_span < 1:
            return False, f"row_span must be a positive integer (>= 1), got {row_span}"

        # Validate col_span
        if not isinstance(col_span, int) or col_span < 1:
            return False, f"col_span must be a positive integer (>= 1), got {col_span}"

        # Must merge at least 2 cells total
        if row_span == 1 and col_span == 1:
            return (
                False,
                "Merge operation requires either row_span > 1 or col_span > 1 (cannot merge single cell)",
            )

        # Bounds checking if table dimensions provided
        if table_rows is not None:
            if start_row >= table_rows:
                return (
                    False,
                    f"start_row ({start_row}) exceeds table rows ({table_rows})",
                )
            if start_row + row_span > table_rows:
                return (
                    False,
                    f"Merge would exceed table bounds: start_row ({start_row}) + row_span ({row_span}) > table_rows ({table_rows})",
                )

        if table_cols is not None:
            if start_col >= table_cols:
                return (
                    False,
                    f"start_col ({start_col}) exceeds table columns ({table_cols})",
                )
            if start_col + col_span > table_cols:
                return (
                    False,
                    f"Merge would exceed table bounds: start_col ({start_col}) + col_span ({col_span}) > table_cols ({table_cols})",
                )

        return True, ""

    def validate_row_style_params(
        self,
        table_index: int,
        row_indices: List[int],
        min_row_height: Optional[float] = None,
        prevent_overflow: Optional[bool] = None,
        table_rows: Optional[int] = None,
    ) -> Tuple[bool, str]:
        """
        Validate parameters for table row styling operations.

        Args:
            table_index: Index of the table (0-based)
            row_indices: List of row indices to update
            min_row_height: Minimum row height in points
            prevent_overflow: Whether to prevent overflow
            table_rows: Total rows in table (for bounds checking)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate table_index
        if not isinstance(table_index, int) or table_index < 0:
            return False, f"table_index must be a non-negative integer, got {table_index}"

        # Validate row_indices
        if not isinstance(row_indices, list):
            return (
                False,
                f"row_indices must be a list of integers, got {type(row_indices).__name__}",
            )

        if not row_indices:
            return False, "row_indices cannot be empty"

        for i, idx in enumerate(row_indices):
            if not isinstance(idx, int) or idx < 0:
                return (
                    False,
                    f"row_indices[{i}] must be a non-negative integer, got {idx}",
                )

        # Check for duplicates
        if len(row_indices) != len(set(row_indices)):
            return False, "row_indices contains duplicate values"

        # Validate style parameters - at least one must be provided
        if min_row_height is None and prevent_overflow is None:
            return (
                False,
                "At least one style parameter must be provided (min_row_height or prevent_overflow)",
            )

        # Validate min_row_height
        if min_row_height is not None:
            if not isinstance(min_row_height, (int, float)):
                return (
                    False,
                    f"min_row_height must be a number, got {type(min_row_height).__name__}",
                )
            if min_row_height < 0:
                return False, f"min_row_height must be non-negative, got {min_row_height}"

        # Validate prevent_overflow
        if prevent_overflow is not None and not isinstance(prevent_overflow, bool):
            return (
                False,
                f"prevent_overflow must be a boolean, got {type(prevent_overflow).__name__}",
            )

        # Bounds checking
        if table_rows is not None:
            for idx in row_indices:
                if idx >= table_rows:
                    return (
                        False,
                        f"Row index {idx} exceeds table rows ({table_rows})",
                    )

        return True, ""

    def validate_column_properties_params(
        self,
        table_index: int,
        column_indices: List[int],
        width: Optional[float] = None,
        width_type: str = "FIXED_WIDTH",
        table_cols: Optional[int] = None,
    ) -> Tuple[bool, str]:
        """
        Validate parameters for table column property operations.

        Args:
            table_index: Index of the table (0-based)
            column_indices: List of column indices to update
            width: Column width in points
            width_type: Width type ("EVENLY_DISTRIBUTED" or "FIXED_WIDTH")
            table_cols: Total columns in table (for bounds checking)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate table_index
        if not isinstance(table_index, int) or table_index < 0:
            return False, f"table_index must be a non-negative integer, got {table_index}"

        # Validate column_indices
        if not isinstance(column_indices, list):
            return (
                False,
                f"column_indices must be a list of integers, got {type(column_indices).__name__}",
            )

        if not column_indices:
            return False, "column_indices cannot be empty"

        for i, idx in enumerate(column_indices):
            if not isinstance(idx, int) or idx < 0:
                return (
                    False,
                    f"column_indices[{i}] must be a non-negative integer, got {idx}",
                )

        # Check for duplicates
        if len(column_indices) != len(set(column_indices)):
            return False, "column_indices contains duplicate values"

        # Validate width_type
        valid_width_types = ["EVENLY_DISTRIBUTED", "FIXED_WIDTH"]
        if width_type not in valid_width_types:
            return (
                False,
                f"width_type must be one of {valid_width_types}, got '{width_type}'",
            )

        # Validate width
        if width_type == "FIXED_WIDTH" and width is None:
            return (
                False,
                "width is required when width_type is 'FIXED_WIDTH'",
            )

        if width is not None:
            if not isinstance(width, (int, float)):
                return False, f"width must be a number, got {type(width).__name__}"
            if width <= 0:
                return False, f"width must be positive, got {width}"

        # Bounds checking
        if table_cols is not None:
            for idx in column_indices:
                if idx >= table_cols:
                    return (
                        False,
                        f"Column index {idx} exceeds table columns ({table_cols})",
                    )

        return True, ""

    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all validation rules and constraints.

        Returns:
            Dictionary containing validation rules
        """
        return {
            "constraints": self.validation_rules.copy(),
            "supported_operations": {
                "table_operations": ["create_table", "populate_table"],
                "text_operations": ["insert_text", "format_text", "find_replace"],
                "element_operations": [
                    "insert_table",
                    "insert_list",
                    "insert_page_break",
                ],
                "header_footer_operations": ["update_header", "update_footer"],
            },
            "data_formats": {
                "table_data": "2D list of strings: [['col1', 'col2'], ['row1col1', 'row1col2']]",
                "text_formatting": "Optional boolean/integer parameters for styling",
                "document_indices": "Non-negative integers for position specification",
            },
        }
