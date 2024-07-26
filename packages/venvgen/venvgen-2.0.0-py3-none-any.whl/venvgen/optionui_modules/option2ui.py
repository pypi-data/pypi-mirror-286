from ..general.ANSI_color import get_color_str
from ..general.ui_helper import introduction_screen, print_current_page
from ..general.system_control_protocol import GO_BACK_TO_VIEW_VENV, NO_LIBRARIES
from ..general.string_processing import str_to_list, list_to_str

from ..utils.system_check import check_venv_existence_with_id, check_libraries

from ..utils.requirement_manager import check_installed_libraries

import inquirer
from inquirer.themes import GreenPassion
import pandas as pd
from datetime import datetime



OPTION2_NAVIGATION     = 'menu > view venv details'
OPTION2_1_NAVIGATION   = f'{OPTION2_NAVIGATION} > view all venv'
OPTION2_2_NAVIGATION   = f'{OPTION2_NAVIGATION} > view venv (filtered)'
OPTION2_2_1_NAVIGATION = f'{OPTION2_2_NAVIGATION} > view latest created date'
OPTION2_2_2_NAVIGATION = f'{OPTION2_2_NAVIGATION} > view latest modified time'
OPTION2_2_3_NAVIGATION = f'{OPTION2_2_NAVIGATION} > view earliest created date'
OPTION2_2_4_NAVIGATION = f'{OPTION2_2_NAVIGATION} > view earliest modified time'
OPTION2_3_NAVIGATION   = f'{OPTION2_NAVIGATION} > venv details'
OPTION2_4_NAVIGATION   = f'{OPTION2_NAVIGATION} > venv edit'


OPTION2_HEADER     = f'          {get_color_str('View Venv Details', 'GREEN')}'
OPTION2_1_HEADER   = f'            {get_color_str('View All VENV', 'GREEN')}'
OPTION2_2_HEADER   = f'         {get_color_str('View Venv (filtered)', 'GREEN')}'
OPTION2_2_1_HEADER = f'   {get_color_str('View VENV (Sorted By Latest Created Date)', 'GREEN')}'
OPTION2_2_2_HEADER = f'   {get_color_str('View VENV (Sorted By Latest Modified Time)', 'GREEN')}'
OPTION2_2_3_HEADER = f'  {get_color_str('View VENV (Sorted By Earliest Created Date)', 'GREEN')}'
OPTION2_2_4_HEADER = f'  {get_color_str('View VENV (Sorted By Earliest Modified Time)', 'GREEN')}'
OPTION2_3_HEADER   = f'         {get_color_str('View Specific VENV Details', 'GREEN')}'
OPTION2_4_HEADER   = f'           {get_color_str('Venv Edit', 'GREEN')}'


def print_option2_page(navigation: str, header: str):
    introduction_screen()
    print_current_page(navigation)
    print(header)
    print()

def view_venv_menu():
    print_option2_page(OPTION2_NAVIGATION, OPTION2_HEADER)

    view_choice = [inquirer.List('view_choice', message = 'Options', choices = [
            '1. View All Venv',
            '2. View Venv (with Filter)',
            '3. View A Venv Details',
            '4. Edit Venv',
            '5. Back'
    ], default = '1. View All Venv')]

    user_answer = inquirer.prompt(view_choice, theme = GreenPassion())['view_choice']
    
    return user_answer[0]

def display_all_view(df: pd.DataFrame):
    print_option2_page(OPTION2_1_NAVIGATION, OPTION2_1_HEADER)
    print(df.to_markdown())
    print()
    print()
    print(f'<-- Press Enter to go back to {get_color_str('view venv details', 'MANGRETA')} menu.')
    input()

def display_with_filter_menu():
    print_option2_page(OPTION2_2_NAVIGATION, OPTION2_2_HEADER)

    view_filter_choice = [inquirer.List('view_filter_choice', message = 'Options', choices = [
            '1. View by Latest Created Day',
            '2. View by Latest Modified Time',
            '3. View by Earliest Created Day',
            '4. View by Earliest Modified Time',
            '5. Back'
    ], default = '1. View All Venv')]

    user_answer = inquirer.prompt(view_filter_choice, theme = GreenPassion())['view_filter_choice']
    return user_answer[0]


