"""
Operation mappings for different ORMs.

Currently, only SQLAlchemy is supported.
"""

from fastapi_filters.src.operation_mapping.sqlalchemy_mapping import (
    LOGICAL_OP_MAPPING as SQLALCHEMY_LOGICAL_OP_MAPPING,
)
from fastapi_filters.src.operation_mapping.sqlalchemy_mapping import (
    OP_MAPPING as SQLALCHEMY_OP_MAPPING,
)
from fastapi_filters.src.operation_mapping.sqlalchemy_mapping import (
    SORTING_MAPPING as SQLALCHEMY_SORTING_MAPPING,
)

__all__ = [
    "SQLALCHEMY_OP_MAPPING",
    "SQLALCHEMY_SORTING_MAPPING",
    "SQLALCHEMY_LOGICAL_OP_MAPPING",
]
