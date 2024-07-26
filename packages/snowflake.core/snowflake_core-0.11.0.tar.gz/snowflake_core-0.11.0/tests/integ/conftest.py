# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import os
import typing
import uuid

from contextlib import contextmanager
from io import BytesIO
from textwrap import dedent
from typing import Dict, Generator, Iterator, List, NamedTuple

import pytest

from pydantic import StrictStr

import snowflake.connector

from snowflake.connector import SnowflakeConnection
from snowflake.core import Root
from snowflake.core.compute_pool import (
    ComputePool,
    ComputePoolCollection,
)
from snowflake.core.cortex.search_service import CortexSearchServiceCollection
from snowflake.core.database import (
    Database,
    DatabaseCollection,
    DatabaseResource,
)
from snowflake.core.function import FunctionCollection
from snowflake.core.grant._grants import Grants
from snowflake.core.image_repository import (
    ImageRepository,
    ImageRepositoryCollection,
)
from snowflake.core.role import RoleCollection
from snowflake.core.schema import (
    Schema,
    SchemaCollection,
    SchemaResource,
)
from snowflake.core.service import (
    Service,
    ServiceCollection,
    ServiceResource,
    ServiceSpecInlineText,
    ServiceSpecStageFile,
)
from snowflake.core.user import UserCollection
from snowflake.core.warehouse import WarehouseCollection
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

from ..utils import is_prod_version
from .utils import connection_config, connection_keys, random_string


RUNNING_ON_GHA = os.getenv("GITHUB_ACTIONS") == "true"
RUNNING_ON_JENKINS = "JENKINS_URL" in os.environ
RUNNING_IN_NOTEBOOK = "RUNNING_IN_NOTEBOOK" in os.environ
RUNNING_IN_STOREDPROC = "RUNNING_IN_STOREDPROC" in os.environ
JENKINS_RUN_ALL_TESTS = "SF_JENKINS_RUN_ALL_TESTS" in os.environ
TEST_SCHEMA = "GH_JOB_{}".format(str(uuid.uuid4()).replace("-", "_"))
if RUNNING_ON_GHA or RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
    # Backwards compatible mode until new test execution mode is able to run on public CI
    TEST_DATABASE = "TESTDB_PYTHON_AUTO"
    TEST_SCHEMA = "GH_JOB_{}".format(str(uuid.uuid4()).replace("-", "_"))
    TEST_COMPUTE_POOL = "ci_compute_pool"
    TEST_INSTANCE_FAMILY = "CPU_X64_XS"
    TEST_IMAGE_REPO = "test_image_repo_auto"
    TEST_IR_URL = (
        "sfengineering-ss-lprpr-test2.registry.snowflakecomputing.com/"
        + "testdb_python_auto/testschema_auto/test_image_repo_auto"
    )
elif RUNNING_ON_JENKINS:
    TEST_DATABASE = "TESTDB_PYTHON_API"
    TEST_SCHEMA = "TESTSCHEMA_PYTHON_API"
    TEST_COMPUTE_POOL = "TESTCP_PYTHON_API"
    TEST_INSTANCE_FAMILY = "CPU_X64_XS"
    TEST_IMAGE_REPO = "TESTIR_PYTHON_API"
    TEST_IR_URL = (
        "sfengineering-ss-lprpr-test2.registry.snowflakecomputing.com/"
        + "testdb_python_auto/testschema_auto/test_image_repo_auto"
    )
else:
    # New test execution mode where setup is only run when necessary to
    #  seed necessary SQL objects
    TEST_DATABASE = "TESTDB_PYTHON_API"
    TEST_SCHEMA = "TESTSCHEMA_PYTHON_API"
    TEST_COMPUTE_POOL = "TESTCP_PYTHON_API"
    TEST_INSTANCE_FAMILY = "FAKE"
    TEST_IMAGE_REPO = "TESTIR_PYTHON_API"
    TEST_IR_URL = None


@pytest.fixture(scope="session")
def running_on_public_ci() -> bool:
    return RUNNING_ON_GHA


@pytest.fixture(scope="session")
def running_on_private_ci():
    return RUNNING_ON_JENKINS


@pytest.fixture(scope="session")
def running_on_dev_vm():
    return not RUNNING_ON_GHA and not RUNNING_ON_JENKINS


@pytest.fixture(scope="session")
def instance_family() -> str:
    return TEST_INSTANCE_FAMILY


@pytest.fixture(scope="session")
def shared_compute_pool(spcs_setup):
    yield spcs_setup


