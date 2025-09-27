from dataclasses import dataclass, field
from typing import Any

from annotated_types import BaseMetadata

from fastapi_filters.src.utils import to_camel_case


@dataclass(frozen=True)
class SortBy(BaseMetadata):
    model_attrs: dict[str, Any]
    __camelcase_alias_cache: dict[str, Any] = field(default_factory=dict, init=False)
    alias_as_camelcase: bool = False

    def __post_init__(self):
        if self.model_attrs and self.alias_as_camelcase:
            object.__setattr__(
                self,
                "_SortBy__camelcase_alias_cache",
                {to_camel_case(name): attr for name, attr in self.model_attrs.items()},
            )

    def get_names(self) -> list[str]:
        if self.alias_as_camelcase:
            return list(self.__camelcase_alias_cache.keys())
        return list(self.model_attrs.keys())

    def get_attr(self, sort_attr: str) -> Any:
        if self.alias_as_camelcase:
            return self.__camelcase_alias_cache.get(sort_attr)
        return self.model_attrs.get(sort_attr)
