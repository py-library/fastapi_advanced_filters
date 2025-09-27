import pytest
from pydantic import ValidationError

from tests.integration.sqlalchemy.models_and_filters import (
    UserAdvancedFilterExample,
    UserCustomizedFilterExample,
)


def test_offset_pagination_valid():
    m = UserAdvancedFilterExample(limit=10, offset=0).get_filter_model()
    assert m.pagination and (m.pagination.limit, m.pagination.offset) == (10, 0)


def test_offset_pagination_defaults_present():
    m = UserAdvancedFilterExample().get_filter_model()
    assert m.pagination and (m.pagination.limit, m.pagination.offset) == (100, 0)


def test_offset_pagination_large_values():
    m = UserAdvancedFilterExample(limit=1000, offset=5000).get_filter_model()
    assert m.pagination and (m.pagination.limit, m.pagination.offset) == (1000, 5000)


@pytest.mark.parametrize("limit, offset", [(-1, 0), (10, -1), (0, 0)])
def test_offset_pagination_invalid_numbers(limit, offset):
    with pytest.raises(ValueError):
        UserAdvancedFilterExample(limit=limit, offset=offset)


def test_offset_pagination_strings_cast():
    m = UserAdvancedFilterExample(limit="10", offset="0").get_filter_model()
    assert m.pagination and (m.pagination.limit, m.pagination.offset) == (10, 0)


@pytest.mark.parametrize("limit, offset", [(None, 0), (10, None)])
def test_offset_pagination_none_values_invalid(limit, offset):
    with pytest.raises(ValidationError):
        UserAdvancedFilterExample(limit=limit, offset=offset)


def test_page_based_pagination_valid():
    m = UserCustomizedFilterExample(page=1, size=10).get_filter_model()
    assert m.pagination and (m.pagination.limit, m.pagination.offset) == (10, 0)


@pytest.mark.parametrize("page, size", [(0, 10), (1, -10)])
def test_page_based_pagination_invalid(page, size):
    with pytest.raises(ValueError):
        UserCustomizedFilterExample(page=page, size=size)


@pytest.mark.parametrize("page, size", [(None, 10), (1, None)])
def test_page_based_pagination_none_values_invalid(page, size):
    with pytest.raises(ValidationError):
        UserCustomizedFilterExample(page=page, size=size)


def test_page_based_pagination_strings_cast():
    m = UserCustomizedFilterExample(page="1", size="10").get_filter_model()
    assert m.pagination and (m.pagination.limit, m.pagination.offset) == (10, 0)
