from typing import Callable, Optional

from fastapi_advanced_filters.enums import OrderEnum


def to_camel_case(snake_str: str) -> str:
    if not snake_str:
        return ""
    components = snake_str.split("_")
    first = components[0].lower() if not components[0].isupper() else components[0]
    return first + "".join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    if not camel_str:
        return ""
    snake_str = ""
    prev_char_is_upper = False
    for i, char in enumerate(camel_str):
        if char.isupper():
            if snake_str and not prev_char_is_upper and i > 0:
                snake_str += "_"
            snake_str += char.lower()
            prev_char_is_upper = True
        else:
            snake_str += char
            prev_char_is_upper = False
    return snake_str


def extract_sorting(sort_field: str) -> tuple[str, OrderEnum]:
    sort_field_with_order_dir: str = sort_field.strip()
    if sort_field_with_order_dir.startswith("-"):
        return sort_field_with_order_dir[1:], OrderEnum.DESC
    return sort_field_with_order_dir, OrderEnum.ASC


def validate_sortable_schema(
    allowed_sortable_attr: list[str],
) -> Callable[[Optional[str]], list[tuple[str, OrderEnum]]]:
    def validate_schema(
        provided_sortable_attr: Optional[str],
    ) -> list[tuple[str, OrderEnum]]:
        if provided_sortable_attr is None:
            return []
        formatted_sortable_data: list[tuple[str, OrderEnum]] = []
        for sort_field_with_order_dir in provided_sortable_attr.strip().split(","):
            if not sort_field_with_order_dir:
                raise ValueError("Invalid sorting format")
            sort_field, op = extract_sorting(sort_field_with_order_dir)
            if sort_field not in allowed_sortable_attr:
                raise ValueError(f"Field '{sort_field}' is not sortable")
            formatted_sortable_data.append((sort_field, op))
        return formatted_sortable_data

    return validate_schema


def validate_selectable_schema(
    allowed_selectable_attr: list[str],
) -> Callable[[str], list[str]]:
    def validate_schema(provided_selecteble_attr: str) -> list[str]:
        if provided_selecteble_attr == "all":
            return allowed_selectable_attr
        formatted_selectable_data: list[str] = []
        for selected_field in provided_selecteble_attr.split(","):
            if not selected_field:
                raise ValueError(
                    "select must be 'all', a list of strings, or a "
                    "comma-separated string"
                )
            if selected_field not in allowed_selectable_attr:
                raise ValueError(f"Field '{selected_field}' is not selectable")
            formatted_selectable_data.append(selected_field)
        return formatted_selectable_data

    return validate_schema
