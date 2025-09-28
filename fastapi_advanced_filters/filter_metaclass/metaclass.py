from typing import Any

from pydantic import BaseModel

from fastapi_advanced_filters.enums import OperationEnum
from fastapi_advanced_filters.filter_metaclass.helpers import (
    attrs_to_field_criteria,
    from_field_criteria_to_attr,
    generate_annotations_for_pagination,
    generate_annotations_for_qsearch,
    generate_annotations_for_selectable_fields,
    generate_annotations_for_sortable_fields,
)


class FilterMetaClass(type(BaseModel)):  # type: ignore
    """Metaclass to dynamically create filter fields from configuration.

    This processes a nested `FilterConfig` inside a Pydantic model and generates
    filter fields with appropriate types, aliases, and metadata for filtering
    operations.
    """

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        **kwargs: dict[str, Any],
    ) -> type:
        if attrs and "FilterConfig" in attrs:
            annotations: dict[str, Any] | None = attrs.get("__annotations__", None)
            if annotations is None:
                attrs["__annotations__"] = mcs.generate_annotations_for_filters(
                    attrs["FilterConfig"]
                )
            else:
                attrs["__annotations__"].update(
                    mcs.generate_annotations_for_filters(attrs["FilterConfig"])
                )
        return super().__new__(mcs, name, bases, attrs, **kwargs)

    def generate_annotations_for_filters(  # noqa: C901
        filter_config_cls: type,
    ) -> dict[str, Any]:
        annotations: dict[str, Any] = {}
        if hasattr(filter_config_cls, "fields"):
            fields = filter_config_cls.fields
            if hasattr(filter_config_cls, "model"):
                fields = attrs_to_field_criteria(
                    model_cls=filter_config_cls.model,
                    fields=filter_config_cls.fields,
                    prefix=getattr(filter_config_cls, "prefix", None),
                    op=getattr(filter_config_cls, "default_op", (OperationEnum.EQ,)),
                )

            for field in fields:
                annotations.update(from_field_criteria_to_attr(field))
        if q_search_annotation := generate_annotations_for_qsearch(filter_config_cls):
            annotations.update(q_search_annotation)
        if selectable_annotation := generate_annotations_for_selectable_fields(
            filter_config_cls
        ):
            annotations.update(selectable_annotation)
        if sortable_annotation := generate_annotations_for_sortable_fields(
            filter_config_cls
        ):
            annotations.update(sortable_annotation)
        if pagination_annotations := generate_annotations_for_pagination(
            filter_config_cls
        ):
            annotations.update(pagination_annotations)
        return annotations
