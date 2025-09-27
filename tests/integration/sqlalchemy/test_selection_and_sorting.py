import pytest

from tests._utils import _sql
from tests.integration.sqlalchemy.models_and_filters import (
    User,
    UserAdvancedFilterExample,
)


@pytest.mark.parametrize(
    "sort_by, expected_suffix",
    [
        ("firstName", "ASC"),
        ("-firstName", "DESC"),
    ],
)
def test_sorting_builds_sql(sort_by, expected_suffix):
    m = UserAdvancedFilterExample(sort_by=sort_by).get_filter_model()
    sql = _sql(m.sorting[0])
    assert sql.endswith(expected_suffix)


def test_sorting_multiple_fields():
    m = UserAdvancedFilterExample(sort_by="firstName,-age,createdAt").get_filter_model()
    s = [_sql(x) for x in m.sorting]
    assert s[0].endswith("ASC") and s[1].endswith("DESC") and s[2].endswith("ASC")


@pytest.mark.parametrize(
    "select, expected",
    [
        ("firstName", [User.first_name]),
        ("firstName,age", [User.first_name, User.age]),
        ("all", [User.first_name, User.age, User.is_working, User.birthday]),
    ],
)
def test_selectable_columns(select, expected):
    m = UserAdvancedFilterExample(select=select).get_filter_model()
    assert [str(c) for c in m.selected_columns] == [str(x) for x in expected]
