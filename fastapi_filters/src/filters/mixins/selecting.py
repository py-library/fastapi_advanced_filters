from typing import Any

from pydantic.fields import FieldInfo

from fastapi_filters.src.data_classes import Selectable


class SelectMixin:
    def __get_selectable_metadata(self, attr_name: str) -> Selectable:
        # Access model_fields on the class to avoid Pydantic V2.11 deprecation warnings
        field: FieldInfo = type(self).model_fields.get(attr_name)  # type: ignore
        assert (
            hasattr(field, "metadata")
        ) and field.metadata, f"Field '{attr_name}' has no metadata."
        assert isinstance(
            field.metadata[0], Selectable
        ), f"Field '{attr_name}' metadata is not of type {Selectable.__name__}."
        return field.metadata[0]

    def build_selectable_fields(self, attr_name: str = "select") -> list[Any] | None:
        if not hasattr(self, attr_name) or not getattr(self, attr_name):
            return None
        field_metadata: Selectable = self.__get_selectable_metadata(attr_name)
        select: str | list[str] = getattr(self, attr_name)
        if select == "all":
            return list(field_metadata.model_attrs.values())
        fields: list[Any] = []
        for field in select:
            if field_attr := field_metadata.get_attr(field):
                fields.append(field_attr)
        return fields if fields else None
