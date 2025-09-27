# Installation

fastapi-filter supports Python 3.9+ and integrates with FastAPI and Pydantic v2.

## Using pip

```bash
pip install fastapi-filter
```

SQLAlchemy extras:

```bash
pip install "fastapi-filter[sqlalchemy]"
```

## Using Poetry

```bash
poetry add fastapi-filter
# or with extras
poetry add fastapi-filter -E sqlalchemy
```

## Optional dependencies

- SQLAlchemy: required for SQL expression generation and operation mappings.
- aiosqlite/PostgreSQL driver: only needed by your app/database layer, not by this library itself.

## Minimum versions

- Python: >= 3.9
- FastAPI: >= 0.100.0
- Pydantic: >= 2.0.0
- SQLAlchemy (optional): >= 1.4.36, < 2.1.0
