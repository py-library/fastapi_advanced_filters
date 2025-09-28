from dataclasses import dataclass, field
from typing import Any, Callable

from annotated_types import BaseMetadata

from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum
from fastapi_advanced_filters.utils import to_camel_case


@dataclass(frozen=True)
class FieldCriteria(BaseMetadata):
    name: str
    field_type: type
    op: tuple[OperationEnum, ...]
    model_attr: Any = None
    model_attrs_with_logical_op: tuple[list[Any], LogicalOperator] | None = None
    required_op: tuple[OperationEnum, ...] | None = None
    prefix: str | None = None
    custom_filter_per_op: Callable | None = None
    alias_as_camelcase: bool = False
    snake_case_separator_between_prefix_and_op: str = "__"
    fields_kwargs: dict[str, Any] = field(default_factory=dict)

    def get_name(self) -> str:
        if self.prefix is None:
            return self.name
        return (
            f"{self.prefix}{self.snake_case_separator_between_prefix_and_op}{self.name}"
        )

    def get_field_name(self, op: OperationEnum) -> str:
        if self.prefix is None:
            return (
                f"{self.name}"
                f"{self.snake_case_separator_between_prefix_and_op}"
                f"{op}"
            )
        return (
            f"{self.prefix}"
            f"{self.snake_case_separator_between_prefix_and_op}"
            f"{self.name}"
            f"{self.snake_case_separator_between_prefix_and_op}"
            f"{op}"
        )

    def get_alias_name(self, op: OperationEnum) -> str:
        if self.alias_as_camelcase:
            return to_camel_case(self.get_field_name(op))
        return self.get_field_name(op)
