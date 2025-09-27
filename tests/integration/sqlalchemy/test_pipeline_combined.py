from sqlalchemy import or_

from tests._utils import _sql, assert_sql_equal, assert_sql_list_equal
from tests.integration.sqlalchemy.models_and_filters import (
    User,
    UserAdvancedFilterExample,
)


def test_filter_and_sort_pipeline():
    f = UserAdvancedFilterExample(
        user_public__first_name__eq="Alice",
        sort_by="age,-createdAt",
    )
    m = f.get_filter_model()
    assert_sql_list_equal(m.filters, [User.first_name == "Alice"])
    assert [_sql(f_) for f_ in m.sorting] == [
        _sql(User.age.asc()),
        _sql(User.created_at.desc()),
    ]


def test_filter_and_q_search_pipeline():
    f = UserAdvancedFilterExample(user_private__age__gt=18, q_search="John")
    m = f.get_filter_model()
    assert [str(col) for col in m.filters] == [str(User.age > 18)]
    assert_sql_equal(
        m.q_search,
        or_(
            User.first_name.ilike("%John%"),
            User.last_name.ilike("%John%"),
            User.last_name.like("%John%"),
        ),
    )


def test_full_pipeline_all_features():
    f = UserAdvancedFilterExample(
        user_private__age__gt=18,
        sort_by="firstName",
        q_search="John",
        select="firstName,age",
    )
    m = f.get_filter_model()
    assert_sql_list_equal(m.filters, [User.age > 18])
    assert [_sql(f_) for f_ in m.sorting] == [_sql(User.first_name.asc())]
    assert_sql_equal(
        m.q_search,
        or_(
            User.first_name.ilike("%John%"),
            User.last_name.ilike("%John%"),
            User.last_name.like("%John%"),
        ),
    )
    assert [str(c) for c in m.selected_columns] == [
        str(User.first_name),
        str(User.age),
    ]


def test_pipeline_defaults_when_empty():
    f = UserAdvancedFilterExample()
    m = f.get_filter_model()
    assert m.filters is None
    assert m.sorting is None
    assert m.q_search is None
    # default select_only returns full set
    assert [str(c) for c in m.selected_columns] == [
        str(User.first_name),
        str(User.age),
        str(User.is_working),
        str(User.birthday),
    ]
