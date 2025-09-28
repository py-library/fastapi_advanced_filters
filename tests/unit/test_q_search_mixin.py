from typing import Annotated

from pydantic import BaseModel, Field

from fastapi_advanced_filters.data_classes import AdvancedQSearch, QSearch
from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum
from fastapi_advanced_filters.filters.mixins import QSearchMixin


class DummyQ(QSearchMixin, BaseModel):
    __op_mapping__ = {OperationEnum.LIKE: lambda col, val: ("LIKE", col, val)}
    __logical_op_mapping__ = {
        LogicalOperator.OR: lambda *conds: ("OR",) + conds,
        LogicalOperator.AND: lambda *conds: ("AND",) + conds,
    }

    q_search: Annotated[
        str | None,
        Field(default=None),
        QSearch(model_attrs=["fname", "lname"], op=OperationEnum.LIKE),
    ]


class DummyAdvancedQ(QSearchMixin, BaseModel):
    __op_mapping__ = {
        OperationEnum.LIKE: lambda col, val: ("LIKE", col, val),
        OperationEnum.ILIKE: lambda col, val: ("ILIKE", col, val),
    }
    __logical_op_mapping__ = {
        LogicalOperator.OR: lambda *conds: ("OR",) + conds,
    }

    q_search: Annotated[
        str | None,
        Field(default=None),
        AdvancedQSearch(
            model_attrs_with_op={
                OperationEnum.LIKE: ["fname"],
                OperationEnum.ILIKE: ["bio"],
            }
        ),
    ]


def test_q_search_none_returns_none():
    assert DummyQ().build_q_search() is None


def test_simple_q_search_builds_conditions():
    dq = DummyQ(q_search="a")
    built = dq.build_q_search()
    assert built[0] == "OR"
    assert ("LIKE", "fname", "a") in built
    assert ("LIKE", "lname", "a") in built


def test_advanced_q_search_builds_conditions():
    dq = DummyAdvancedQ(q_search="a")
    built = dq.build_q_search()
    assert built[0] == "OR"
    assert ("LIKE", "fname", "a") in built
    assert ("ILIKE", "bio", "a") in built


class DummyAdvancedQNoOps(QSearchMixin, BaseModel):
    __op_mapping__ = {}
    __logical_op_mapping__ = {LogicalOperator.OR: lambda *conds: ("OR",) + conds}
    q_search: Annotated[
        str | None,
        Field(default=None),
        AdvancedQSearch(model_attrs_with_op={OperationEnum.LIKE: [None]}),
    ]


def test_advanced_q_search_returns_none_when_no_conditions():
    # No mapped ops and model attr is None -> conditions list stays empty ->
    # returns None
    dq = DummyAdvancedQNoOps(q_search="x")
    assert dq.build_q_search() is None
