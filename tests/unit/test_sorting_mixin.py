from typing import Annotated

import pytest
from pydantic import BaseModel, Field

from fastapi_advanced_filters.data_classes import SortBy
from fastapi_advanced_filters.enums import OrderEnum
from fastapi_advanced_filters.filters.mixins import SortingMixin


class DummySort(SortingMixin, BaseModel):
    __sorting_mapping__ = {
        OrderEnum.ASC: lambda x: (x, "ASC"),
        OrderEnum.DESC: lambda x: (x, "DESC"),
    }

    sorting: Annotated[
        list[tuple[str, OrderEnum]] | None,
        Field(default=None),
        SortBy(model_attrs={"name": "COL_NAME"}),
    ]


def test_build_sorting_returns_none_when_not_set():
    assert DummySort().build_sorting() is None


@pytest.mark.parametrize(
    "input_sort, expected",
    [
        ([("name", OrderEnum.ASC)], [("COL_NAME", "ASC")]),
        ([("name", OrderEnum.DESC)], [("COL_NAME", "DESC")]),
    ],
)
def test_build_sorting_happy_paths(input_sort, expected):
    ds = DummySort(sorting=input_sort)
    assert ds.build_sorting() == expected
