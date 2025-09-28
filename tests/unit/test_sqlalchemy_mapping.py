import pytest
from sqlalchemy import Boolean, Column, Date, Integer, String

from fastapi_advanced_filters.enums import LogicalOperator, OperationEnum, OrderEnum
from fastapi_advanced_filters.operation_mapping.sqlalchemy_mapping import (
    LOGICAL_OP_MAPPING,
    OP_MAPPING,
    SORTING_MAPPING,
    between,
    contains,
    in_funct,
    not_in_funct,
)


def _sql(expr) -> str:
    return str(expr.compile(compile_kwargs={"literal_binds": True}))


def test_in_funct_and_not_in_boolean_and_int():
    col_bool = Column("b", Boolean())
    res_in = in_funct(col_bool, "true,false,0,1")
    s = _sql(res_in).lower()
    assert " in (" in s and ("1" in s or "true" in s) and ("0" in s or "false" in s)

    res_not_in = not_in_funct(col_bool, "true,0")
    s2 = _sql(res_not_in).lower()
    assert "not in" in s2 or ("not" in s2 and " in " in s2)

    col_int = Column("i", Integer())
    res_int = in_funct(col_int, "1,2,3")
    s3 = _sql(res_int)
    assert "1" in s3 and "2" in s3 and "3" in s3


def test_contains_string_and_scalar_list_paths():
    col_str = Column("s", String())
    res = contains(col_str, "a,b")
    s = _sql(res)
    # SQLite renders LIKE as concatenation with '%' || 'a' || '%', so keep this
    # dialect-agnostic
    assert "LIKE" in s and "a" in s and "b" in s

    col_int = Column("i", Integer())
    res2 = contains(col_int, "1,2")
    s2 = _sql(res2)
    # SQLite may quote numeric literals in compiled SQL; accept either form
    assert "=" in s2 and "1" in s2 and "2" in s2


def test_contains_array_path_branch():
    try:
        from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
    except Exception:
        PG_ARRAY = None
    if PG_ARRAY is None:  # pragma: no cover - platform without PG dialect
        return
    col_arr = Column("a", PG_ARRAY(String()))
    # don't compile; just ensure we can build the expression and branch executes
    expr = contains(col_arr, "x,y")
    assert expr is not None


def test_between_for_numeric_and_date():
    col_int = Column("i", Integer())
    res_num = between(col_int, "10,1,5")
    s = _sql(res_num)
    assert " BETWEEN 1 AND 10" in s or " BETWEEN 10 AND 1" in s

    col_date = Column("d", Date())
    res_date = between(col_date, "2020-01-01,2020-01-10")
    s2 = _sql(res_date)
    assert "2020-01-01" in s2 and "2020-01-10" in s2


def test_between_invalid_type_raises():
    from fastapi_advanced_filters.operation_mapping import sqlalchemy_mapping as sm

    col_str = Column("s", String())
    with pytest.raises(ValueError):
        sm.between(col_str, "a,b")


def test_op_mappings_like_and_order_and_logical():
    col = Column("s", String())
    assert "LIKE" in _sql(OP_MAPPING[OperationEnum.LIKE](col, "x"))
    assert "LIKE" in _sql(OP_MAPPING[OperationEnum.ILIKE](col, "x")).upper()

    # Sorting mapping on actual columns
    asc_expr = SORTING_MAPPING[OrderEnum.ASC](col)
    desc_expr = SORTING_MAPPING[OrderEnum.DESC](col)
    assert _sql(asc_expr).endswith("ASC")
    assert _sql(desc_expr).endswith("DESC")

    # logical operator mapping should be callable and produce a SQL expression
    col_i = Column("i", Integer())
    or_expr = LOGICAL_OP_MAPPING[LogicalOperator.OR](col_i == 1, col_i == 2)
    assert " OR " in _sql(or_expr)


def test_is_and_isnull_op_mapping():
    col = Column("b", Boolean())
    assert " IS NULL" in _sql(OP_MAPPING[OperationEnum.IS](col, None)).upper()
    assert " IS NULL" in _sql(OP_MAPPING[OperationEnum.ISNULL](col, True)).upper()
    assert " IS NOT NULL" in _sql(OP_MAPPING[OperationEnum.ISNULL](col, False)).upper()


def test_contains_array_branch_with_monkeypatch():
    # Force ARRAY isinstance check to be true and ensure any() is called
    from fastapi_advanced_filters.operation_mapping import sqlalchemy_mapping as sm

    class ArrayMarker:  # dummy marker class
        pass

    class DummyArrayField:
        def __init__(self):
            self.type = ArrayMarker()

        def any(self, values):
            return ("ANY", tuple(values))

    original = sm.ARRAY
    try:
        sm.ARRAY = ArrayMarker
        expr = sm.contains(DummyArrayField(), "x,y,,z")
        assert expr == ("ANY", ("x", "y", "z"))
    finally:
        sm.ARRAY = original


def test_in_funct_value_error_returns_none():
    # For integer column, passing non-integers will raise ValueError
    # internally -> returns None
    col = Column("i", Integer())
    assert in_funct(col, "a,b") is None


def test_not_in_funct_value_error_returns_none():
    # For integer column, passing non-integers should also trigger ValueError
    # -> returns None
    col = Column("i", Integer())
    assert not_in_funct(col, "a,b") is None
