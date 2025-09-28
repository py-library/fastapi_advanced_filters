from typing import Annotated, Any, Dict, Optional

from pydantic.fields import Field

from fastapi_advanced_filters.data_classes import AdvancedQSearch, QSearch


def generate_annotations_for_qsearch(
    filter_config_cls: type,
) -> Optional[Dict[str, Any]]:
    if hasattr(filter_config_cls, "q_search") and isinstance(
        filter_config_cls.q_search, (QSearch, AdvancedQSearch)
    ):
        q_search: QSearch | AdvancedQSearch = filter_config_cls.q_search
        return {
            "q_search": Annotated[
                str | None,
                Field(
                    default=None,
                    title="Search by query string",
                ),
                q_search,
            ]
        }
    return None
