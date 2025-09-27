def _sql(expr) -> str:
    """Compile a SQLAlchemy expression to a SQL string with literal binds.

    This makes assertions stable across dialects by inlining parameters.
    """
    return str(expr.compile(compile_kwargs={"literal_binds": True}))


def assert_sql_equal(actual, expected):
    assert _sql(actual) == _sql(expected)


def assert_sql_list_equal(actual_list, expected_list):
    assert len(actual_list) == len(expected_list)
    for a, e in zip(actual_list, expected_list):
        assert_sql_equal(a, e)
