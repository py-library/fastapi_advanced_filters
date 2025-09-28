from typing import Any, Callable

from pydantic.fields import FieldInfo

from fastapi_advanced_filters.data_classes import AdvancedQSearch, QSearch
from fastapi_advanced_filters.enums import OperationEnum


class QSearchMixin:
    __op_mapping__: dict[OperationEnum, Callable[..., Any]]
    __logical_op_mapping__: dict[Any, Callable[..., Any]]

    def __get_q_search_metadata(self, attr_name: str) -> QSearch | AdvancedQSearch:
        # Access model_fields on the class to avoid Pydantic V2.11 deprecation warnings
        field: FieldInfo = type(self).model_fields.get(attr_name)  # type: ignore
        assert (
            hasattr(field, "metadata")
        ) and field.metadata, f"Field '{attr_name}' has no metadata."
        assert isinstance(field.metadata[0], (QSearch, AdvancedQSearch)), (
            f"Field '{attr_name}' metadata is not of type "
            f"(QSearch, AdvancedQSearch)."
        )
        return field.metadata[0]

    def build_q_search(self, attr_name: str = "q_search") -> Any | None:
        if not hasattr(self, attr_name) or not getattr(self, attr_name):
            return None
        field_metadata = self.__get_q_search_metadata(attr_name)
        q_search: str = getattr(self, attr_name)
        assert field_metadata is not None and isinstance(
            field_metadata, (QSearch, AdvancedQSearch)
        ), (
            f"Field '{attr_name}' must have metadata of type "
            f"(QSearch, AdvancedQSearch)."
        )
        if isinstance(field_metadata, QSearch):
            return self.__build_q_search_operation(field_metadata, q_search)
        return self.__build_advanced_q_search_operation(field_metadata, q_search)

    def __build_q_search_operation(self, field: QSearch, value: str) -> Any:
        condition: Callable[..., Any] | None = self.__op_mapping__.get(field.op, None)
        assert (
            field.model_attrs is not None and condition is not None
        ), f"Field '{field.name}' must have 'model_attrs' and valid 'op' defined."
        conditions = [
            condition(model_attr, value)
            for model_attr in field.model_attrs
            if model_attr is not None
        ]
        return (
            self.__logical_op_mapping__[field.logical_op](*conditions)
            if conditions
            else None
        )

    def __build_advanced_q_search_operation(
        self, field: AdvancedQSearch, value: str
    ) -> Any:
        assert (
            field.model_attrs_with_op is not None
        ), f"Field '{field.name}' must have 'model_attrs_with_op' defined."
        assert (
            field.logical_op is not None
        ), f"Field '{field.name}' must have 'logical_op' defined."
        conditions = []
        for op, model_attrs in field.model_attrs_with_op.items():
            if (condition := self.__op_mapping__.get(op, None)) is not None:
                conditions.extend(
                    [
                        condition(model_attr, value)
                        for model_attr in model_attrs
                        if model_attr is not None
                    ]
                )

        return (
            self.__logical_op_mapping__[field.logical_op](*conditions)
            if conditions
            else None
        )
