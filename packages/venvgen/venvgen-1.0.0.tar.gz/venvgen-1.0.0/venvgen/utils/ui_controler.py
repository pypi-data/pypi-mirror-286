
from .all_system_control import *
from .system_control_protocol import *
from .string_processing import *


from . import OS
from .ANSI_color import get_color_str
# from .system_check import get_this_project_version, refresh_check, check_dir_connectivity
from .ANSI_line_modification import *
import inquirer
from inquirer.themes import GreenPassion
    


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



    end_program = menu_choice_process(user_answer[0])


    if user_answer[0] == '4':
        OS.clear_screen()
        return True
    
    return end_program