def print_help() -> None:
    print(
        """Connection parameter must be specified in parameters.py,
    for example:
CONNECTION_PARAMETERS = {
    'account': 'testaccount',
    'user': 'user1',
    'password': 'test',
    'database': 'testdb',
    'schema': 'public',
}
"""
    )


def pytest_runtest_setup(item):
    # Skip online tests when not running on GHA or Jenkins
    # TODO: make the naming of this marker consistent with the other skip_xzy markers
    envnames = [mark.args[0] for mark in item.iter_markers(name="env")]
    if envnames:
        if "online" in envnames:
            if not RUNNING_ON_GHA and not RUNNING_ON_JENKINS:
                pytest.skip("this test is skipped when running locally")
        if "local" in envnames:
            if RUNNING_ON_GHA or RUNNING_ON_JENKINS or RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
                pytest.skip("this test is only enabled in the local environment")
    # Skip any test not marked for Jenkins when running on Jenkins
    if RUNNING_ON_JENKINS and not JENKINS_RUN_ALL_TESTS:
        jenkins_marker = list(item.iter_markers(name="jenkins"))
        if not jenkins_marker:
            pytest.skip("this test is not supposed to run on Jenkins")
    # Skip any test marked for Notebook when running on Notebook Environment
    if RUNNING_IN_NOTEBOOK:
        notebook_marker = list(item.iter_markers(name="skip_notebook"))
        if notebook_marker:
            pytest.skip("this test is not supposed to run on Notebook Environment")
    # Skip any test marked for Storedproc when running on Storedproc Environment
    if RUNNING_IN_STOREDPROC:
        storedproc_marker = list(item.iter_markers(name="skip_storedproc"))
        if storedproc_marker:
            pytest.skip("this test is not supposed to run on Storedproc Environment")


@pytest.fixture(autouse=True)
def min_sf_ver(request, snowflake_version):
    if "min_sf_ver" in request.keywords and len(request.keywords["min_sf_ver"].args) > 0:
        requested_version = request.keywords["min_sf_ver"].args[0]

        if is_prod_version(snowflake_version):
            current_version = tuple(map(int, snowflake_version.split(".")))
            min_version = tuple(map(int, requested_version.split(".")))
            if current_version < min_version:
                pytest.skip(
                    f"Skipping test because the current server version {snowflake_version} "
                    f"is older than the minimum version {requested_version}"
                )


@pytest.fixture(scope="session")
def snowflake_version(session) -> str:
    return session.sql("select current_version()").collect()[0][0].strip()


@pytest.fixture(scope="session")
def db_parameters() -> Dict[str, str]:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        config = {}
        session = get_active_session()
        config["schema"] = TEST_SCHEMA
        config["database"] = TEST_DATABASE
        config["warehouse"] = session.get_current_warehouse()
        return config

    config = connection_config(TEST_SCHEMA, TEST_DATABASE)
    return config


# 2023-06-21(warsaw): WARNING!  If any of these fixtures fail, they will print
# db_parameters in the traceback, and that **will** leak the password.  pytest
# doesn't seem to have any way to suppress the password, and I've tried lots
# of things to get that to work, to no avail.


@pytest.fixture(scope="session")
def session_notebook() -> Session:
    return get_active_session()


@pytest.fixture(scope="session")
def session_default(connection_default) -> Session:
    return Session.builder.config("connection", connection_default).create()


@pytest.fixture(scope="session")
def session(request) -> Session:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        return request.getfixturevalue("session_notebook")
    else:
        return request.getfixturevalue("session_default")


@pytest.fixture(scope="session")
def connection_notebook(session_notebook) -> SnowflakeConnection:
    return session_notebook.connection


@pytest.fixture(scope="session")
def connection_default(db_parameters) -> SnowflakeConnection:
    _keys = connection_keys()
    with snowflake.connector.connect(
        # This works around SNOW-998521, by forcing JSON results
        **{k: db_parameters[k] for k in _keys if k in db_parameters}
    ) as con:
        yield con


@pytest.fixture(scope="session")
def connection(request) -> SnowflakeConnection:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        return request.getfixturevalue("connection_notebook")
    else:
        return request.getfixturevalue("connection_default")


@pytest.fixture(scope="session")
def root(connection, session) -> Root:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        return Root(session)
    return Root(connection)


@pytest.fixture(scope="session")
def database(root, db_parameters) -> DatabaseResource:
    return root.databases[db_parameters["database"]]


