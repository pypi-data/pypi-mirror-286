#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from io import BytesIO
from textwrap import dedent
from time import sleep

import pytest

from snowflake.core.exceptions import APIError
from snowflake.core.service import Service, ServiceSpecStageFile
from tests.utils import random_string


pytestmark = pytest.mark.jenkins

def test_fetch(services, temp_service, database, shared_compute_pool):
    service = services[temp_service.name].fetch()
    assert service.name == temp_service.name.upper()
    assert service.compute_pool == shared_compute_pool.upper()
    assert service.auto_resume
    assert service.comment == "created by temp_service"
    assert service.database_name == database.name

@pytest.mark.skip("Temporarily disable for flaky test")
def test_fetch_service_logs(services, temp_service, running_on_dev_vm):
    success = False
    for _ in range(5):
        try:
            if not running_on_dev_vm:
                message = "This message shows that your installation appears to be working " "correctly"
            else:
                message = "test 999"

            assert message in services[
                temp_service.name
            ].get_service_logs(0, "hello-world")

            # Wish there were a better way to test this with more
            # values for num_lines, but it involves reconfiguring the CI test
            # image. Now we just assert on empty response if log lines is set to 0.
            # TODO(SNOW-1371992) - Please uncomment this once you have this bug resolved
            # assert not (services[temp_service.name].get_service_logs(0, "hello-world", num_lines=0).strip())
            success = True
            break
        except APIError as e:
            if ("container: hello-world") not in str(e):
                raise
            sleep(1)
        except AssertionError:
            status = (services[temp_service.name]\
                .get_service_status(1)[0]['status']
            )
            print(f'Failed to get message of service, status: {status}')
            sleep(5)
    assert success is True


def test_fetch_service_status(services, session, imagerepo, shared_compute_pool):
    service_name = random_string(5, "test_service_")
    stage_name = random_string(5, "test_stage_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    stage_file = f"@{stage_name}"
    spec = f"{stage_file}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(f"""
                spec:
                  containers:
                  - name: hello-world
                    image: {imagerepo}/hello-world:latest
                """).encode()
        ),
        spec,
    )
    test_service = Service(
        name=service_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )

    s = services.create(test_service)

    try:
        status = s.get_service_status()
        assert status[0]["status"] in ["UNKNOWN", "PENDING", "READY", "DONE"]
        status = s.get_service_status(timeout=3)
        assert status[0]["status"] in ["UNKNOWN", "PENDING", "READY", "DONE"]
        s.suspend()
        status = s.get_service_status()
        assert status[0]["status"] in ["SUSPENDED", "UNKNOWN", "PENDING", "READY", "DONE"]
        status = s.get_service_status(timeout=3)
        assert status[0]["status"] in ["SUSPENDED"]
    finally:
        s.drop()
