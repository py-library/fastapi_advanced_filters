from typing import Annotated, Any, Dict, Generator, TypeVar, Union

from pydantic.fields import Field, FieldInfo

try:
    from sqlalchemy.orm.attributes import InstrumentedAttribute
except ImportError:  # pragma: no cover
    InstrumentedAttribute = TypeVar("InstrumentedAttribute")  # type: ignore

from fastapi_advanced_filters.data_classes import FieldCriteria
from fastapi_advanced_filters.enums import OperationEnum


def attrs_to_field_criteria(
    model_cls: type,
    fields: list[str] | str | None = None,
    prefix: str | None = None,
    op: tuple[OperationEnum, ...] | None = None,
) -> Generator[FieldCriteria, None, None]:
    # Normalize fields into a list of attribute names
    if fields is None:
        model_attrs: list[Any] = []
    elif fields == "__all__":
        model_attrs = __get_all_fields_from_model(model_cls)
    elif isinstance(fields, str):
        model_attrs = [fields]
    else:
        model_attrs = fields

    for attr in model_attrs:
        if isinstance(attr, FieldCriteria):
            yield attr
            continue

        field: Any = getattr(model_cls, attr)

        yield __get_field_criteria_from_model(
            field_type=__type_from_attr(field),
            model_attr=field,
            field_name=attr,
            prefix=prefix,
            op=op or (OperationEnum.EQ,),
        )


def __type_from_attr(attr: Any) -> type:
    if hasattr(attr, "property") and hasattr(attr.property, "columns"):
        column = attr.property.columns[0]
        return column.type.python_type
    return str  # Default to str if type cannot be determined


def __get_all_fields_from_model(model_cls: type) -> list[str]:
    assert model_cls is not None, "Model class cannot be None."
    return [
        attr
        for attr in dir(model_cls)
        if not attr.startswith("_")
        and (
            isinstance(getattr(model_cls, attr), FieldInfo)
            or isinstance(getattr(model_cls, attr), InstrumentedAttribute)
        )
    ]


def __get_field_criteria_from_model(
    field_type: type,
    model_attr: type,
    field_name: str,
    prefix: str | None,
    op: tuple[OperationEnum, ...],
) -> FieldCriteria:
    return FieldCriteria(
        name=field_name,
        field_type=field_type,
        model_attr=model_attr,
        op=op,
        prefix=prefix,
    )


def from_field_criteria_to_attr(
    field_criteria: FieldCriteria,
) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}
    for op in field_criteria.op:
        annotation_type: type = field_criteria.field_type
        field_name: str = field_criteria.get_field_name(op)
        is_required: bool = (
            field_criteria.required_op is not None and op in field_criteria.required_op
        )
        kwargs: dict[str, Any] = field_criteria.fields_kwargs.copy()
        if is_required:
            kwargs["default"] = ...  # type: ignore
        else:
            kwargs["default"] = None
        fields[field_name] = Annotated[
            Union[annotation_type, str, None],
            Field(
                alias=(field_criteria.get_alias_name(op)),
                title=f"Filter by {field_criteria.name} with operation {op}",
                description=f"Filter by {field_criteria.name} with operation {op}",
                **kwargs,
            ),
            op,
            field_criteria,
        ]
    return fields
