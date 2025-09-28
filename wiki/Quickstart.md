# Quickstart

Example SQLAlchemy model and filter class:

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
        q_search = QSearch(
            model_attrs=[User.first_name, User.last_name],
            op=OperationEnum.ILIKE,
            logical_op=LogicalOperator.OR,
        )
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
```

FastAPI integration:

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
