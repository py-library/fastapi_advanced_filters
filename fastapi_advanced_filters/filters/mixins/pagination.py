from fastapi_advanced_filters.data_classes import Pagination


class PaginationMixin:
    def build_pagination(self) -> Pagination | None:
        if hasattr(self, "limit") and hasattr(self, "offset"):
            return Pagination(limit=self.limit, offset=self.offset)
        if hasattr(self, "page") and hasattr(self, "page_size"):
            return Pagination(
                limit=self.page_size, offset=(self.page - 1) * self.page_size
            )
        return None
