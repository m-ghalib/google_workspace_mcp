"""
Table Operation Manager — REST API only

Handles 3 specialized table operations:
- unmerge_table_cells
- update_table_row_style
- pin_table_header_rows
"""

import logging
import asyncio
from typing import List, Dict, Any, Tuple

from gdocs.docs_helpers import (
    create_unmerge_table_cells_request,
    create_update_table_row_style_request,
    create_pin_table_header_rows_request,
)
from gdocs.docs_structure import find_tables

logger = logging.getLogger(__name__)


class TableOperationManager:
    """REST API table operations for features Apps Script cannot support."""

    def __init__(self, service):
        self.service = service

    async def _get_document_tables(self, document_id: str) -> List[Dict[str, Any]]:
        """Get fresh document structure and extract table information."""
        doc = await asyncio.to_thread(
            self.service.documents().get(documentId=document_id).execute
        )
        return find_tables(doc)

    async def unmerge_cells(
        self,
        document_id: str,
        table_index: int,
        row_index: int,
        col_index: int,
        row_span: int,
        col_span: int,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Unmerge previously merged cells in a table."""
        try:
            tables = await self._get_document_tables(document_id)
            if table_index >= len(tables):
                return (
                    False,
                    f"Table index {table_index} not found. Document has {len(tables)} tables",
                    {},
                )

            table_start_index = tables[table_index]["start_index"]

            request = create_unmerge_table_cells_request(
                table_start_index, row_index, col_index, row_span, col_span
            )

            await asyncio.to_thread(
                self.service.documents()
                .batchUpdate(documentId=document_id, body={"requests": [request]})
                .execute
            )

            return (
                True,
                f"Successfully unmerged cells at ({row_index},{col_index}) spanning {row_span}x{col_span}",
                {
                    "table_index": table_index,
                    "row_index": row_index,
                    "col_index": col_index,
                    "row_span": row_span,
                    "col_span": col_span,
                },
            )

        except Exception as e:
            logger.error(f"Failed to unmerge cells: {str(e)}")
            return False, f"Failed to unmerge cells: {str(e)}", {}

    async def update_row_style(
        self,
        document_id: str,
        table_index: int,
        row_indices: List[int],
        min_row_height: float = None,
        prevent_overflow: bool = None,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Update the style of table rows."""
        try:
            if min_row_height is None and prevent_overflow is None:
                return (
                    False,
                    "At least one style property (min_row_height or prevent_overflow) must be provided",
                    {},
                )

            tables = await self._get_document_tables(document_id)
            if table_index >= len(tables):
                return (
                    False,
                    f"Table index {table_index} not found. Document has {len(tables)} tables",
                    {},
                )

            table_info = tables[table_index]
            table_start_index = table_info["start_index"]
            table_rows = table_info["rows"]

            for idx in row_indices:
                if idx < 0 or idx >= table_rows:
                    return (
                        False,
                        f"Row index {idx} is out of bounds. Table has {table_rows} rows",
                        {},
                    )

            request = create_update_table_row_style_request(
                table_start_index, row_indices, min_row_height, prevent_overflow
            )

            if request is None:
                return False, "No valid style properties to apply", {}

            await asyncio.to_thread(
                self.service.documents()
                .batchUpdate(documentId=document_id, body={"requests": [request]})
                .execute
            )

            return (
                True,
                f"Successfully updated style for rows {row_indices}",
                {
                    "table_index": table_index,
                    "row_indices": row_indices,
                    "min_row_height": min_row_height,
                    "prevent_overflow": prevent_overflow,
                },
            )

        except Exception as e:
            logger.error(f"Failed to update row style: {str(e)}")
            return False, f"Failed to update row style: {str(e)}", {}

    async def pin_header_rows(
        self,
        document_id: str,
        table_index: int,
        pinned_header_rows_count: int,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Pin rows as repeating table headers."""
        try:
            tables = await self._get_document_tables(document_id)
            if table_index >= len(tables):
                return (
                    False,
                    f"Table index {table_index} not found. Document has {len(tables)} tables",
                    {},
                )

            table_info = tables[table_index]
            table_start_index = table_info["start_index"]
            table_rows = table_info["rows"]

            if pinned_header_rows_count < 0:
                return (False, "pinned_header_rows_count cannot be negative", {})
            if pinned_header_rows_count > table_rows:
                return (
                    False,
                    f"pinned_header_rows_count ({pinned_header_rows_count}) exceeds table rows ({table_rows})",
                    {},
                )

            request = create_pin_table_header_rows_request(
                table_start_index, pinned_header_rows_count
            )

            await asyncio.to_thread(
                self.service.documents()
                .batchUpdate(documentId=document_id, body={"requests": [request]})
                .execute
            )

            action = "pinned" if pinned_header_rows_count > 0 else "unpinned"
            return (
                True,
                f"Successfully {action} {pinned_header_rows_count} header row(s)",
                {
                    "table_index": table_index,
                    "pinned_header_rows_count": pinned_header_rows_count,
                },
            )

        except Exception as e:
            logger.error(f"Failed to pin header rows: {str(e)}")
            return False, f"Failed to pin header rows: {str(e)}", {}
