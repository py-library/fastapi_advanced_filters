from fastapi_advanced_filters.data_classes import FieldCriteria, Selectable, SortBy
from fastapi_advanced_filters.enums import OperationEnum


def test_sortby_alias_camelcase_cache_and_access():
    sb = SortBy(model_attrs={"first_name": object()}, alias_as_camelcase=True)
    # names are exposed as camelCase
    names = sb.get_names()
    assert names == ["firstName"]
    # access by alias
    assert sb.get_attr("firstName") is not None


def test_sortby_non_alias_access():
    sb = SortBy(model_attrs={"name": object()}, alias_as_camelcase=False)
    assert sb.get_names() == ["name"]
    assert sb.get_attr("name") is not None


def test_selectable_alias_and_plain():
    sel = Selectable(model_attrs={"user_name": 1}, alias_as_camelcase=True)
    assert sel.get_names() == ["userName"]
    assert sel.get_attr("userName") == 1
    sel2 = Selectable(model_attrs={"email": 2})
    assert sel2.get_names() == ["email"]
    assert sel2.get_attr("email") == 2


def test_field_criteria_alias_and_names_with_prefix():
    fc = FieldCriteria(
        name="age",
        field_type=int,
        op=(OperationEnum.GT,),
        prefix="user",
        alias_as_camelcase=True,
    )
    # snake name
    assert fc.get_name() == "user__age"
    # field and alias
    assert fc.get_field_name(OperationEnum.GT) == "user__age__gt"
    assert fc.get_alias_name(OperationEnum.GT) == "userAgeGt"


def test_field_criteria_names_without_prefix_and_plain_alias():
    fc = FieldCriteria(
        name="status",
        field_type=str,
        op=(OperationEnum.EQ,),
        alias_as_camelcase=False,
    )
    assert fc.get_name() == "status"
    assert fc.get_field_name(OperationEnum.EQ) == "status__eq"
    assert fc.get_alias_name(OperationEnum.EQ) == "status__eq"
