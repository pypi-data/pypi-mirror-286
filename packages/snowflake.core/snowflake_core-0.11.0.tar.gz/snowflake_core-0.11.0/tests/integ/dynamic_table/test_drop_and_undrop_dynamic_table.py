import pytest as pytest

from snowflake.core.exceptions import NotFoundError


pytestmark = pytest.mark.jenkins


def test_drop_and_undrop(dynamic_table_handle):
    dynamic_table_handle.drop()
    with pytest.raises(NotFoundError):
        dynamic_table_handle.fetch()
    dynamic_table_handle.undrop()
    dynamic_table_handle.fetch()
