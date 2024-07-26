#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from tests.utils import is_prod_version


@pytest.mark.min_sf_ver("99.99.99")
def test_should_never_run_in_prod(snowflake_version):
    # This might still run in dev (where the version contains non-numerals,
    # so check if it has non-numerals). If it does not, then this should never
    # run.
    if is_prod_version(snowflake_version):
        pytest.fail("This test should not have run in a production version.")


@pytest.mark.min_sf_ver("1.0.0")
def test_should_always_run():
    pass
