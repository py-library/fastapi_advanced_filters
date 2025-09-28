from dataclasses import dataclass
from typing import Any

from annotated_types import BaseMetadata

from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum


@dataclass(frozen=True)
class AdvancedQSearch(BaseMetadata):
    model_attrs_with_op: dict[OperationEnum, list[Any]]
    logical_op: LogicalOperator = LogicalOperator.OR
