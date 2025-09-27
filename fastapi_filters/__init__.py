"""
FastAPI Filters - A library to add filtering, ordering, and
pagination to FastAPI endpoints.

License: MIT
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

__author__ = "er5bus"
__version__ = "0.0.1"
__license__ = "MIT"
__copyright__ = "Copyright 2023-2025, er5bus"


from fastapi_filters.src import (
    SQLALCHEMY_LOGICAL_OP_MAPPING,
    SQLALCHEMY_OP_MAPPING,
    SQLALCHEMY_SORTING_MAPPING,
    AdvancedQSearch,
    BaseFilter,
    FieldCriteria,
    FilterResult,
    LogicalOperator,
    OperationEnum,
    OrderEnum,
    Pagination,
    PaginationEnum,
    QSearch,
    Selectable,
    SortBy,
)

__all__ = [
    "BaseFilter",
    "OperationEnum",
    "FieldCriteria",
    "Selectable",
    "SortBy",
    "QSearch",
    "PaginationEnum",
    "OrderEnum",
    "FilterResult",
    "Pagination",
    "LogicalOperator",
    "AdvancedQSearch",
    "SQLALCHEMY_OP_MAPPING",
    "SQLALCHEMY_SORTING_MAPPING",
    "SQLALCHEMY_LOGICAL_OP_MAPPING",
]
