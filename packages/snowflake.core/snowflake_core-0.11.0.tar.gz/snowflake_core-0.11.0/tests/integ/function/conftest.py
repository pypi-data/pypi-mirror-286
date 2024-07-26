from io import BytesIO
from pathlib import Path
from textwrap import dedent

import pytest

from pydantic import StrictStr

from snowflake.core.service import (
    Service,
    ServiceSpecStageFile,
)

from ..utils import random_string


@pytest.fixture(scope="session")
def echo_service_name(session):
    stage_name = random_string(5, "testfunc_stage_")
    session.sql(f"create or replace stage {stage_name};").collect()

    session.sql(
        """
        alter session set
        qa_mode = true,
        qa_mode_mock_external_function_remote_calls = true;
        """
    ).collect()
    session.sql("""
                alter session set snowservices_mock_server_endpoints =
                  '{"ep1":["mockhost1", "mockhost2"],"end-point-2":["mockhost3"]}';
                """).collect()

    print(
        session.sql(f"""put file://{Path(__file__).resolve().parent.parent.parent
                      / "resources"
                      / "fake_spec_single_container.yaml"
                } @{stage_name} auto_compress=false;
            """).collect()
    )

    service_name = random_string(5, "testfunc_service_")
    session.sql(f"""
            create service {service_name}
            in compute pool mypool
            from @{stage_name}
            spec='/fake_spec_single_container.yaml';
            """).collect()

    return service_name


@pytest.fixture(scope="session")
def temp_service_for_function(services, session, imagerepo, shared_compute_pool) -> StrictStr:
    stage_name = random_string(5, "test_stage_ff_")
    s_name = random_string(5, "test_service_ff_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    spec = f"@{stage_name}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(
                f"""
                spec:
                    containers:
                        - name: hello-world
                          image: {imagerepo}/hello-world:latest
                    endpoints:
                        - name: ep1
                          port: 8000
                        - name: end-point-2
                          port: 8010
                 """
            ).encode()
        ),
        spec,
    )

    test_s = Service(
        name=s_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service for function",
    )
    s = services.create(test_s)
    try:
        yield s
    finally:
        s.delete()
