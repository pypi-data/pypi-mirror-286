import sqlite3
import pandas as pd
import os
import types
from datetime import datetime

# from utils.sql_command import *

from .package_directory_manager import get_database_path, create_database_dir
from .sql_command import *
from .ANSI_color import *

'''
Database:

venv_info(id, project_path, venv_name, created_date, requirement_file, connect_status)

'''

def check_database() -> None:
    # If the database directory don't exist this function will create one, else pass
    create_database_dir()
    con = sqlite3.connect(get_database_path())
    cur = con.cursor()

    # If the require tables are not created, these functions will create them
    cur.execute(CREATE_VENV_INFO_SQL)
    cur.execute(CREATE_VENV_LOG_SQL)
    cur.execute(CREATE_VENV_INSERT_TRIGGER_LOG_SQL)
    cur.execute(CREATE_VENV_UPDATE_STATUS_TRIGGER_LOG_SQL)
    con.close()

# It is RECOMMENDED to use this function to safely connect to the database
def connect_check_database() -> sqlite3.Connection:
    # This will return the connection to the database but it will check if the database is availabe first

    check_database()
    con = sqlite3.connect(get_database_path())
    return con

def insert_data_into_venv_info(*args, **kwargs):
    con = connect_check_database()
    cur = con.cursor()
    cur.execute(INSERT_INTO_VENV_INFO_SQL, (kwargs['project_path'], kwargs['venv_name'], kwargs['created_date'], kwargs['requirement_file'], kwargs['connect_status'], kwargs['last_modified']))
    con.commit()
    con.close()

def update_data_venv_info(*args, **kwargs):
    con = connect_check_database()
    cur = con.cursor()
    cur.execute(UPDATE_CONNECT_STATUS_VENV_INFO_SQL, (kwargs['connect_status'], kwargs['last_modified'], kwargs['venv_id']))
    con.commit()
    con.close()


def check_venv_connection(system_control: types.ModuleType, *args, **kwargs):
    con = connect_check_database()
    cur = con.cursor() 
    result = cur.execute(SELECT_ALL_VENV_SQL)
    venv_info = result.fetchall()
    for i in range(len(venv_info)):
        venv_id, venv_name, _, connect_status, project_path, _ = venv_info[i]
        # code_status = system_control.activate_venv(project_path, venv_name)
        # if code_status != 0 and connect_status != get_color_str('no', 'RED'):
        #     update_data_venv_info(con, connect_status = get_color_str('no', 'RED'), venv_name = venv_name, last_modified = datetime.now())
        if not system_control.check_venv(project_path, venv_name) and connect_status != get_color_str('no', 'RED'):
            update_data_venv_info(con, connect_status = get_color_str('no', 'RED'), venv_id = venv_id, last_modified = datetime.now())
    con.close()

def select_all_venv():
    con = connect_check_database()
    df = pd.read_sql(SELECT_ALL_VENV_SQL, con)
    con.close()
    return df

def select_top_latest_create_data_venv(no_of_rows: int) -> pd.DataFrame:
    con = connect_check_database()
    no_of_rows = str(no_of_rows)

    df = pd.read_sql(SELECT_TOP_LATEST_CREATE_DATA_VENV_SQL.replace('?', no_of_rows), con)
    con.close()
    return df

def select_top_latest_modified_data_venv(no_of_rows: int) -> pd.DataFrame:
    con = connect_check_database()
    no_of_rows = str(no_of_rows)

    df = pd.read_sql(SELECT_TOP_LATEST_MODIFIED_DATA_VENV_SQL.replace('?', no_of_rows), con)
    con.close()
    return df

def select_top_earliest_create_data_venv(no_of_rows: int) -> pd.DataFrame:
    con = connect_check_database()
    no_of_rows = str(no_of_rows)

    df = pd.read_sql(SELECT_TOP_EARLIEST_CREATE_DATA_VENV_SQL.replace('?', no_of_rows), con)
    con.close()
    return df

def select_top_earliest_modified_data_venv(no_of_rows: int) -> pd.DataFrame:
    con = connect_check_database()
    no_of_rows = str(no_of_rows)

    df = pd.read_sql(SELECT_TOP_EARLIEST_MODIFIED_DATA_VENV_VIEW.replace('?', no_of_rows), con)
    con.close()
    return df

def select_specific_venv(venv_id: int) -> pd.DataFrame:
    con = connect_check_database()
    venv_id = str(venv_id)

    df = pd.read_sql(SELECT_SPECIFIC_VENV_SQL.replace('?', venv_id), con)
    con.close()
    return df

def check_project_dir_and_venv(project_dir, venv):
    con = connect_check_database()
    cur = con.cursor()
    result = cur.execute(SELECT_PROJECT_DIR_AND_VENV_SQL, (project_dir, venv))
    project_venv = result.fetchall()
    con.close()
    if len(project_venv) > 0:
        return True
    else:
        return False
    