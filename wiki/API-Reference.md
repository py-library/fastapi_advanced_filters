# API Reference

Core building blocks:

- `BaseFilter`: Pydantic v2 model with mixins. Provides `get_filter_model()` to produce a `FilterResult`.
- `FilterConfig`: inner class for schema declaration.
- `FieldCriteria`: field name, type, model attribute, and allowed operations.
- `QSearch` / `AdvancedQSearch`: free-text search configuration.
- `SortBy`: sorting configuration with optional camelCase aliasing.
- `Selectable`: selected columns configuration with optional camelCase aliasing.
- `PaginationEnum`: pagination strategy options.

Return types in `FilterResult`:
- `filters: list[Any]` — SQLAlchemy boolean expressions
- `sorting: list[tuple[Any, Any]]` — `(column, direction)` pairs
- `selected_columns: list[Any]`
- `q_search: Optional[Any]`
- `pagination: Optional[Pagination]`

See the repository [docs/reference.md](../docs/reference.md) for deep details and enums, types, and mappings.
