# Usage examples (quick and simple)

Below is a minimal, copy‑pasteable setup to get filtering working fast. You
can add sorting, selection, and q_search as needed.

## 1) Define your SQLAlchemy model

```python
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    age = Column(Integer)
    is_working = Column(Boolean)
```

## 2) Create a simple Filter

Give the filter the model and list the fields you want to filter. This creates
query parameters like `first_name__ilike`, `age__gte`, `age__lte`, etc.

```python
from fastapi_advanced_filters import BaseFilter

class UserFilter(BaseFilter):
    class FilterConfig:
        model = User
        fields = ["first_name", "age", "is_working"]
```

Example requests (no prefix):
- `GET /users?first_name__ilike=ali`
- `GET /users?age__gte=21&age__lte=65`
- `GET /users?is_working__is=true`

## 3) Use it in a FastAPI endpoint

```python
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/users")
def get_users(filters: UserFilter = Depends(), db: Session = Depends(get_db)):
    q = db.query(User)
    m = filters.get_filter_model()

    if m.filters:
        q = q.filter(*m.filters)
    # If you add sorting/select/q_search later, see the snippets below

    return q.all()
```

---

## Optional add‑ons

### Sorting

Declare which attributes are sortable, then pass `?sorting=first_name,-age`.

```python
from fastapi_advanced_filters import SortBy

class UserFilterWithSort(BaseFilter):
    class FilterConfig:
        model = User
        fields = ["first_name", "age"]
        sort_by = SortBy(
            model_attrs={
                "first_name": User.first_name,
                "age": User.age,
            }
        )

@app.get("/users-sorted")
def get_users_sorted(
    filters: UserFilterWithSort = Depends(), db: Session = Depends(get_db)
):
    q = db.query(User)
    m = filters.get_filter_model()
    if m.filters:
        q = q.filter(*m.filters)
    if m.sorting:
        q = q.order_by(*m.sorting)
    return q.all()
```

### Selecting (project specific columns)

Pass `?select=first_name,age` or `?select=all`.

```python
from fastapi_advanced_filters import Selectable

class UserFilterWithSelect(BaseFilter):
    class FilterConfig:
        model = User
        fields = ["first_name", "age", "is_working"]
        select_only = Selectable(
            model_attrs={
                "first_name": User.first_name,
                "age": User.age,
                "is_working": User.is_working,
            }
        )

@app.get("/users-select")
def get_users_select(
    filters: UserFilterWithSelect = Depends(), db: Session = Depends(get_db)
):
    q = db.query(User)
    m = filters.get_filter_model()
    if m.selected_columns:
        q = q.with_entities(*m.selected_columns)
    return q.all()
```

### q_search (simple full‑text across a few fields)

Pass `?q_search=john`.

```python
from fastapi_advanced_filters import QSearch, OperationEnum, LogicalOperator

class UserFilterWithQ(BaseFilter):
    class FilterConfig:
        q_search = QSearch(
            model_attrs=[User.first_name],
            op=OperationEnum.ILIKE,
            logical_op=LogicalOperator.OR,
        )

@app.get("/users-q")
def get_users_q(
    filters: UserFilterWithQ = Depends(), db: Session = Depends(get_db)
):
    q = db.query(User)
    m = filters.get_filter_model()
    if m.q_search is not None:
        q = q.filter(m.q_search)
    return q.all()
```

### Pagination

Offset-based pagination: `?limit=20&offset=40`

```python
from fastapi_advanced_filters import PaginationEnum

class UserFilterWithPagination(BaseFilter):
    class FilterConfig:
        model = User
        fields = ["first_name", "age"]
        pagination = PaginationEnum.OFFSET_BASED

@app.get("/users-page")
def get_users_page(
    filters: UserFilterWithPagination = Depends(), db: Session = Depends(get_db)
):
    q = db.query(User)
    m = filters.get_filter_model()
    if m.filters:
        q = q.filter(*m.filters)
    if m.pagination:
        q = q.limit(m.pagination.limit).offset(m.pagination.offset)
    return q.all()
```
