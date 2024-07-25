import re



# from utils.all_system_control import *
# from utils.ANSI_color import *
# from utils.system_control_protocol import *
# from utils.string_processing import *


from .all_system_control import *
from .system_control_protocol import *
from .string_processing import *
from typing import Literal

from ..general.ui_helper import introduction_screen, print_current_page

from . import OS
from .ANSI_color import get_color_str
from .system_check import get_this_project_version, refresh_check, check_dir_connectivity
from .ANSI_line_modification import *
import inquirer
from inquirer.themes import GreenPassion
    
def test_name():
    print(__name__)

# def introduction_screen():
#     refresh_check()
#     OS.clear_screen()
#     print('_______________________________________')
#     print(f'        {get_color_str('Python VENV Generator', 'GREEN')}     ')
#     print()
#     print(f' This Version:\t{get_this_project_version()}')
#     print(' Created By:\tNguyen Tuan')
#     print(f' Your OS:\t{OS.get_os_name()}')
#     print('_______________________________________')


# def print_current_page(current_page_name: str) -> None:
#     print(f'Current Page: ' + get_color_str(current_page_name, 'MANGRETA'))
#     print()


def create_new_project_screen(first_time = True, step: Literal['project_directory', 'venv', 'requirement', 'library_manual_input'] = None, *args, **kwargs):
    pass
    

