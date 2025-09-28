# fastapi_advanced_filters

<!-- Badges -->
[
![CI](https://github.com/py-library/fastapi_advanced_filters/actions/workflows/main.yml/badge.svg)
](https://github.com/py-library/fastapi_advanced_filters/actions/workflows/main.yml)
[
![Publish](https://github.com/py-library/fastapi_advanced_filters/actions/workflows/publish.yml/badge.svg)
](https://github.com/py-library/fastapi_advanced_filters/actions/workflows/publish.yml)
[
![codecov](https://codecov.io/gh/py-library/fastapi_advanced_filters/branch/main/graph/badge.svg)
](https://codecov.io/gh/py-library/fastapi_advanced_filters)
[![Coverage](https://img.shields.io/codecov/c/gh/py-library/fastapi_advanced_filters?label=coverage&logo=codecov)](https://codecov.io/gh/py-library/fastapi_advanced_filters)
[![PyPI](https://img.shields.io/pypi/v/fastapi_advanced_filters.svg)](https://pypi.org/project/fastapi_advanced_filters/)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi_advanced_filters.svg)](https://pypi.org/project/fastapi_advanced_filters/)
[![License](https://img.shields.io/pypi/l/fastapi_advanced_filters.svg)](./LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/fastapi_advanced_filters.svg)](https://pypi.org/project/fastapi_advanced_filters/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)
![ruff](https://img.shields.io/badge/lint-ruff-46a0f5?logo=ruff&logoColor=white)
![mypy](https://img.shields.io/badge/types-mypy-blue)
![poetry](https://img.shields.io/badge/packaging-poetry-60A5FA)

PyPI package name: `fastapi_advanced_filters`.

Type-safe, declarative filtering for FastAPI with first-class SQLAlchemy support.

- Define filters once, map them to SQLAlchemy columns, and get query conditions, sorting, selection, and q-search out of the box.
- Pydantic v2 models with a metaclass generate the filter schema from a simple `FilterConfig`.
- Dialect-agnostic SQL assertions in tests via compiled literal SQL.

## Installation

Python 3.9+ is supported.

Using pip:

```bash
pip install fastapi_advanced_filters
```

If you plan to use SQLAlchemy features, install the extra:

```bash
pip install "fastapi_advanced_filters[sqlalchemy]"
```

With Poetry:

```bash
poetry add fastapi_advanced_filters
# or, with extras
poetry add fastapi_advanced_filters -E sqlalchemy
```

## Quickstart

Define your SQLAlchemy model and a filter class. The filter class uses an inner `FilterConfig` to describe the fields and behaviors.

```python
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base

from fastapi_advanced_filters import (
	BaseFilter,
	FieldCriteria,
	LogicalOperator,
	OperationEnum,
	PaginationEnum,
	QSearch,
	Selectable,
	SortBy,
)

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	age = Column(Integer)
	is_working = Column(Boolean)
	birthday = Column(Date)


class UserFilter(BaseFilter):
	class FilterConfig:
		model = User
		pagination = PaginationEnum.OFFSET_BASED
		# Map sortable and selectable attributes by name
		sort_by = SortBy(
			model_attrs={
				"first_name": User.first_name,
				"age": User.age,
			},
			alias_as_camelcase=True,
		)
		select_only = Selectable(
			model_attrs={
				"first_name": User.first_name,
				"age": User.age,
			},
			alias_as_camelcase=True,
		)
		# Free-text search across multiple columns
		q_search = QSearch(
			model_attrs=[User.first_name, User.last_name],
			op=OperationEnum.ILIKE,
			logical_op=LogicalOperator.OR,
		)
		# Field-level filtering rules
		fields = [
			FieldCriteria(
				name="first_name",
				field_type=str,
				model_attr=User.first_name,
				op=(OperationEnum.EQ, OperationEnum.ILIKE),
			),
			FieldCriteria(
				name="age",
				field_type=int,
				model_attr=User.age,
				op=(OperationEnum.GTE, OperationEnum.LTE, OperationEnum.IN),
			),
		]

# Use it
f = UserFilter(
	user__first_name__ilike="ali",
	age__gte=18,
	sort_by="-age",
	select="firstName,age",
	q_search="ali",
)
result = f.get_filter_model()
print(result.filters)          # list of SQLAlchemy conditions
print(result.sorting)          # list of (column, direction)
print(result.selected_columns) # mapped selected columns
print(result.q_search)         # OR/AND expression for search
print(result.pagination)       # limit/offset or page/page_size
```

## FastAPI integration

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users")
def list_users(filters: UserFilter = Depends(), db: Session = Depends(get_db)):
	q = db.query(User)
	model = filters.get_filter_model()
	if model.filters:
		q = q.filter(*model.filters)
	if model.q_search is not None:
		q = q.filter(model.q_search)
	if model.sorting:
		for col, direction in model.sorting:
			q = q.order_by(direction(col)) if callable(direction) else q.order_by(col)
	if model.selected_columns:
		q = q.with_entities(*model.selected_columns)
	if model.pagination:
		q = q.limit(model.pagination.limit).offset(model.pagination.offset)
	return q.all()
```

## Documentation

Full docs index:

- [docs/README.md](docs/README.md)

Direct links:

- [Installation](docs/installation.md) — How to install and optional extras
- [API reference](docs/reference.md) — FilterConfig, FieldCriteria, QSearch, SortBy, Selectable, Pagination
- [Examples](docs/examples.md) — End-to-end examples
- [Extending](docs/extending.md) — Adding operations, custom filters, advanced usage
- [Types](docs/types.md) — Enums and core dataclasses overview

## Development

- Run tests: `pytest -q`
- Lint/type: `pre-commit run --all-files`
- Python: 3.9+

### Coverage

This project uses pytest-cov. Locally, you can view coverage in the terminal or generate XML/HTML reports:

- Terminal summary (default): `pytest --cov`
- XML for CI/Codecov: `pytest --cov --cov-report=xml`
- HTML report: `pytest --cov --cov-report=html && open htmlcov/index.html`
