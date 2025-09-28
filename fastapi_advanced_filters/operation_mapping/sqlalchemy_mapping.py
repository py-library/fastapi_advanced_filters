import operator
from datetime import date, datetime
from typing import Any, Callable

try:
    from sqlalchemy import ARRAY, Boolean, Column, String, and_, or_
except ImportError:  # pragma: no cover
    ARRAY = Boolean = Column = or_ = and_ = String = None  # type: ignore

from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum, OrderEnum


def in_funct(field: Any, values: str) -> Any:  # type: ignore
    try:
        conditions = []
        if ARRAY is not None and isinstance(getattr(field, "type", None), ARRAY):
            return field.contains([val for val in values.split(",") if val])
        for value in values.split(","):
            if Boolean is not None and isinstance(field.type, Boolean):
                conditions.append(False if value == "false" or value == "0" else True)
            else:
                conditions.append(field.type.python_type(value))
        return field.in_(conditions)
    except ValueError:
        return None


def not_in_funct(field: Any, values: str) -> Any:  # type: ignore
    try:
        conditions = []
        for value in values.split(","):
            if Boolean is not None and isinstance(field.type, Boolean):
                conditions.append(False if value == "false" or value == "0" else True)
            else:
                conditions.append(field.type.python_type(value))
        return ~field.in_(conditions)
    except ValueError:
        return None


def contains(field: Any, val: str) -> Any:  # type: ignore
    if ARRAY is not None and isinstance(getattr(field, "type", None), ARRAY):
        return field.any([val for val in val.split(",") if val])
    if String is not None and isinstance(field.type, String):
        return or_(field.contains(val) for val in val.split(",") if val)
    return or_(field == i for i in val.split(",") if i)


def between(field: Any, values: str) -> Any:  # type: ignore
    parts = [p for p in values.split(",") if p]
    if len(parts) >= 2 and getattr(field.type, "python_type", None) in (int, float):
        split_values = list(map(int, parts))
        return field.between(min(split_values), max(split_values))
    if len(parts) >= 2 and getattr(field.type, "python_type", None) in (
        date,
        datetime,
    ):
        # parse into date if date-like, otherwise datetime.fromisoformat
        # would be fallback
        try:
            split_dates = list(map(date.fromisoformat, parts))
        except ValueError:
            split_dates = list(map(lambda x: datetime.fromisoformat(x).date(), parts))
        return field.between(min(split_dates), max(split_dates))
    raise ValueError("Invalid values for between operation")


OP_MAPPING: dict[OperationEnum, Callable[..., Any]] = {
    OperationEnum.LIKE: lambda x, y: x.like(f"%{y}%"),
    OperationEnum.ILIKE: lambda x, y: x.ilike(f"%{y}%"),
    OperationEnum.EQ: operator.eq,
    OperationEnum.NEQ: operator.ne,
    OperationEnum.GT: operator.gt,
    OperationEnum.GTE: operator.ge,
    OperationEnum.LTE: operator.le,
    OperationEnum.LT: operator.lt,
    OperationEnum.IS: lambda x, y: x.is_(y),
    OperationEnum.IN: in_funct,
    OperationEnum.CONT: contains,
    OperationEnum.NOTIN: not_in_funct,
    OperationEnum.ISNULL: lambda x, y: x.is_(None) if y else x.is_not(None),
    OperationEnum.BTW: between,
}

SORTING_MAPPING: dict[OrderEnum, Callable[[Any], Any]] = {
    OrderEnum.ASC: lambda x: x.asc(),
    OrderEnum.DESC: lambda x: x.desc(),
}

LOGICAL_OP_MAPPING: dict[LogicalOperator, Callable[..., Any]] = {
    LogicalOperator.AND: and_,
    LogicalOperator.OR: or_,
}
