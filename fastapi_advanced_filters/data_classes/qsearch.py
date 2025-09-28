from dataclasses import dataclass
from typing import Any

from annotated_types import BaseMetadata

from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum


@dataclass(frozen=True)
class QSearch(BaseMetadata):
    model_attrs: list[Any]
    logical_op: LogicalOperator = LogicalOperator.OR
    op: OperationEnum = OperationEnum.ILIKE
