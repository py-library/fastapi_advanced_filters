# fastapi-filter documentation

A flexible, type-safe filtering system for SQLAlchemy models, designed for FastAPI and Pydantic v2.

- Type-safe filter definitions
- Customizable operations
- Easy integration with FastAPI

Start here:

- [`installation.md`](installation.md)
- [`reference.md`](reference.md)
- [`examples.md`](examples.md)
- [`extending.md`](extending.md)
- [`types.md`](types.md)

Back to project overview: [../README.md](../README.md)

## Quick Example

```python
from fastapi_filters import BaseFilter, FieldCriteria, OperationEnum

class UserFilter(BaseFilter):
    class FilterConfig:
        fields = [
            FieldCriteria(
                name="first_name",
                field_type=str,
                model_attr=User.first_name,
                op=(OperationEnum.EQ, OperationEnum.ILIKE),
            )
        ]
```
