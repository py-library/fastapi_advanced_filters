import pytest

from fastapi_advanced_filters.utils import (
    to_camel_case,
    to_snake_case,
    validate_selectable_schema,
    validate_sortable_schema,
)


def test_to_camel():
    assert to_camel_case("user_name") == "userName"
    assert to_camel_case("api_key") == "apiKey"
    assert to_camel_case("API_Key") == "APIKey"
    assert to_camel_case("") == ""


def test_to_snake():
    assert to_snake_case("userName") == "user_name"
    assert to_snake_case("apiKey") == "api_key"
    assert to_snake_case("APIKey") == "apikey"
    assert to_snake_case("") == ""


def test_validate_selectable_schema():
    assert validate_selectable_schema(["name", "age"])("all") == ["name", "age"]
    assert validate_selectable_schema(["name", "age"])("name,age") == ["name", "age"]
    assert validate_selectable_schema(["name", "age"])("name,age") == ["name", "age"]
    with pytest.raises(ValueError) as e:
        validate_selectable_schema(["name", "age"])("")
        assert (
            str(e)
            == "select must be 'all', a list of strings, or a comma-separated string"
        )
    with pytest.raises(ValueError) as e:
        validate_selectable_schema(["name", "age"])(",")
        assert (
            str(e)
            == "select must be 'all', a list of strings, or a comma-separated string"
        )
    with pytest.raises(ValueError) as e:
        validate_selectable_schema(["name"])("name_sdd,123")
        assert str(e) == "Field 'name_sdd' is not selectable"


def test_validate_sortable_schema():
    assert validate_sortable_schema(["name", "age"])("name,-age") == [
        ("name", "asc"),
        ("age", "desc"),
    ]
    assert validate_sortable_schema(["name", "age"])("-name,age") == [
        ("name", "desc"),
        ("age", "asc"),
    ]
    with pytest.raises(ValueError) as e:
        validate_sortable_schema(["name"])("123")
        assert (
            str(e) == "sort_by must be a string, a list of strings, or a list of "
            "(field, order) tuples"
        )
    with pytest.raises(ValueError) as e:
        validate_sortable_schema(["name"])("name,123")
        assert str(e) == "Field '123' is not sortable"
    with pytest.raises(ValueError) as e:
        validate_sortable_schema(["name"])("name,ascending")
        assert str(e) == "Field 'ascending' is not sortable"
