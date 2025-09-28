from typing import Annotated, Any, Dict, Optional

from pydantic.fields import Field

from fastapi_advanced_filters.enums import PaginationEnum


def generate_annotations_for_pagination(
    filter_config_cls: type,
) -> Optional[Dict[str, Any]]:
    if (
        not hasattr(filter_config_cls, "pagination")
        or not filter_config_cls.pagination
        or not isinstance(filter_config_cls.pagination, PaginationEnum)
    ):
        return None
    if filter_config_cls.pagination == PaginationEnum.OFFSET_BASED:
        return {
            "limit": Annotated[
                int,
                Field(
                    default=100,
                    alias="limit",
                    title="Limit the number of results",
                    description="Limit the number of results returned. Default is 100.",
                    ge=1,
                    le=1000,
                ),
            ],
            "offset": Annotated[
                int,
                Field(
                    default=0,
                    alias="offset",
                    title="Offset the results",
                    description="Offset the results by a certain number. Default is 0.",
                    ge=0,
                ),
            ],
        }
    return {
        "page": Annotated[
            int,
            Field(
                default=1,
                alias="page",
                title="Page number",
                description="Page number for pagination. Default is 1.",
                ge=1,
            ),
        ],
        "page_size": Annotated[
            int,
            Field(
                default=100,
                alias="size",
                title="Number of items per page",
                description="Number of items per page for pagination. Default is 100.",
                ge=1,
                le=1000,
            ),
        ],
    }
