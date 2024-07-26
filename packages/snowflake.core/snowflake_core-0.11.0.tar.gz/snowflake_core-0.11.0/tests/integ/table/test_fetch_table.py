import pytest

from tests.integ.table.conftest import assert_table


pytestmark = pytest.mark.jenkins


def test_fetch(tables, table_handle, database, schema):
    table_deep = table_handle.fetch()
    assert_table(table_deep, table_handle.name, database, schema, True)