def input_no_of_row(navigation: str, header: str):
    valid_answer = False
    first_time = True

    while not valid_answer:
        print_option2_page(navigation, header)
        print(get_color_str('- Please input the number of rows you want to be displayed', 'GREEN'))
        print(get_color_str('- Default is 10 (press Enter in your answer)', 'GREEN'))
        print()

        if not first_time:
            print(get_color_str('Please input a valid answer', 'RED'))

        first_time = False

        try:
            no_of_rows = input('Number of Rows to be Displayed (Default 10): ')
            if no_of_rows == '' or no_of_rows == None:
                return 10
            else:
                no_of_rows = int(no_of_rows)
            return no_of_rows
        except ValueError:
            pass

def display_df(navigation: str, header: str, df: pd.DataFrame):
    print_option2_page(navigation, header)
    print(df.to_markdown())
    print()
    print()
    print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
    input()


def input_no_of_rows_latest_create() -> int:
    return input_no_of_row(OPTION2_2_1_NAVIGATION, OPTION2_2_1_HEADER)

def display_latest_create_date(df: pd.DataFrame):
    display_df(OPTION2_2_1_NAVIGATION, OPTION2_2_1_HEADER, df)

def input_no_of_rows_latest_modified() -> int:
    return input_no_of_row(OPTION2_2_2_NAVIGATION, OPTION2_2_2_HEADER)

def display_latest_modified_time(df: pd.DataFrame):
    display_df(OPTION2_2_2_NAVIGATION, OPTION2_2_2_HEADER, df)

def input_no_of_rows_earliest_create():
    return input_no_of_row(OPTION2_2_3_NAVIGATION, OPTION2_2_3_HEADER)

def display_earliest_create_date(df: pd.DataFrame):
    display_df(OPTION2_2_3_NAVIGATION, OPTION2_2_3_HEADER, df)

def input_no_rows_earliest_modified() -> int:
    return input_no_of_row(OPTION2_2_4_NAVIGATION, OPTION2_2_4_HEADER)

def display_earliest_modified_time(df: pd.DataFrame):
    display_df(OPTION2_2_4_NAVIGATION, OPTION2_2_4_HEADER, df)

def input_venv_id(navigation: str, header: str) -> int:
    valid_answer = False
    first_time = True
    exist_venv = False

    while not valid_answer or not exist_venv:
        print_option2_page(navigation, header)
        print(get_color_str('- Please input the venv id', 'GREEN'))
        print(get_color_str('- The id must be an integer', 'GREEN'))
        print(get_color_str('- Type "back" to go back to view venv', 'GREEN'))
        print()

        if not first_time and not valid_answer:
            print(get_color_str('Please input a valid answer', 'RED'))

        if not first_time and not exist_venv:
            print(get_color_str('Venv does NOT exist', 'RED'))

        first_time = False

        venv_id = input('VENV id: ')
        if venv_id == 'back':
            return GO_BACK_TO_VIEW_VENV

        try:
            venv_id = int(venv_id)
            valid_answer = True
        except ValueError:
            valid_answer = False
        
        if check_venv_existence_with_id(venv_id):
            return venv_id
        else:
            exist_venv = False
        

def input_venv_id_for_view():
    return input_venv_id(OPTION2_3_NAVIGATION, OPTION2_3_HEADER)

def display_specific_view(df: pd.DataFrame):
    print_option2_page(OPTION2_3_NAVIGATION, OPTION2_3_HEADER)
    print(df.to_markdown())
    print()
    print()
    print(f'<-- Press Enter to go back to {get_color_str('view venv details', 'MANGRETA')} menu.')
    input()

def input_venv_id_for_edit():
    return input_venv_id(OPTION2_4_NAVIGATION, OPTION2_4_HEADER)

def recover_venv():
    print_option2_page(OPTION2_4_NAVIGATION, OPTION2_4_HEADER)
    print(get_color_str('The given venv has lost the connection', 'RED'))
    yes_no_recover = [inquirer.List('yes_no_recover', message = 'Do you want to recover it?', choices = [
            '1. YES',
            '2. NO'
    ], default = '1. View All Venv')]

    user_answer = inquirer.prompt(yes_no_recover, theme = GreenPassion())['yes_no_recover']

    if user_answer[0] == '1':
        return True
    else:
        return False
    
