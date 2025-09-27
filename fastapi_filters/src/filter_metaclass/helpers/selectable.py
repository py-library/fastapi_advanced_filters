from typing import Annotated, Any, Dict, Optional

from pydantic import AfterValidator, Field

from fastapi_filters.src.data_classes import Selectable
from fastapi_filters.src.utils import validate_selectable_schema


def generate_annotations_for_selectable_fields(
    filter_config_cls: type | Selectable,
) -> Optional[Dict[str, Any]]:
    if (
        hasattr(filter_config_cls, "select_only")
        and isinstance(filter_config_cls.select_only, Selectable)
        and (selectable := filter_config_cls.select_only)
    ):
        return {
            "select": Annotated[
                str,
                Field(
                    default="all",
                    alias="select",
                    title=(
                        "Select specific fields ("
                        f"{', '.join(selectable.get_names())} or 'all')"
                    ),
                    description=(
                        "Comma separated fields to include in the response or 'all'"
                        " to include all fields."
                    ),
                ),
                selectable,
                AfterValidator(validate_selectable_schema(selectable.get_names())),
            ]
        }
    return None
