from ..utils import OS
from ..utils.system_check import refresh_check, get_this_project_version

from .ANSI_color import get_color_str

def introduction_screen():
    refresh_check()
    OS.clear_screen()
    print('_______________________________________')
    print(f'        {get_color_str('Python VENV Generator', 'GREEN')}     ')
    print()
    print(f' This Version:\t{get_this_project_version()}')
    print(' Created By:\tNguyen Tuan')
    print(f' Your OS:\t{OS.get_os_name()}')
    print('_______________________________________')

def print_current_page(current_page_name: str) -> None:
    print(f'Current Page: ' + get_color_str(current_page_name, 'MANGRETA'))
    print()