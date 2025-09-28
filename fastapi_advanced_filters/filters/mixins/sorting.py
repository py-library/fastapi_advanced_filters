from typing import Any

from pydantic.fields import FieldInfo

from fastapi_advanced_filters.data_classes import SortBy
from fastapi_advanced_filters.enums import OrderEnum


class SortingMixin:
    __sorting_mapping__: dict[OrderEnum, Any]

    def __get_sorting_metadata(self, attr_name: str) -> SortBy:
        # Access model_fields on the class to avoid Pydantic V2.11 deprecation warnings
        field: FieldInfo = type(self).model_fields.get(attr_name)  # type: ignore
        assert (
            hasattr(field, "metadata")
        ) and field.metadata, f"Field '{attr_name}' has no metadata."
        assert isinstance(
            field.metadata[0], SortBy
        ), f"Field '{attr_name}' metadata is not of type {SortBy.__name__}."
        return field.metadata[0]

    def build_sorting(self, attr_name: str = "sorting") -> list[Any] | None:
        if not hasattr(self, attr_name) or not getattr(self, attr_name):
            return None
        field_metadata: SortBy = self.__get_sorting_metadata(attr_name)
        sorting: list[tuple[str, OrderEnum]] = getattr(self, attr_name)
        sort_by: list[Any] = []
        for sort_field, op in sorting:
            field_attr = field_metadata.get_attr(sort_field)
            if field_attr and self.__sorting_mapping__.get(op) is not None:
                sort_by.append(self.__sorting_mapping__[op](field_attr))
        return sort_by if sort_by else None
