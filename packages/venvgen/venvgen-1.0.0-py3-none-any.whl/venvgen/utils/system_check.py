from .ANSI_color import get_color_str, print_color

# All of the imported functions that are not used in this module will be used by the other modules that import this module
from .database_manager import (
    check_database, 
    check_venv_connection, 
    check_project_dir_and_venv, 
    check_venv_existence_with_id, 
    get_specific_venv_connection
)
from .requirement_manager import check_requirement
from ..venvgen_version import __version__
from .depedencies_check import check_os

import os
import requests

# TODO: This function may need to be deleted
def init_check():
    check_database()
    check_requirement()

def refresh_check():
    check_venv_connection(check_os())
    check_requirement()

def get_this_project_version() -> str:
    return __version__

def check_dir_connectivity(dir: str) -> bool:
    return os.path.exists(dir)

def check_libraries(libraries: list) -> tuple[list, list]:
    available = []
    not_available = []

    print('Checking libraries availability...')

    for i in range(len(libraries)):

        status = requests.get(f'https://pypi.org/project/{libraries[i]}/').status_code
        
        if status == 200:
            available.append(libraries[i])

        if status == 404:
            not_available.append(libraries[i])

        percentage = ((i + 1) / len(libraries))
        percentage_100 = percentage * 100

        MAX_BAR_LEN = 50

        percentage_bar_len = int(percentage * MAX_BAR_LEN) - 1

        remaining_bar_len = MAX_BAR_LEN - percentage_bar_len - 1

        percentage_bar = '=' * percentage_bar_len + '>'
        remaining_bar  = '.' * remaining_bar_len


        print(f'Progress: |{percentage_bar}{remaining_bar}| {percentage_100:.2f}%', end = '\r')

    print()
    return available, not_available

