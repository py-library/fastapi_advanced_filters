# API Reference

This document summarizes the public API exposed by `fastapi-filter` for building filter models.

## BaseFilter

- Inherit from `BaseFilter` to define a filter model for an endpoint.
- The inner `class FilterConfig:` controls generation of fields.

### FilterConfig fields

- `model`: Optional SQLAlchemy model class. If provided, you can refer to real columns in criteria.
- `prefix`: Optional string prefix used to namespace generated field names.
- `default_op`: Tuple of `OperationEnum` used for implicit fields when `fields = "__all__"`.
- `fields`: Either `"__all__"` or a list of `FieldCriteria`/field names to include.
- `pagination`: `PaginationEnum.OFFSET_BASED` or `PaginationEnum.PAGE_BASED`.
- `q_search`: Either `QSearch` or `AdvancedQSearch` for keyword search across columns.
- `sort_by`: `SortBy` describing allowed sortable attributes and aliasing.
- `select_only`: `Selectable` describing allowed selected attributes and aliasing.

### Methods

- `get_filter_model() -> FilterResult`
  - Returns a `FilterResult` containing:
    - `filters`: list of SQLAlchemy conditions, or `None`.
    - `sorting`: list of `(column, direction)` entries, or `None`.
    - `selected_columns`: list of SQLAlchemy columns, or `None`.
    - `q_search`: OR/AND expression, or `None`.
    - `pagination`: dict of pagination values, or `None`.

## Data Classes

- `FieldCriteria`: describes a filterable field (name, type, op, model_attr, required_op, etc.).
- `QSearch`: define free-text search across `model_attrs` with a single op and logical op.
- `AdvancedQSearch`: like `QSearch`, but per-op model attrs mapping.
- `SortBy`: allowed sortable attributes with aliasing options.
- `Selectable`: allowed selectable attributes with aliasing options.
- `Pagination`: configure limit/offset or page/page_size.
- `FilterResult`: normalized result of `BaseFilter.get_filter_model()`.

## Enums

- `OperationEnum`: EQ, NEQ, IN, NOTIN, GT, GTE, LT, LTE, LIKE, ILIKE, CONT, IS, ISNULL, BTW.
- `OrderEnum`: ASC, DESC.
- `LogicalOperator`: AND, OR.
- `PaginationEnum`: OFFSET_BASED, PAGE_BASED.

## Operation Mappings (SQLAlchemy)

- `SQLALCHEMY_OP_MAPPING`: maps `OperationEnum` to callables generating SQLAlchemy expressions.
- `SQLALCHEMY_SORTING_MAPPING`: maps `OrderEnum` to sorting callables (e.g., `col.asc()`).
- `SQLALCHEMY_LOGICAL_OP_MAPPING`: maps `LogicalOperator` to `and_`/`or_`.

These are available at module import:

```python
from fastapi_filters import (
    SQLALCHEMY_LOGICAL_OP_MAPPING,
    SQLALCHEMY_OP_MAPPING,
    SQLALCHEMY_SORTING_MAPPING,
)
```

## Utilities

- `to_camel_case`, `to_snake_case`
- Validation helpers: `validate_sortable_schema`, `validate_selectable_schema`

## Error handling

- Most validation raises `ValueError` with descriptive messages.
- Some mapping functions return `None` when inputs are invalid (e.g., IN/NOTIN with bad values), allowing callers to skip conditions safely.
