# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import os
import shutil
import tempfile

from typing import List

from snowflake.snowpark import Row, Session

from ..utils import random_string


def random_object_name() -> str:
    return random_string(8, prefix="test_object_")


def get_task_history(session: Session, name: str) -> List[Row]:
    query = (
        f"select * from table(information_schema.task_history("
        f"scheduled_time_range_start=>dateadd('hour',-1,current_timestamp()),"
        f"result_limit => 10,task_name=>'{name}'))"
    )
    return session.sql(query).collect()


def string_skip_space_and_cases(s):
    return s.replace(" ", "").upper()


def array_equal_comparison(arr1, arr2):
    if not arr1 and not arr2:
        return True
    if not arr1 or not arr2:
        return False

    return [string_skip_space_and_cases(i) for i in arr1] == [string_skip_space_and_cases(i) for i in arr2]


def connection_config(override_schema=None, override_database=None):
    config = {}
    try:
        from ..parameters import CONNECTION_PARAMETERS
    except ImportError:
        CONNECTION_PARAMETERS = None
        from snowflake.connector.config_manager import CONFIG_MANAGER

    # 2023-06-23(warsaw): By default, we read out of the [connections.snowflake] section in the config.toml file, but by
    # setting the environment variable SNOWFLAKE_DEFAULT_CONNECTION_NAME you can read out of a different section.
    # For example SNOWFLAKE_DEFAULT_CONNECTION_NAME='test' reads out of [connections.test]

    level0, level1 = ("connections", CONFIG_MANAGER["default_connection_name"])

    if CONNECTION_PARAMETERS is None:
        config = CONFIG_MANAGER[level0][level1]
    else:
        config = CONNECTION_PARAMETERS

    if override_schema:
        config["schema"] = override_schema
    if override_database:
        config["database"] = override_database
    return config


def connection_keys():
    return ["user", "password", "host", "port", "database", "schema", "account", "protocol", "role", "warehouse"]


def create_zip_from_paths(paths, output_filename):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            for path in paths:
                if os.path.isdir(path):
                    folder_name = os.path.basename(path)
                    temp_folder = os.path.join(temp_dir, folder_name)
                    shutil.copytree(path, temp_folder)
                elif os.path.isfile(path):
                    shutil.copy(path, temp_dir)
                else:
                    print(f"Warning: '{path}' is not a valid file or directory. Skipping.")

            shutil.make_archive(os.path.splitext(output_filename)[0], "zip", root_dir=temp_dir)
    except Exception as e:
        raise Exception(f"Error creating the snowflake core zip file:\n {e.with_traceback(None)}") from e


def backup_existing_create_and_use_new_database_and_schema(cursor, new_database_name, new_schema_name):
    old_database_name = cursor.execute("SELECT CURRENT_DATABASE()").fetchone()[0]
    old_schema_name = cursor.execute("SELECT CURRENT_SCHEMA()").fetchone()[0]

    # Database
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS /* setup_basic */ " f"{new_database_name} DATA_RETENTION_TIME_IN_DAYS=1",
    )
    cursor.execute(f"USE DATABASE {new_database_name}")

    # Schema
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {new_schema_name}")
    cursor.execute(f"USE SCHEMA {new_schema_name}")

    return old_database_name, old_schema_name


def upload_given_files_to_stage(cursor, stage_url, files):
    try:
        for file in files:
            cursor.execute(f"PUT file://{file} @{stage_url} AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
    except Exception as e:
        raise Exception(f"Error uploading files to the stage:\n {e.with_traceback(None)}") from e


def execute_notebook(cursor, notebook_name, stage_full_path, warehouse_name, notebook_file_name) -> bool:
    try:
        cursor.execute(
            f"CREATE OR REPLACE NOTEBOOK {notebook_name} "
            f"FROM '@{stage_full_path}' "
            f"MAIN_FILE = '{notebook_file_name}' QUERY_WAREHOUSE = {warehouse_name}"
        )
        cursor.execute(f"ALTER NOTEBOOK {notebook_name} ADD LIVE VERSION FROM LAST")
        cursor.execute(f"EXECUTE NOTEBOOK {notebook_name}()")
        return False
    except Exception as e:
        print(f"Error creating and executing the notebook file {notebook_file_name}:\n {e.with_traceback(None)}")
        return True