@pytest.fixture(scope="session")
def schema(schemas, db_parameters) -> SchemaResource:
    return schemas[db_parameters["schema"]]


@pytest.fixture(scope="module")
def image_repositories(schema) -> ImageRepositoryCollection:
    return schema.image_repositories


@pytest.fixture(scope="module")
def compute_pools(root) -> ComputePoolCollection:
    return root.compute_pools


@pytest.fixture(scope="module")
def warehouses(root) -> WarehouseCollection:
    return root.warehouses


@pytest.fixture(scope="session")
def services(schema) -> ServiceCollection:
    return schema.services


@pytest.fixture(scope="session")
def functions(schema) -> FunctionCollection:
    return schema.functions


@pytest.fixture(scope="session")
def databases(root) -> DatabaseCollection:
    return root.databases


@pytest.fixture(scope="session")
def schemas(database) -> SchemaCollection:
    return database.schemas


@pytest.fixture(scope="module")
def roles(root) -> RoleCollection:
    return root.roles


@pytest.fixture(scope="module")
def users(root) -> UserCollection:
    return root.users


@pytest.fixture(scope="module")
def grants(root) -> Grants:
    return root.grants


@pytest.fixture(scope="session")
def cortex_search_services(schema) -> CortexSearchServiceCollection:
    return schema.cortex_search_services


@pytest.fixture(scope="session", autouse=True)
def test_schema() -> str:
    """Set up and tear down the test schema. This is automatically called per test session."""
    return TEST_SCHEMA


@pytest.fixture
def temp_ir(image_repositories) -> Generator[ImageRepository, None, None]:
    ir_name = random_string(5, "test_ir_")
    test_ir = ImageRepository(
        name=ir_name,
        # TODO: comment is not supported by image repositories?
        # comment="created by temp_ir",
    )
    image_repositories.create(test_ir)
    yield test_ir
    image_repositories[test_ir.name].drop()


@pytest.fixture
def temp_cp(compute_pools) -> Generator[ComputePool, None, None]:
    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name, instance_family=TEST_INSTANCE_FAMILY, min_nodes=1, max_nodes=1, comment="created by temp_cp"
    )
    compute_pools.create(test_cp)
    yield test_cp
    compute_pools[test_cp.name].drop()


@pytest.fixture
def temp_service(root, services, session, imagerepo, shared_compute_pool) -> Iterator[ServiceResource]:
    stage_name = random_string(5, "test_stage_")
    s_name = random_string(5, "test_service_")
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
                  - name: default
                    port: 8080
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
        max_instances=5,
        comment="created by temp_service",
    )
    s = services.create(test_s)
    yield test_s
    s.drop()


@pytest.fixture
def temp_service_from_spec_inline(root, services, session, imagerepo, shared_compute_pool) -> Iterator[ServiceResource]:
    s_name = random_string(5, "test_service_")
    inline_spec = dedent(
        f"""
        spec:
          containers:
          - name: hello-world
            image: {imagerepo}/hello-world:latest
         """
    )
    test_s = Service(
        name=s_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecInlineText(spec_text=inline_spec),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service_from_spec_inline",
    )
    s = services.create(test_s)
    yield test_s
    s.drop()


@pytest.fixture
def backup_database_schema(connection):
    """Reset the current database and schema after a test is complete.

    These 2 resources go hand-in-hand, so they should be backed up together.
    This fixture should be used when a database, or schema is created,
    or used in a test.
    """
    with connection.cursor() as cursor:
        database_name = cursor.execute("SELECT /* backup_database_schema */ CURRENT_DATABASE()").fetchone()[0]
        schema_name = cursor.execute("SELECT /* backup_database_schema */ CURRENT_SCHEMA()").fetchone()[0]
        try:
            yield
        finally:
            if schema_name is not None:
                cursor.execute(f"USE SCHEMA /* backup_database_schema */ {database_name}.{schema_name}")
            elif database_name is not None:
                cursor.execute(f"USE DATABASE /* backup_database_schema */ {database_name}")


