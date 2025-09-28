from fastapi_advanced_filters.data_classes import FieldCriteria
from fastapi_advanced_filters.enums import OperationEnum, PaginationEnum
from fastapi_advanced_filters.filter_metaclass.helpers import (
    generate_annotations_for_pagination,
    generate_annotations_for_qsearch,
    generate_annotations_for_selectable_fields,
    generate_annotations_for_sortable_fields,
)
from fastapi_advanced_filters.filter_metaclass.metaclass import FilterMetaClass


def test_helpers_return_none_when_not_configured():
    class Dummy:
        pass

    assert generate_annotations_for_qsearch(Dummy) is None
    assert generate_annotations_for_selectable_fields(Dummy) is None
    assert generate_annotations_for_sortable_fields(Dummy) is None
    assert generate_annotations_for_pagination(Dummy) is None


def test_pagination_annotations_offset_and_page_based():
    class C1:
        pagination = PaginationEnum.OFFSET_BASED

    class C2:
        pagination = PaginationEnum.PAGE_BASED

    off = generate_annotations_for_pagination(C1)
    page = generate_annotations_for_pagination(C2)
    assert set(off.keys()) == {"limit", "offset"}
    assert set(page.keys()) == {"page", "page_size"}


def test_fields_list_of_fieldcriteria_is_used():
    fc = FieldCriteria(name="age", field_type=int, op=(OperationEnum.GT,))

    class C:
        fields = [fc]

    annotations = FilterMetaClass.generate_annotations_for_filters(C)
    # The annotation name is generated as age__gt
    assert "age__gt" in annotations
