from typing import Annotated

import pytest
from pydantic import BaseModel, Field

from fastapi_filters.src.data_classes import Selectable
from fastapi_filters.src.filters.mixins import SelectMixin


class DummySelect(SelectMixin, BaseModel):
    select: Annotated[
        str | list[str] | None,
        Field(default=None),
        Selectable(model_attrs={"a": 1, "b": 2}),
    ]


def test_build_select_returns_none_when_not_set():
    assert DummySelect().build_selectable_fields() is None


@pytest.mark.parametrize(
    "value, expected",
    [
        ("all", [1, 2]),
        (["b"], [2]),
    ],
)
def test_build_select_various_inputs(value, expected):
    ds = DummySelect(select=value)
    assert ds.build_selectable_fields() == expected


def test_build_select_returns_none_when_attr_missing():
    # attr does not exist on model -> early None branch
    assert DummySelect().build_selectable_fields("missing") is None


def test_build_select_returns_none_when_unknown_fields():
    ds = DummySelect(select=["z"])  # not in selectable map
    assert ds.build_selectable_fields() is None
