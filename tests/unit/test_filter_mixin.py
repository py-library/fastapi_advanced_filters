from datetime import datetime, timezone
from typing import Annotated

import pytest
from pydantic import BaseModel, Field

from fastapi_advanced_filters.data_classes import FieldCriteria
from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum
from fastapi_advanced_filters.filters.mixins import FilterMixin


class DummyFilter(FilterMixin, BaseModel):
    __op_mapping__ = {
        OperationEnum.EQ: lambda col, val: (col, "=", val),
        OperationEnum.GT: lambda col, val: (col, ">", val),
    }
    __logical_op_mapping__ = {
        LogicalOperator.OR: lambda *conds: ("OR",) + conds,
        LogicalOperator.AND: lambda *conds: ("AND",) + conds,
    }

    # Single model_attr
    age__gt: Annotated[
        int | None,
        Field(default=None, alias="age__gt"),
        OperationEnum.GT,
        FieldCriteria(
            name="age", field_type=int, op=(OperationEnum.GT,), model_attr="age_column"
        ),
    ]

    # non-filter normal field should be excluded by exclude list in build_filters
    plain: str | None = Field(default=None)

    # Field with operation not present in __op_mapping__ to force
    # __build_operation to return None
    unknown__lte: Annotated[
        int | None,
        Field(default=None, alias="unknown__lte"),
        OperationEnum.LTE,
        FieldCriteria(
            name="unknown",
            field_type=int,
            op=(OperationEnum.LTE,),
            model_attrs_with_logical_op=(
                ["col1", "col2"],
                LogicalOperator.OR,
            ),
        ),
    ]

    # datetime value path to exercise tz-stripping branch
    created_at__eq: Annotated[
        datetime | None,
        Field(default=None, alias="created_at__eq"),
        OperationEnum.EQ,
        FieldCriteria(
            name="created_at",
            field_type=datetime,
            op=(OperationEnum.EQ,),
            model_attr="created_col",
        ),
    ]

    # Using model_attrs_with_logical_op
    name__eq: Annotated[
        str | None,
        Field(default=None, alias="name__eq"),
        OperationEnum.EQ,
        FieldCriteria(
            name="name",
            field_type=str,
            op=(OperationEnum.EQ,),
            model_attrs_with_logical_op=(
                ["first_name_col", "last_name_col"],
                LogicalOperator.OR,
            ),
        ),
    ]

    # Field with empty model_attrs to drive the "conditions -> [] -> None" path
    empty_attrs__eq: Annotated[
        str | None,
        Field(default=None, alias="empty_attrs__eq"),
        OperationEnum.EQ,
        FieldCriteria(
            name="empty",
            field_type=str,
            op=(OperationEnum.EQ,),
            model_attrs_with_logical_op=([], LogicalOperator.OR),
        ),
    ]


def test_build_filters_none_when_no_values():
    df = DummyFilter()
    assert df.build_filters() is None


def test_build_filters_with_model_attr_and_logical_attrs():
    df = DummyFilter(age__gt=30, name__eq="A")
    built = df.build_filters()
    # Should produce two conditions
    assert isinstance(built, list) and len(built) == 2
    # First: single model_attr path
    assert built[0] == ("age_column", ">", 30)
    # Second: logical OR path returns composed structure
    assert built[1][0] == "OR" and len(built[1]) == 3


def test_build_filters_skips_plain_field_and_unknown_metadata():
    # plain field should not appear in filters
    df = DummyFilter(plain="value")
    assert df.build_filters() is None


def test_build_filters_operation_mapping_missing_returns_none():
    # Set a value for a field whose operation isn't mapped; should produce no filters
    df = DummyFilter(unknown__lte=5)
    assert df.build_filters() is None


def test_build_filters_datetime_value_strips_tz():
    aware = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    df = DummyFilter(created_at__eq=aware)
    built = df.build_filters()
    # Should produce naive datetime in payload
    assert built and built[0][2].tzinfo is None


def test_build_filters_returns_none_when_model_attrs_empty():
    df = DummyFilter(empty_attrs__eq="x")
    assert df.build_filters() is None


def test_asserts_when_model_attr_is_sequence_instead_of_scalar():
    class DF(DummyFilter):
        # Provide a bad field where model_attr is a list which should raise assertion
        bad__eq: Annotated[
            str | None,
            Field(default=None, alias="bad__eq"),
            OperationEnum.EQ,
            FieldCriteria(
                name="bad",
                field_type=str,
                op=(OperationEnum.EQ,),
                model_attr=["col1", "col2"],
            ),
        ]

    with pytest.raises(AssertionError):
        DF(bad__eq="x").build_filters()


def test_asserts_when_logical_operator_not_mapped():
    class DF(DummyFilter):
        __logical_op_mapping__ = {}  # remove OR/AND to trigger assertion

    with pytest.raises(AssertionError):
        DF(name__eq="A").build_filters()


def test_asserts_when_model_attrs_not_sequence():
    class DF(DummyFilter):
        wrong__eq: Annotated[
            str | None,
            Field(default=None, alias="wrong__eq"),
            OperationEnum.EQ,
            FieldCriteria(
                name="wrong",
                field_type=str,
                op=(OperationEnum.EQ,),
                model_attrs_with_logical_op=("notalist", LogicalOperator.OR),
            ),
        ]

    with pytest.raises(AssertionError):
        DF(wrong__eq="x").build_filters()
