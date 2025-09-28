from datetime import date

import pytest
from sqlalchemy import or_

from fastapi_advanced_filters.enums import OperationEnum
from fastapi_advanced_filters.operation_mapping.sqlalchemy_mapping import OP_MAPPING
from tests._utils import assert_sql_list_equal
from tests.integration.sqlalchemy.models_and_filters import (
    User,
    UserAdvancedFilterExample,
)


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"user_public__first_name__eq": "Alice"}, [User.first_name == "Alice"]),
        ({"user_public__first_name__neq": "Alice"}, [User.first_name != "Alice"]),
        (
            {"user_public__first_name__like": "A%"},
            [OP_MAPPING[OperationEnum.LIKE](User.first_name, "A%")],
        ),
        (
            {"user_public__first_name__ilike": "a%"},
            [OP_MAPPING[OperationEnum.ILIKE](User.first_name, "a%")],
        ),
        (
            {"user_private__full_name__eq": "Alice"},
            [(User.first_name == "Alice") & (User.last_name == "Alice")],
        ),
        (
            {"user_private__birthday__btw": "1990-01-01,2000-12-31"},
            [User.birthday.between(date(1990, 1, 1), date(2000, 12, 31))],
        ),
        (
            {"user_private__is_working__is": True},
            [User.is_working.is_(True)],
        ),
        (
            {"user_private__age__in": "25,30"},
            [User.age.in_([25, 30])],
        ),
        (
            {"user_public__first_name__cont": "li"},
            [OP_MAPPING[OperationEnum.CONT](User.first_name, "li")],
        ),
    ],
)
def test_build_filters_happy_paths(kwargs, expected):
    f = UserAdvancedFilterExample(**kwargs)
    model = f.get_filter_model()
    assert_sql_list_equal(model.filters, expected)


def test_q_search_builds_boolean_clause_list():
    f = UserAdvancedFilterExample(q_search="John")
    model = f.get_filter_model()
    actual = model.q_search
    expected = or_(
        User.first_name.ilike("%John%"),
        User.last_name.ilike("%John%"),
        User.last_name.like("%John%"),
    )
    from tests._utils import assert_sql_equal

    assert_sql_equal(actual, expected)
