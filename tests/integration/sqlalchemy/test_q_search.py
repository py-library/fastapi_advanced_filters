import pytest
from sqlalchemy import or_

from tests._utils import assert_sql_equal
from tests.integration.sqlalchemy.models_and_filters import (
    AdvancedQ,
    SimpleQ,
    User,
    UserAdvancedFilterExample,
    UserSimpleFilterExample,
)


@pytest.mark.parametrize("query", ["Alice", "Bob", "123", "O'Connor"])
def test_simple_q_search_or_ilike(query):
    filters = UserSimpleFilterExample(q_search=query)
    m = filters.get_filter_model()
    # We expect an OR of ILIKE against first_name and last_name
    expected = or_(
        User.first_name.ilike(f"%{query}%"),
        User.last_name.ilike(f"%{query}%"),
    )
    assert_sql_equal(m.q_search, expected)


def test_simple_q_search_empty_returns_none():
    assert UserSimpleFilterExample(q_search="").get_filter_model().q_search is None
    assert UserSimpleFilterExample().get_filter_model().q_search is None


@pytest.mark.parametrize("query", ["Alice", "Bob"])
def test_advanced_q_search_or_like_ilike(query):
    filters = UserAdvancedFilterExample(q_search=query)
    actual = filters.get_filter_model().q_search
    expected = or_(
        User.first_name.ilike(f"%{query}%"),
        User.last_name.ilike(f"%{query}%"),
        User.last_name.like(f"%{query}%"),
    )
    assert_sql_equal(actual, expected)


def test_q_search_mixins_direct_build():
    assert SimpleQ(q_search="abc").build_q_search() is not None
    assert AdvancedQ(q_search="x").build_q_search() is not None
