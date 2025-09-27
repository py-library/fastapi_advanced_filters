# Extending the Library

## Add New Types

To support a new Python type (e.g., `datetime`):

1. Use `FieldCriteria(field_type=...)` with your type and map `model_attr` to a SQLAlchemy column of that type.
2. Ensure your SQLAlchemy column’s `type.python_type` behaves as expected for operations like `IN`, `BTW`, etc.
3. Add new operations to `OperationEnum` only if you need new behavior.

## Add New Operations

1. Extend `OperationEnum` (see `fastapi_filters/src/enums.py`):
    ```python
    class OperationEnum(str, Enum):
        # ...existing...
        MYOP = "myop"
    ```
2. Update `fastapi_filters/src/operation_mapping/sqlalchemy_mapping.py` to map the new operation to SQLAlchemy logic.

## Custom Methods

- Prefer `custom_filter_per_op` in `FieldCriteria` for per-operation customization.
- You can also subclass and add helper methods if needed.

## Example: Custom Filter Logic

```python
def custom_filter(op, value):
    if op == OperationEnum.EQ:
        return User.first_name.ilike(value)
    # Add more logic as needed

class CustomUserFilter(BaseFilter):
    class FilterConfig:
        fields = [
            FieldCriteria(
                name="first_name",
                field_type=str,
                op=(OperationEnum.EQ,),
                model_attr=User.first_name,
                custom_filter_per_op=custom_filter,
            )
        ]
```
