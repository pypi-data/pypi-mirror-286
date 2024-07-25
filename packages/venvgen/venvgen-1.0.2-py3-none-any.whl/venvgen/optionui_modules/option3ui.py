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



OPTION3_NAVIGATION     = 'menu > view logs'
OPTION3_1_NAVIGATION   = f'{OPTION3_NAVIGATION} > view all logs'
OPTION3_2_NAVIGATION   = f'{OPTION3_NAVIGATION} > view latest logs'
OPTION3_3_NAVIGATION   = f'{OPTION3_NAVIGATION} > view earliest logs'

OPTION3_HEADER     = f'           {get_color_str('View Logs', 'GREEN')}'
OPTION3_1_HEADER   = f'         {get_color_str('View All Logs', 'GREEN')}'
OPTION3_2_HEADER   = f'       {get_color_str('View Latest Logs', 'GREEN')}'
OPTION3_3_HEADER   = f'      {get_color_str('View Earliest Logs', 'GREEN')}'


def print_option3_page(navigation: str, header: str):
    introduction_screen()
    print_current_page(navigation)
    print(header)
    print()

def display_log_menu():
    print_option3_page(OPTION3_NAVIGATION, OPTION3_HEADER)

    view_log_choice = [inquirer.List('view_log_choice', message = 'Options', choices = [
            '1. View All Logs',
            '2. View Latest Logs',
            '3. View Earliest Logs',
            '4. Back',
    ], default = '1. View All Logs')]

    user_answer = inquirer.prompt(view_log_choice, theme = GreenPassion())['view_log_choice']
    return user_answer[0]

def input_no_of_row(navigation: str, header: str):
    valid_answer = False
    first_time = True

    while not valid_answer:
        print_option3_page(navigation, header)
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
    print_option3_page(navigation, header)
    print(df.to_markdown())
    print()
    print()
    print(f'<-- Press Enter to go back to {get_color_str('view venv filters', 'MANGRETA')} menu.')
    input()


def display_all_log(df):
    display_df(OPTION3_1_NAVIGATION, OPTION3_1_HEADER, df)

def input_number_of_row_latest_log():
    return input_no_of_row(OPTION3_2_NAVIGATION, OPTION3_2_HEADER)

def display_latest_log(df):
    display_df(OPTION3_2_NAVIGATION, OPTION3_2_HEADER, df)

def input_number_of_row_earliest_log():
    return input_no_of_row(OPTION3_3_NAVIGATION, OPTION3_3_HEADER)

def display_earliest_log(df):
    display_df(OPTION3_3_NAVIGATION, OPTION3_3_HEADER, df)