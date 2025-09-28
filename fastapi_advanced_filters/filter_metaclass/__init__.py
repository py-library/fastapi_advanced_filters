"""

Filter metaclass for creating filter configurations dynamically.
This module provides a metaclass that processes a nested `FilterConfig`
class within a Pydantic model to generate filter fields with
appropriate types, aliases, and metadata for filtering operations.
It supports features like field operations, sorting, selection,
full-text search, and pagination.

"""
from fastapi_advanced_filters.filter_metaclass.metaclass import FilterMetaClass
