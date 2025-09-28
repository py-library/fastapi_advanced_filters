from enum import StrEnum


class PaginationEnum(StrEnum):
    PAGE_BASED = "page_based"
    OFFSET_BASED = "offset_based"


class LogicalOperator(StrEnum):
    AND = "AND"
    OR = "OR"


class OperationEnum(StrEnum):
    ILIKE = "ilike"
    LIKE = "like"
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOTIN = "notin"
    ISNULL = "isnull"
    BTW = "btw"
    CONT = "cont"
    IS = "is"


class OrderEnum(StrEnum):
    ASC = "asc"
    DESC = "desc"