@pytest.fixture
def backup_warehouse(connection):
    """Reset the current warehouse after a test is complete.

    This fixture should be used when a warehouse is created, or used in a test.
    """
    with connection.cursor() as cursor:
        warehouse_name = cursor.execute("SELECT /* backup_warehouse */ CURRENT_WAREHOUSE()").fetchone()[0]
        try:
            yield
        finally:
            if warehouse_name is not None:
                cursor.execute(f"USE WAREHOUSE /* backup_warehouse */ {warehouse_name};")


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_db(databases: DatabaseCollection) -> Iterator[DatabaseResource]:
    # create temp database
    db_name = random_string(5, "test_database_")
    test_db = Database(name=db_name, comment="created by temp_db")
    db = databases.create(test_db)
    try:
        yield db
    finally:
        db.drop()


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_db_case_sensitive(databases: DatabaseCollection) -> Iterator[DatabaseResource]:
    # create temp database
    db_name = random_string(5, "test_database_case_sensitive_")
    db_name_case_sensitive = '"' + db_name + '"'
    test_db = Database(name=db_name_case_sensitive, comment="created by temp_case_sensitive_db")
    db = databases.create(test_db)
    try:
        yield db
    finally:
        db.drop()


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_schema(schemas) -> Iterator[SchemaResource]:
    schema_name = random_string(5, "test_schema_")
    test_schema = Schema(
        name=schema_name,
        comment="created by temp_schema",
    )
    sc = schemas.create(test_schema)
    try:
        yield sc
    finally:
        sc.drop()


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_schema_case_sensitive(schemas) -> Iterator[SchemaResource]:
    schema_name = random_string(5, "test_schema_case_sensitive_")
    schema_name_case_sensitive = '"' + schema_name + '"'
    test_schema = Schema(
        name=schema_name_case_sensitive,
        comment="created by temp_schema_case_sensitive",
    )
    sc = schemas.create(test_schema)
    try:
        yield sc
    finally:
        sc.drop()


class Tuple_database(NamedTuple):
    name: str
    param: str


class DatabaseDict(typing.TypedDict):
    params: str
    schemas: typing.Set[str]


objects_to_setup: typing.Dict[str, DatabaseDict] = {
    TEST_DATABASE: {
        "schemas": {
            TEST_SCHEMA,
        },
        "params": "DATA_RETENTION_TIME_IN_DAYS=1",
    },
}


def setup_checker(connection):
    if not RUNNING_ON_GHA:
        try:
            with connection.cursor() as cursor:
                res = cursor.execute(f"SHOW COMPUTE POOLS LIKE '{TEST_COMPUTE_POOL}';").fetchone()
                assert res[0] == TEST_COMPUTE_POOL
        except Exception:
            pytest.fail(f"create Compute Pool {TEST_COMPUTE_POOL} failed")


@pytest.fixture(scope="session")
def spcs_setup(connection, setup_basic, running_on_private_ci, running_on_public_ci):
    if running_on_private_ci:
        with connection.cursor() as cursor:
            cursor.execute("set snowservices_external_image_registry_allowlist = '*';").fetchone()
            cursor.execute(
                f"create compute pool if not exists {TEST_COMPUTE_POOL} "
                + f"with instance_family={TEST_INSTANCE_FAMILY} "
                + "min_nodes=1 max_nodes=5 auto_resume=true;"
            ).fetchone()[0]
        setup_checker(connection)

    if running_on_private_ci or running_on_public_ci:
        try:
            yield TEST_COMPUTE_POOL
        except Exception as e:
            raise e
        return

    # Running in notebook is indepenent of running in public or private CI or public CI or devvm
    # but notebook environment does not know about where it is running so any code which depends on
    # where the code is running cannot be handeled by notebook at the time this code was written
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        try:
            yield TEST_COMPUTE_POOL
        except Exception as e:
            raise e
        return

    SPCS_parameters = {
        "enable_snowservices": True,
        "enable_snowservices_user_facing_features": True,
    }
    with connection.cursor() as cursor:
        cursor.execute("use role accountadmin;").fetchone()[0]
        machine_info = cursor.execute("""CALL
            SYSTEM$SNOWSERVICES_MACHINE_IMAGE_REGISTER(
                '{"image":"k8s_snowservices", "tag": "sometag", "registry": "localhost:5000"}'
            )""").fetchone()[0]
        import json

        machine_id = json.loads(machine_info)["machineImageId"]
        cursor.execute(f"""
            select SYSTEM$SNOWSERVICES_MACHINE_IMAGE_SET_DEFAULT('CONTROLLER', {machine_id});""").fetchone()[0]
        cursor.execute(f"""
            select SYSTEM$SNOWSERVICES_MACHINE_IMAGE_SET_DEFAULT('WORKER', {machine_id});""").fetchone()[0]

        cursor.execute("use role sysadmin;").fetchone()[0]
        cursor.execute(f"call system$snowservices_create_instance_type('{TEST_INSTANCE_FAMILY}');").fetchone()[0]

        cursor.execute("use role accountadmin;").fetchone()[0]
        for k, v in SPCS_parameters.items():
            cursor.execute(f"alter account set {k}={v}").fetchone()[0]

        cursor.execute(
            f"create compute pool if not exists {TEST_COMPUTE_POOL} "
            + f"with instance_family={TEST_INSTANCE_FAMILY} "
            + "min_nodes=1 max_nodes=1 auto_resume=true;"
        ).fetchone()[0]

        setup_checker(connection)

        try:
            yield TEST_COMPUTE_POOL
        finally:
            cursor.execute(f"ALTER COMPUTE POOL {TEST_COMPUTE_POOL} STOP ALL").fetchone()[0]
            cursor.execute(f"drop compute pool if exists {TEST_COMPUTE_POOL}").fetchone()[0]
            cursor.execute("use role accountadmin;").fetchone()[0]
            for k in SPCS_parameters.keys():
                cursor.execute(f"alter account unset {k}").fetchone()[0]


