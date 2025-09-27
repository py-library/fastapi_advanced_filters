from typing import Any, Callable

from pydantic import BaseModel, ConfigDict

from fastapi_filters.src.data_classes import FilterResult
from fastapi_filters.src.enums import LogicalOperator, OperationEnum, OrderEnum
from fastapi_filters.src.filter_metaclass import FilterMetaClass
from fastapi_filters.src.filters.mixins import (
    FilterMixin,
    PaginationMixin,
    QSearchMixin,
    SelectMixin,
    SortingMixin,
)
from fastapi_filters.src.operation_mapping import (
    SQLALCHEMY_LOGICAL_OP_MAPPING as LOGICAL_OP_MAPPING,
)
from fastapi_filters.src.operation_mapping import SQLALCHEMY_OP_MAPPING as OP_MAPPING
from fastapi_filters.src.operation_mapping import (
    SQLALCHEMY_SORTING_MAPPING as SORTING_MAPPING,
)


class BaseFilter(
    BaseModel,
    FilterMixin,
    SortingMixin,
    SelectMixin,
    QSearchMixin,
    PaginationMixin,
    metaclass=FilterMetaClass,
):
    # Explicit types to satisfy mypy against the mixins' expectations
    __op_mapping__: dict[OperationEnum, Callable[..., Any]] = OP_MAPPING
    __sorting_mapping__: dict[OrderEnum, Callable[[Any], Any]] = SORTING_MAPPING
    __logical_op_mapping__: dict[
        LogicalOperator, Callable[..., Any]
    ] = LOGICAL_OP_MAPPING

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=False,
    )

    def get_filter_model(self) -> FilterResult:
        return FilterResult(
            filters=self.build_filters(),
            sorting=self.build_sorting(),
            pagination=self.build_pagination(),
            selected_columns=self.build_selectable_fields(),
            q_search=self.build_q_search(),
        )
