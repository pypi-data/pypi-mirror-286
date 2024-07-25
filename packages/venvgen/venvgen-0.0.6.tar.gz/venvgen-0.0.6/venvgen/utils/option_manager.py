# from utils.system_control_protocol import *
# from utils.database_manager import *

from ..general.system_control_protocol import *
# from .system_control_protocol import *
from .database_manager import (
    connect_check_database, 
    insert_data_into_venv_info, 
    select_all_venv,
    select_top_latest_create_data_venv,
    select_top_latest_modified_data_venv,
    select_top_earliest_create_data_venv,
    select_top_earliest_modified_data_venv,
    select_specific_venv
)
from datetime import date, datetime
from .ANSI_color import *
from .system_check import refresh_check
import pandas as pd



from ..optionui_modules import option1ui

def option1(system_control, *args, **kwargs):
    refresh_check()

    project_directory, venv_name, requirement_file, libraries = option1ui.input_venv_info()
    if GO_BACK_TO_MENU_PAGE in (project_directory, venv_name, requirement_file, libraries):
        return False

    
    if requirement_file == NO_REQUIREMENTS_FILE:

        system_control.create_venv(project_directory, venv_name)
        insert_data_into_venv_info(
            project_path = project_directory, 
            venv_name = venv_name, 
            created_date = date.today(), 
            requirement_file = None, 
            connect_status = get_color_str('yes', 'GREEN'), 
            last_modified = datetime.now()
        )

        if libraries != NO_LIBRARIES:
            system_control.install_libraries(project_directory, venv_name, libraries)
        return False
    
    if requirement_file != NO_REQUIREMENTS_FILE:
        system_control.create_venv(project_directory, venv_name)
        system_control.install_libraries_with_requirement(project_directory, venv_name, requirement_file)
        insert_data_into_venv_info(
            project_path = project_directory, 
            venv_name = venv_name, 
            created_date = date.today(), 
            requirement_file = requirement_file, 
            connect_status = get_color_str('yes', 'GREEN'), 
            last_modified = datetime.now()
        )
        
    else:
        system_control.create_venv(project_directory, venv_name)
        insert_data_into_venv_info(
            project_path = project_directory, 
            venv_name = venv_name, 
            created_date = date.today(), 
            requirement_file = None, 
            connect_status = get_color_str('yes', 'GREEN'), 
            last_modified = datetime.now()
        )


def option2_1(display_function, con):
    refresh_check()
    all_venv_df = select_all_venv()
    display_function(first_time = True, step = 'display_all_venv', df = all_venv_df)
    return False
    
def option2_2_1(display_function, con):
    no_of_rows = display_function(first_time = True, step = 'input_no_of_rows_latest_create')
    latest_create_venv_df = select_top_latest_create_data_venv(no_of_rows)
    display_function(first_time = True, step = 'display_latest_create_date', df = latest_create_venv_df)
    return False

def option2_2_2(display_function, con):
    no_of_rows = display_function(first_time = True, step = 'input_no_of_rows_latest_modified')
    latest_modified_venv_df = select_top_latest_modified_data_venv(no_of_rows)
    display_function(first_time = True, step = 'display_latest_modified_time', df = latest_modified_venv_df)
    return False

def option2_2_3(display_function, con):
    no_of_rows = display_function(first_time = True, step = 'input_no_of_rows_earliest_create')
    earliest_create_venv_df = select_top_earliest_create_data_venv(no_of_rows)
    display_function(first_time = True, step = 'display_earliest_create_date', df = earliest_create_venv_df)
    return False

def option2_2_4(display_function, con):
    no_of_rows = display_function(first_time = True, step = 'input_no_of_rows_earliest_modified')
    earliest_modified_venv_df = select_top_earliest_modified_data_venv(no_of_rows)
    display_function(first_time = True, step = 'display_earliest_modified_time', df = earliest_modified_venv_df)
    return False

    
def option2_2(display_function, con):
    refresh_check()

    to_view_menu = False

    while not to_view_menu:
        user_choice = display_function(first_time = True, step = 'display_with_filter')

        if user_choice == '1':
            to_view_menu = option2_2_1(display_function, con)
        elif user_choice == '2':
            to_view_menu = option2_2_2(display_function, con)
        elif user_choice == '3':
            to_view_menu = option2_2_3(display_function, con)
        elif user_choice == '4':
            to_view_menu = option2_2_4(display_function, con)
        elif user_choice == '5':
            return False

    return False

def option2_3(display_function, con):
    venv_id = display_function(first_time = True, step = 'input_venv_id')
    if venv_id == GO_BACK_TO_VIEW_VENV:
        return False
    else:
        venv_detail = select_specific_venv(venv_id)
        display_function(first_time = True, step = 'display_specific_venv', df = venv_detail)


def option2_4(display_function, con):
    venv_id = display_function(first_time = True, step = 'input_venv_for_edit')

    if venv_id == GO_BACK_TO_VIEW_VENV:
        return False
    else:
        pass

def option2(display_function, *args, **kwargs):
    refresh_check()
    con = connect_check_database()

    

    to_main_menu = False

    while not to_main_menu:
        user_choice = display_function(first_time = True, step = 'view_venv_menu')
        if user_choice == '5':
            return False
        

        elif user_choice == '1':

            to_main_menu = option2_1(display_function, con)
        

        elif user_choice == '2':
            to_main_menu = option2_2(display_function, con)
        

        elif user_choice == '3':
            to_main_menu = option2_3(display_function, con)
        
        elif user_choice == '4':
            return False







    pass