@pytest.fixture(scope="session", autouse=True)
def setup_basic(connection):
    with connection.cursor() as cursor:
        # Like backup_database_schema, but scope of this fixture is session
        _database_name = cursor.execute("SELECT /* setup_basic */ CURRENT_DATABASE()").fetchone()[0]
        _schema_name = cursor.execute("SELECT /* setup_basic */ CURRENT_SCHEMA()").fetchone()[0]

        _last_database = _database_name
        _last_schema = _schema_name

        for db_name, db in objects_to_setup.items():
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS /* setup_basic */ {db_name} {db['params']}",
            )
            _last_database = db_name

            cursor.execute(f"USE DATABASE /* setup_basic */ {db_name}")  # just in case it already existed
            for schema_name in db["schemas"]:
                cursor.execute(
                    f"CREATE SCHEMA IF NOT EXISTS /* setup_basic */ {schema_name}",
                )
                _last_schema = schema_name

        cursor.execute(
            f"USE DATABASE /* setup_basic */ {_last_database}",
        )
        cursor.execute(
            f"USE SCHEMA /* setup_basic */ {_last_schema}",
        )

        try:
            yield
        finally:
            if _schema_name is not None:
                cursor.execute(f"USE SCHEMA /* setup_basic::reset */ {_database_name}.{_schema_name}")
            elif _database_name is not None:
                cursor.execute(f"USE DATABASE /* setup_basic::reset */ {_database_name}")


@pytest.fixture(scope="session")
def imagerepo(connection, spcs_setup) -> str:
    # When adding an inlined image repository YAML file, don't hard code the path to the test image
    # repository.  Instead, use this fixture and f-string this value in for the `{imagrepo}` substitution.
    # This way, there's only one thing to change across the entire test suite.
    # Legacy: return 'sfengineering-ss-lprpr-test2.registry
    #    .snowflakecomputing.com/testdb_python/public/ci_image_repository'
    if TEST_IR_URL is not None:
        return TEST_IR_URL
    else:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE IMAGE REPOSITORY IF NOT EXISTS {TEST_IMAGE_REPO};")
            return cursor.execute(f"SHOW IMAGE REPOSITORIES LIKE '{TEST_IMAGE_REPO}';").fetchone()[4]


@pytest.fixture(autouse=True)
# TODO: SNOW-1545034 make sure the role used here not hurt account
def use_accountadmin(connection, request):
    if "use_accountadmin" not in request.keywords:
        yield
        return

    with connection.cursor() as cursor:
        _current_role = cursor.execute("SELECT /* setup_basic */ CURRENT_ROLE()").fetchone()[0]
        try:
            cursor.execute("USE ROLE ACCOUNTADMIN")
        except Exception:
            pytest.xfail("Switch to role AccountAdmin failed")

        try:
            yield
        finally:
            if _current_role is not None:
                cursor.execute(f"USE ROLE /* setup_basic::reset */ {_current_role}")


@pytest.fixture
def setup_with_connector_execution(connection):
    @contextmanager
    def _setup(sqls_to_enable: List[StrictStr], sqls_to_disable: List[StrictStr]):
        with connection.cursor() as cursor:
            for sql in sqls_to_enable:
                cursor.execute(sql)

            try:
                yield
            finally:
                for sql in sqls_to_disable:
                    cursor.execute(sql)

    return _setup
