# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to
Semantic Versioning.

## [0.1.0] - 2025-09-28

Initial public release of fastapi_advanced_filters.

### Added

- Pydantic v2-based `BaseFilter` with a `FilterConfig` inner class to declaratively define:
	- Filterable fields via `FieldCriteria` (supports EQ, NEQ, IN, NOTIN, GT, GTE, LT, LTE, LIKE, ILIKE, CONT, IS, ISNULL, BTW)
	- Optional full-text-ish search via `QSearch` and `AdvancedQSearch` with logical combinators (AND/OR)
	- Sorting via `SortBy` with optional camelCase aliasing
	- Field selection via `Selectable` with optional camelCase aliasing
	- Pagination via `PaginationEnum.OFFSET_BASED` (returns a `Pagination` dataclass with `limit`/`offset`)
- First-class SQLAlchemy support:
	- Operation mappings that translate `OperationEnum` to SQLAlchemy expressions
	- Sorting mappings for `OrderEnum`
	- Logical operator mappings for AND/OR
- Utilities:
	- `to_camel_case`, `to_snake_case`
	- Schema validators for `SortBy` and `Selectable`
- Robust test suite (unit + integration) with dialect-agnostic SQL assertions; ~98% coverage locally.
- Documentation:
	- `docs/` with Installation, Reference, Examples, Extending, and Types
	- Simplified examples demonstrating filtering, sorting, selection, q_search, and pagination
	- Root `README.md` linked to docs and quickstart

### CI/CD

- GitHub Actions CI: Poetry-based setup running flake8, mypy, and pytest with SQLAlchemy extras.
- Publish workflow: tag-driven (vX.Y.Z), validates tag vs `pyproject.toml` version, builds, and publishes to PyPI using repo secret `PYPI_API_TOKEN` (or `API_TOKEN`). Also creates a GitHub Release.

### Compatibility

- Python: 3.9+
- FastAPI: >= 0.100.0
- Pydantic: >= 2.0.0 (tested with 2.11+)
- SQLAlchemy (optional): >= 1.4.36, < 2.1.0

[0.1.0]: https://github.com/py-library/fastapi_advanced_filters/releases/tag/v0.1.0
