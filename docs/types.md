# Types and Core Concepts

## Filter Class

- Inherit from `BaseFilter`.
- Configure with an inner `FilterConfig` class.

## FieldCriteria

- `name`: The input field name (string)
- `field_type`: Python type (e.g., `str`, `int`, `datetime`)
- `op`: Tuple of allowed `OperationEnum`
- `model_attr`: SQLAlchemy column to filter (optional if using custom logic)
- `model_attrs_with_logical_op`: tuple[(list[col], LogicalOperator)] for combining multiple attrs
- `required_op`: subset of `op` that are marked required in the schema
- `custom_filter_per_op`: callable `(op, value) -> SQLAlchemy expression`
- `prefix`: optional string to namespace the generated field name

## Enums

- OperationEnum: `EQ`, `NEQ`, `IN`, `NOTIN`, `GT`, `GTE`, `LT`, `LTE`, `LIKE`, `ILIKE`, `CONT`, `IS`, `ISNULL`, `BTW`
- OrderEnum: `ASC`, `DESC`
- LogicalOperator: `AND`, `OR`
- PaginationEnum: `OFFSET_BASED`, `PAGE_BASED`

## QSearch and AdvancedQSearch

- `QSearch`: `model_attrs`, single `op`, `logical_op`
- `AdvancedQSearch`: `model_attrs_with_op` dict and `logical_op`

## SortBy and Selectable

- `SortBy`: maps input names to SQLAlchemy columns, with aliasing to camelCase if desired
- `Selectable`: maps input names to SQLAlchemy columns for projection

## FilterResult

Returned by `BaseFilter.get_filter_model()` with fields:

- `filters`: list of SQLAlchemy expressions or `None`
- `sorting`: list of `(column, direction)` callables or `None`
- `selected_columns`: list of SQLAlchemy columns or `None`
- `q_search`: OR/AND expression or `None`
- `pagination`: dict with keys like `limit`, `offset`, `page`, `page_size` or `None`
