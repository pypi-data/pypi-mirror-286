from . import OS
from .package_directory_manager import get_requirement_dir, create_requirement_dir
from .database_manager import select_the_latest_inserted_venv_id, get_specific_venv_connection, select_all_venv_list, update_requirement

# from ..general.ANSI_color import get_color_str

import re




# TODO: check why this thing yield error circular import
# from ..general.string_processing import remove_version_from_library


import importlib

import os

def update_install_requirement(venv_id):
    _, project_dir, venv_name, requirement_file = get_specific_venv_connection(venv_id)
    pip_freeze = OS.get_requirement(project_dir, venv_name)

    if requirement_file is None:
        requirement_dir = get_requirement_dir()
        requirement_file = os.path.join(requirement_dir, f'{venv_id}.txt')

    with open(requirement_file, 'w') as f:
        f.write(pip_freeze)

    return requirement_file

def check_requirement():
    create_requirement_dir()

    ## Testing
    venv_list = select_all_venv_list()
    requirement_dir = get_requirement_dir()

    for i in range(len(venv_list)):
        venv_id, venv_name, _, _, project_dir, _ = venv_list[i]
        is_connected, *_ = get_specific_venv_connection(venv_id)
        if is_connected:
            requirement_path = os.path.join(requirement_dir, f'{venv_id}.txt')
            update_install_requirement(venv_id)
            update_requirement(venv_id, requirement_path)

        percentage = ((i + 1) / len(venv_list))
        percentage_100 = percentage * 100

        MAX_BAR_LEN = 50

        percentage_bar_len = int(percentage * MAX_BAR_LEN) - 1

        remaining_bar_len = MAX_BAR_LEN - percentage_bar_len - 1

        percentage_bar = '=' * percentage_bar_len + '>'
        remaining_bar  = '.' * remaining_bar_len

        print(f'Progress: |{percentage_bar}{remaining_bar}| {percentage_100:.2f}%', end = '\r')



    ###

def requirement_generator(project_dir, venv):
    requirement_dir = get_requirement_dir()
    latest_inserted_id = select_the_latest_inserted_venv_id()
    pip_freeze = OS.get_requirement(project_dir, venv)

    with open(os.path.join(requirement_dir, f'{latest_inserted_id}.txt'), 'w') as f:
        f.write(pip_freeze)

    return latest_inserted_id, os.path.join(requirement_dir, f'{latest_inserted_id}.txt')

def requirement_is_updated(venv_id: int, project_dir: str, venv: str) -> bool:
    requirement_dir = get_requirement_dir()
    latest_inserted_id = select_the_latest_inserted_venv_id()
    pip_freeze = OS.get_requirement(project_dir, venv)

    with open(os.path.join(requirement_dir, f'{latest_inserted_id}.txt'), 'r') as f:
        requirement_file = f.read(pip_freeze)

    if pip_freeze == requirement_file:
        return True
    else:
        return False
    
def remove_version_from_library(library):
    pattern = r'==.*\n'
    pattern = re.compile(pattern, re.X)
    no_version_library = re.sub(pattern, '', library)
    return no_version_library


def get_libraries_from_venv_id(venv_id: int) -> list:
    requirement_file = os.path.join(get_requirement_dir(), f'{venv_id}.txt')

    libraries = []

    with open(requirement_file, 'r') as f:
        for line in f.readlines():
            line = remove_version_from_library(line)
            libraries.append(line)

    return libraries



def check_installed_libraries(venv_id: int, libraries: list) -> tuple[list, list]:

    not_installed = []
    installed = []

    requirement_libraries = get_libraries_from_venv_id(venv_id)

    for i in range(len(libraries)):
        
        if libraries[i] in requirement_libraries:
            installed.append(libraries[i])
        else:
            not_installed.append(libraries[i])

        percentage = ((i + 1) / len(libraries))
        percentage_100 = percentage * 100

        MAX_BAR_LEN = 50

        percentage_bar_len = int(percentage * MAX_BAR_LEN) - 1

        remaining_bar_len = MAX_BAR_LEN - percentage_bar_len - 1

        percentage_bar = '=' * percentage_bar_len + '>'
        remaining_bar  = '.' * remaining_bar_len

        print(f'Progress: |{percentage_bar}{remaining_bar}| {percentage_100:.2f}%', end = '\r')

    return installed, not_installed

