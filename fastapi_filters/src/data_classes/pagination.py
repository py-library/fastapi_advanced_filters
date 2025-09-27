from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    limit: int | None = None
    offset: int | None = None
