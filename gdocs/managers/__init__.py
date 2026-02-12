"""
Google Docs Operation Managers — REST API only

Only TableOperationManager remains, for 3 RED tools (unmerge, row_style, pin_headers).
All other table operations are handled directly in docs_tools.py.
"""

from .table_operation_manager import TableOperationManager

__all__ = [
    "TableOperationManager",
]
