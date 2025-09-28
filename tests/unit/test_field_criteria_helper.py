from fastapi_advanced_filters.data_classes import FieldCriteria
from fastapi_advanced_filters.enums import OperationEnum
from fastapi_advanced_filters.filter_metaclass.helpers.field_criteria import (
    attrs_to_field_criteria,
    from_field_criteria_to_attr,
)


class DummyModel:
    # plain attribute without SQLAlchemy instrumentation -> __type_from_attr
    # default path (str)
    plain_attr = "value"


def test_attrs_to_field_criteria_default_type_str():
    # Use non-ORM attribute to hit __type_from_attr default branch
    gen = attrs_to_field_criteria(
        DummyModel, fields=["plain_attr"], prefix=None, op=(OperationEnum.EQ,)
    )
    crit = next(gen)
    assert isinstance(crit, FieldCriteria)
    assert crit.name == "plain_attr"
    assert crit.field_type is str  # default branch


def test_from_field_criteria_to_attr_required_and_optional():
    fc_required = FieldCriteria(
        name="age",
        field_type=int,
        op=(OperationEnum.EQ, OperationEnum.GT),
        required_op=(OperationEnum.EQ,),
        prefix=None,
    )
    attrs = from_field_criteria_to_attr(fc_required)
    # Two generated annotated fields (age__eq and age__gt)
    assert set(attrs.keys()) == {"age__eq", "age__gt"}
    # Verify Pydantic Field defaults: required for eq, optional for gt
    eq_field = attrs["age__eq"].__metadata__[0]
    gt_field = attrs["age__gt"].__metadata__[0]
    assert eq_field.default
    assert gt_field.default is None
