from typing import Annotated, Any, Dict, Optional

from pydantic import Field, PlainValidator

from fastapi_filters.src.data_classes import SortBy
from fastapi_filters.src.utils import validate_sortable_schema


def generate_annotations_for_sortable_fields(
    filter_config_cls: SortBy | type,
) -> Optional[Dict[str, Any]]:
    if (
        hasattr(filter_config_cls, "sort_by")
        and isinstance(filter_config_cls.sort_by, SortBy)
        and (sort_by := filter_config_cls.sort_by)
    ):
        return {
            "sorting": Annotated[
                str | None,
                Field(
                    default=None,
                    alias="sort_by",
                    title=(
                        "Order by specific fields ("
                        f"{', '.join(sort_by.get_names())})"
                    ),
                    description=(
                        "Comma separated fields to order by. Prefix with '-' for"
                        " descending order."
                    ),
                ),
                sort_by,
                PlainValidator(validate_sortable_schema(sort_by.get_names())),
            ]
        }
    return None