def view_venv_info_screen(first_time = True, step: Literal['view_venv_menu', 'display_all_venv', 'display_latest_create_date', 'display_with_filter', 'input_no_of_rows_latest_create', 'input_no_of_rows_latest_modified', 'display_latest_modified_time'] = None, *arg, **kwargs):
    introduction_screen()
    print_current_page('menu > view venv details')
    print(f'         {get_color_str('View VENV Details', 'GREEN')}            ')
    print()

    if step == 'view_venv_menu':
        view_choice = [inquirer.List('view_choice', message = 'Options', choices = [
            '1. View All Venv',
            '2. View Venv (with Filter)',
            '3. View A Venv Details',
            '4. Edit Venv',
            '5. Back'
        ], default = '1. View All Venv')]

        user_answer = inquirer.prompt(view_choice, theme = GreenPassion())['view_choice']
        
        return user_answer[0]

    elif step == 'display_all_venv':
        introduction_screen()
        print_current_page('menu > view venv details > view all venv')
        print(f'            {get_color_str('View All VENV', 'GREEN')}            ')
        print()
        print(kwargs['df'].to_markdown())
        print()
        print()
        print(f'<-- Press Enter to go back to {get_color_str('view venv details', 'MANGRETA')} menu.')
        input()

    elif step == 'display_with_filter':
        introduction_screen()
        print_current_page('menu > view venv details > view venv (filtered)')
        view_filter_choice = [inquirer.List('view_filter_choice', message = 'Options', choices = [
            '1. View by Latest Created Day',
            '2. View by Latest Modified Time',
            '3. View by Earliest Created Day',
            '4. View by Earliest Modified Time',
            '5. Back'
        ], default = '1. View All Venv')]

        user_answer = inquirer.prompt(view_filter_choice, theme = GreenPassion())['view_filter_choice']
        return user_answer[0]


    elif step == 'input_no_of_rows_latest_create':
        valid_answer = False

        while not valid_answer:
            introduction_screen()
            print_current_page('menu > view venv details > view venv (filtered) > view latest created date')
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

    elif step == 'display_latest_create_date':
        introduction_screen()
        print_current_page('menu > view venv details > view venv (filtered) > view latest created date')
        print(f'       {get_color_str('View VENV (Sorted By Latest Created Date)', 'GREEN')}            ')
        print()
        print(kwargs['df'].to_markdown())
        print()
        print()
        print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
        input()

    elif step == 'input_no_of_rows_latest_modified':
        valid_answer = False

        while not valid_answer:
            introduction_screen()
            print_current_page('menu > view venv details > view venv (filtered) > view latest modified time')
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
        
    elif step == 'display_latest_modified_time':
        introduction_screen()
        print_current_page('menu > view venv details > view venv (filtered) > view latest modified time')
        print(f'       {get_color_str('View VENV (Sorted By Latest Modified Time)', 'GREEN')}            ')
        print()
        print(kwargs['df'].to_markdown())
        print()
        print()
        print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
        input()

    elif step == 'input_no_of_rows_earliest_create':
        valid_answer = False

        while not valid_answer:
            introduction_screen()
            print_current_page('menu > view venv details > view venv (filtered) > view earliest created date')
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

    elif step == 'display_earliest_create_date':
        introduction_screen()
        print_current_page('menu > view venv details > view venv (filtered) > view earliest created date')
        print(f'       {get_color_str('View VENV (Sorted By Earliest Created Date)', 'GREEN')}            ')
        print()
        print(kwargs['df'].to_markdown())
        print()
        print()
        print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
        input()


    elif step == 'input_no_of_rows_earliest_modified':
        valid_answer = False

        while not valid_answer:
            introduction_screen()
            print_current_page('menu > view venv details > view venv (filtered) > view earliest modified time')
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
        
    elif step == 'display_earliest_modified_time':
        introduction_screen()
        print_current_page('menu > view venv details > view venv (filtered) > view earliest modified time')
        print(f'       {get_color_str('View VENV (Sorted By Earliest Modified Time)', 'GREEN')}            ')
        print()
        print(kwargs['df'].to_markdown())
        print()
        print()
        print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
        input()

    elif step == 'input_venv_id':

        valid_answer = False

        while not valid_answer:
            introduction_screen()
            print_current_page('menu > view venv details > venv details')
            print(get_color_str('- Please input the venv id', 'GREEN'))
            print(get_color_str('- The id must be an integer', 'GREEN'))
            print(get_color_str('- Type "back" to go back to view venv', 'GREEN'))
            print()

            if not first_time:
                print(get_color_str('Please input a valid answer', 'RED'))

            first_time = False

            try:
                venv_id = input('VENV id: ')
                if venv_id == 'back':
                    return GO_BACK_TO_VIEW_VENV
                else:
                    venv_id = int(venv_id)
                    return venv_id
            except ValueError:
                pass

    elif step == 'display_specific_venv':
        introduction_screen()
        print_current_page('menu > view venv details > venv details')
        print()
        print(kwargs['df'].to_markdown())
        print()
        print()
        print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
        input()

    elif step == 'input_venv_id_for_edit':
        alid_answer = False

        while not valid_answer:
            introduction_screen()
            print_current_page('menu > view venv details > venv edit')
            print(get_color_str('- Please input the venv id', 'GREEN'))
            print(get_color_str('- The id must be an integer', 'GREEN'))
            print(get_color_str('- Type "back" to go back to view venv', 'GREEN'))
            print()

            if not first_time:
                print(get_color_str('Please input a valid answer', 'RED'))

            first_time = False

            try:
                venv_id = input('VENV id: ')
                if venv_id == 'back':
                    return GO_BACK_TO_VIEW_VENV
                else:
                    venv_id = int(venv_id)
                    return venv_id
            except ValueError:
                pass



def menu_screen():
    print(f'              {get_color_str('MENU', 'GREEN')}                     ')
    print()
    menu_choice = [inquirer.List('menu_choice', message = 'Options', choices = [
        '1. Create New Project',
        '2. View Created Virtual Enviroment',
        '3. View Activity Log',
        '4. Exit'
    ], default = '1. Create New Project')]
    user_answer = inquirer.prompt(menu_choice, theme = GreenPassion())['menu_choice']

    display_functions = [create_new_project_screen, view_venv_info_screen]

    end_program = menu_choice_process(user_answer[0], display_functions)
    # print(user_answer[0])





    if user_answer[0] == '4':
        OS.clear_screen()
        return True
    
    return end_program