def venv_edit_menu():
    print_option2_page(OPTION2_4_NAVIGATION, OPTION2_4_HEADER)
    venv_edit_option = [inquirer.List('venv_edit_option', message = 'Option:', choices = [
            '1. Install More Libraries',
            '2. Uninstall More Libraries'
    ], default = '1. Install More Libraries')]

    user_answer = inquirer.prompt(venv_edit_option, theme = GreenPassion())['venv_edit_option']
    return user_answer[0]

def venv_edit_install_library(venv_id):
    first_time: bool = True
    no_library: bool = True
    valid_libraries: bool = True
    is_installed: bool = False


    available: list = None
    not_available: list = None

    while first_time or (not first_time and (not valid_libraries or no_library or is_installed)):
        libraries = None
        print_option2_page(OPTION2_4_NAVIGATION, OPTION2_4_HEADER)
        print(get_color_str('- Please type "back" to go back to the view venv details', 'GREEN'))

        if not first_time and not valid_libraries:
            not_available = list_to_str(not_available, sep = ', ')
            print(get_color_str(f'These are not availabe libraries: {not_available}', 'RED'))
            print(get_color_str('Please type in the libraries again: ', 'RED'))
            not_available = None
            available = None

        if not first_time and no_library:
            print(get_color_str('Please insert the libraries name!', 'RED'))

        if not first_time and is_installed:
            print(get_color_str('The libraries have been installed already!', 'RED'))


        first_time = False

        libraries = input('Libraries (Separate by ","): ')


        
        if libraries == 'back':
            return GO_BACK_TO_VIEW_VENV
        
        if libraries == '' or libraries == None:
            no_library = True
            valid_libraries = True
            is_installed = False
        
            
        if libraries != '' and libraries != None:
            no_library = False

            libraries = str_to_list(libraries)
            available, not_available = check_libraries(libraries)

            if len(not_available) > 0:
                valid_libraries = False
                libraries = None
                is_installed = False

            elif len(check_installed_libraries(venv_id, available)[0]) > 0:
                is_installed = True
                no_library = False
                valid_libraries = True
            
            else:
                available = list_to_str(available, ' ')
                return available
            
def venv_edit_uninstall_library(venv_id):
    first_time: bool = True
    no_library: bool = True
    valid_libraries: bool = True
    is_not_installed: bool = False


    available: list = None
    not_available: list = None

    while first_time or (not first_time and (not valid_libraries or no_library or is_not_installed)):
        libraries = None
        print_option2_page(OPTION2_4_NAVIGATION, OPTION2_4_HEADER)
        print(get_color_str('- Please type "back" to go back to the view venv details', 'GREEN'))

        if not first_time and not valid_libraries:
            not_available = list_to_str(not_available, sep = ', ')
            print(get_color_str(f'These are not availabe libraries: {not_available}', 'RED'))
            print(get_color_str('Please type in the libraries again: ', 'RED'))
            not_available = None
            available = None

        if not first_time and no_library:
            print(get_color_str('Please insert the libraries name!', 'RED'))

        if not first_time and is_not_installed:
            print(get_color_str('The libraries have NOT been installed yet!', 'RED'))


        first_time = False

        libraries = input('Libraries (Separate by ","): ')


        
        if libraries == 'back':
            return GO_BACK_TO_VIEW_VENV
        
        if libraries == '' or libraries == None:
            no_library = True
            valid_libraries = True
            is_not_installed = False
        
            
        if libraries != '' and libraries != None:
            no_library = False

            libraries = str_to_list(libraries)
            available, not_available = check_libraries(libraries)

            if len(not_available) > 0:
                valid_libraries = False
                libraries = None
                is_not_installed = False

            elif len(check_installed_libraries(venv_id, available)[1]) > 0:
                is_not_installed = True
                no_library = False
                valid_libraries = True
            
            else:
                available = list_to_str(available, ' ')
                return available















# def input_install_venv_library():
#     print_option2_page(OPTION2_4_NAVIGATION, OPTION2_4_HEADER)
