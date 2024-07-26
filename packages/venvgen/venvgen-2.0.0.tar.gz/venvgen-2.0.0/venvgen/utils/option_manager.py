
from ..general.system_control_protocol import *
from ..general.ANSI_color import *
from ..optionui_modules import option1ui, option2ui, option3ui

from .database_manager import (
    insert_data_into_venv_info, 
    select_all_venv,
    select_top_latest_create_data_venv,
    select_top_latest_modified_data_venv,
    select_top_earliest_create_data_venv,
    select_top_earliest_modified_data_venv,
    select_specific_venv,
    update_requirement,
    update_data_venv_info,
    insert_install_edit_venv_log,
    insert_unistall_edit_venv_log,
    select_all_log,
    select_latest_log,
    select_earliest_log
)

from .requirement_manager import requirement_generator, update_install_requirement

from .system_check import refresh_check, get_specific_venv_connection

from datetime import date, datetime


import pandas as pd

from . import OS






def option1():

    project_directory, venv_name, requirement_file, libraries = option1ui.input_venv_info()
    if GO_BACK_TO_MENU_PAGE in (project_directory, venv_name, requirement_file, libraries):
        return False

    
    if requirement_file == NO_REQUIREMENTS_FILE:

        OS.create_venv(project_directory, venv_name)
        insert_data_into_venv_info(
            project_path = project_directory, 
            venv_name = venv_name, 
            created_date = date.today(), 
            requirement_file = None, 
            connect_status = get_color_str('yes', 'GREEN'), 
            last_modified = datetime.now()
        )

        if libraries != NO_LIBRARIES:
            OS.install_libraries(project_directory, venv_name, libraries)
        
    
    else:
        OS.create_venv(project_directory, venv_name)
        OS.install_libraries_with_requirement(project_directory, venv_name, requirement_file)
        insert_data_into_venv_info(
            project_path = project_directory, 
            venv_name = venv_name, 
            created_date = date.today(), 
            requirement_file = requirement_file, 
            connect_status = get_color_str('yes', 'GREEN'), 
            last_modified = datetime.now()
        )
        
    # else:
    #     OS.create_venv(project_directory, venv_name)
    #     insert_data_into_venv_info(
    #         project_path = project_directory, 
    #         venv_name = venv_name, 
    #         created_date = date.today(), 
    #         requirement_file = None, 
    #         connect_status = get_color_str('yes', 'GREEN'), 
    #         last_modified = datetime.now()
    #     )


    # TODO: check on this thing
    venv_id, requirement_path = requirement_generator(project_directory, venv_name)
    update_requirement(venv_id, requirement_path)
    return False

def option2_1():
    refresh_check()
    all_venv_df = select_all_venv()
    option2ui.display_all_view(all_venv_df)
    return False
    
def option2_2_1():
    no_of_rows = option2ui.input_no_of_rows_latest_create()
    latest_create_venv_df = select_top_latest_create_data_venv(no_of_rows)
    option2ui.display_latest_create_date(latest_create_venv_df)
    return False

def option2_2_2():
    no_of_rows = option2ui.input_no_of_rows_latest_modified()
    latest_modified_venv_df = select_top_latest_modified_data_venv(no_of_rows)
    option2ui.display_latest_modified_time(latest_modified_venv_df)
    return False

def option2_2_3():
    no_of_rows = option2ui.input_no_of_rows_earliest_create()
    earliest_create_venv_df = select_top_earliest_create_data_venv(no_of_rows)
    option2ui.display_earliest_create_date(earliest_create_venv_df)
    return False

def option2_2_4():
    no_of_rows = option2ui.input_no_rows_earliest_modified()
    earliest_modified_venv_df = select_top_earliest_modified_data_venv(no_of_rows)
    option2ui.display_earliest_modified_time(earliest_modified_venv_df)
    return False

    
def option2_2():
    refresh_check()

    option2_2_lookup_table = {
        '1': option2_2_1,
        '2': option2_2_2,
        '3': option2_2_3,
        '4': option2_2_4,
        '5': (lambda : True)
    }

    to_view_menu = False

    while not to_view_menu:
        user_choice = option2ui.display_with_filter_menu()
        to_view_menu = option2_2_lookup_table[user_choice]()
    return False

def option2_3():
    venv_id = option2ui.input_venv_id_for_view()
    if venv_id == GO_BACK_TO_VIEW_VENV:
        return False
    else:
        venv_detail = select_specific_venv(venv_id)
        option2ui.display_specific_view(venv_detail)


def option2_4():
    option2_4_lookup_table = {
        '1': option2ui.venv_edit_install_library,
        '2': option2ui.venv_edit_uninstall_library
    }


    venv_id = option2ui.input_venv_id_for_edit()

    if venv_id == GO_BACK_TO_VIEW_VENV:
        return False
    else:
        connected, project_dir, venv_name, requirement_file = get_specific_venv_connection(venv_id)

        if not connected and option2ui.recover_venv():
            OS.create_venv(project_dir, venv_name)
            OS.install_libraries_with_requirement(project_dir, venv_name, requirement_file)
            update_data_venv_info(connect_status = get_color_str('yes','GREEN'), last_modified = datetime.now(), venv_id = venv_id)
            

        #TODO: create an option2ui.venv_edit
        # create an option2ui.venv_edit_menu
        else:
            user_choice = option2ui.venv_edit_menu()

            

            libraries = option2_4_lookup_table[user_choice](venv_id)
            
            if libraries == GO_BACK_TO_VIEW_VENV:
                return False
            elif user_choice == '1':
                # print(venv_id, project_dir, venv_name)
                # input()



                OS.install_libraries(project_dir, venv_name, libraries)
                insert_install_edit_venv_log(venv_id)
                update_install_requirement(venv_id)
                return False
            elif user_choice == '2':
                OS.uninstall_libraries(project_dir, venv_name, libraries)
                insert_unistall_edit_venv_log(venv_id)
                update_install_requirement(venv_id)
                return False
            




    
    return False
        

def option2():
    
    option2_lookup_table = {
        '1': option2_1,
        '2': option2_2,
        '3': option2_3,
        '4': option2_4,
        '5': (lambda : True)
    }

    to_main_menu = False

    while not to_main_menu:
        user_choice = option2ui.view_venv_menu()

        to_main_menu = option2_lookup_table[user_choice]()
        
    return False

def option3():

    
    to_main_menu = False

    while not to_main_menu:
        user_choice = option3ui.display_log_menu()
        
        if user_choice == '1':
            all_log = select_all_log()
            to_main_menu = option3ui.display_all_log(all_log)
        elif user_choice == '2':
            no_of_rows = option3ui.input_number_of_row_latest_log()
            latest_log = select_latest_log(no_of_rows)
            to_main_menu = option3ui.display_latest_log(latest_log)
        elif user_choice == '3':
            no_of_rows = option3ui.input_number_of_row_earliest_log()
            earliest_log = select_earliest_log(no_of_rows)
            to_main_menu = option3ui.display_earliest_log(earliest_log)
        elif user_choice == '4':
            to_main_menu = True

    return False



    



