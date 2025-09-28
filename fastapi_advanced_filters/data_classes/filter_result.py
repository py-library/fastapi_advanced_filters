from dataclasses import dataclass
from typing import Any

from .pagination import Pagination


@dataclass(frozen=True)
class FilterResult:
    selected_columns: list[Any] | None = None
    sorting: list[Any] | None = None
    filters: list[Any] | None = None
    pagination: Pagination | None = None
    q_search: Any | None = None
