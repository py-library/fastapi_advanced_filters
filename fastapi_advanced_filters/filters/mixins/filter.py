from datetime import datetime
from typing import Any

from pydantic.fields import FieldInfo

from fastapi_advanced_filters.data_classes import FieldCriteria
from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum


class FilterMixin:
    __op_mapping__: dict[OperationEnum, Any]
    __logical_op_mapping__: dict[LogicalOperator, Any]

    def __get_filterable_field_metadata(
        self, attr_name: str
    ) -> tuple[OperationEnum, FieldCriteria] | None:
        # Access model_fields on the class to avoid Pydantic V2.11 deprecation warnings
        field: FieldInfo = type(self).model_fields.get(attr_name)  # type: ignore
        if (
            hasattr(field, "metadata")
            and field.metadata
            and isinstance(field.metadata, list)
            and len(field.metadata) == 2
        ) and (
            (operation := field.metadata[0])
            and (field_metadata := field.metadata[1])
            and isinstance(field_metadata, FieldCriteria)
        ):
            return operation, field_metadata
        return None

    def __build_operation(
        self, operation: OperationEnum, field: FieldCriteria, value: Any
    ) -> list[Any] | Any:
        assert (
            field.model_attr is not None
            or field.custom_filter_per_op is not None
            or field.model_attrs_with_logical_op is not None
        ), (
            f"Field '{field.name}' must have either 'model_attr', "
            f"'custom_filter_per_op' or 'model_attrs_with_logical_op' defined."
        )
        if isinstance(value, datetime):
            value = value.replace(tzinfo=None)
        if field.custom_filter_per_op and callable(field.custom_filter_per_op):
            return field.custom_filter_per_op(operation, value)
        if (
            self.__op_mapping__.get(operation, None) is not None
            and field.model_attr is not None
        ):
            assert isinstance(field.model_attr, (list, tuple)) is False, (
                f"Field '{field.name}' has multiple 'model_attr' defined. "
                f"Use 'model_attrs_with_logical_op' instead."
            )
            condition = self.__op_mapping__[operation](field.model_attr, value)
            return condition
        if (
            field.model_attrs_with_logical_op is not None
            and self.__op_mapping__.get(operation, None) is not None
        ):
            assert isinstance(field.model_attrs_with_logical_op, (tuple, list)), (
                f"Field '{field.name}' must have 'model_attrs_with_logical_op' "
                f"defined as a list."
            )
            model_attrs, logical_operator = field.model_attrs_with_logical_op
            assert isinstance(model_attrs, (list, tuple)), (
                f"Field '{field.name}' must have list of 'model_attrs' defined in "
                f"'model_attrs_with_logical_op'."
            )
            assert (
                isinstance(logical_operator, LogicalOperator)
                and self.__logical_op_mapping__.get(logical_operator, None) is not None
            ), (
                f"Field '{field.name}' must have 'logical_operator' defined in "
                f"'model_attrs_with_logical_op'."
            )
            conditions: list[Any] = []
            for model_attr in model_attrs:
                if (condition := self.__op_mapping__.get(operation, None)) is not None:
                    conditions.append(condition(model_attr, value))
            return (
                self.__logical_op_mapping__[logical_operator](*conditions)
                if conditions
                else None
            )
        return None

    def build_filters(self) -> list[Any] | None:
        filters: list[Any] = []
        for key, value in self.model_dump(  # type: ignore
            exclude_defaults=True,
            exclude_none=True,
            exclude_unset=True,
            exclude=(
                "sorting",
                "select",
                "q_search",
                "limit",
                "offset",
                "page",
                "page_size",
            ),
        ).items():
            metadata: tuple[
                OperationEnum, FieldCriteria
            ] | None = self.__get_filterable_field_metadata(key)
            if metadata is None:
                continue
            assert isinstance(metadata, (tuple, list)) and len(metadata) == 2, (
                f"Field '{key}' must have metadata defined as a tuple of "
                f"(operation, metadata)."
            )
            if (conditions := self.__build_operation(*metadata, value)) is not None:
                filters.append(conditions)
        return filters if filters else None
