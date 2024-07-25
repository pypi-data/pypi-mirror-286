from ..general.ui_helper import introduction_screen, print_current_page
from ..general.sha256_generator import sha256_generator
from ..general.ANSI_color import get_color_str
from ..general.ANSI_line_modification import GO_UP_ONE_LINE
from ..general.system_control_protocol import GO_BACK_TO_MENU_PAGE, NO_REQUIREMENTS_FILE, NO_LIBRARIES
from ..general.string_processing import str_to_list, list_to_str

from ..utils.system_check import check_dir_connectivity, check_project_dir_and_venv, check_libraries

OPTION1_NAVIGATION = 'menu > create new venv'


def print_option1_page():
    introduction_screen()
    print_current_page(OPTION1_NAVIGATION)
    print(f'            {get_color_str('Create New VENV', 'GREEN')}            ')
    print()


def input_project_directory() -> str:

    first_time = True
    project_directory = None

    while first_time or (not first_time and (project_directory == None or project_directory == '')):
        print_option1_page()

        if not first_time:
            print(f'{get_color_str('Please fill in the valid Directory Name', 'RED')}')

        first_time = False
        
        sha_256_str = sha256_generator()
        print(f'sha256: {sha_256_str}')
        print('Paste this to your answer to go back to main menu')
        print()
        print()
        print()
        project_directory = input(f'Libraries / Dependencies in requirements.txt (Y/n):{GO_UP_ONE_LINE}Project Name / Venv Name:{GO_UP_ONE_LINE}Project Directory: ')
        print()
        print()
        print()

        if project_directory == sha_256_str:
            return GO_BACK_TO_MENU_PAGE

        else:
            directory_exist = check_dir_connectivity(project_directory)
            if not directory_exist:
                project_directory = None

    return project_directory

def input_venv_name(project_directory) -> str:

    first_time = True

    venv_name = None

    valid_project_dir_and_venv = True

    while first_time or (not first_time and (venv_name == None or venv_name == '' or not valid_project_dir_and_venv)):
        print_option1_page()
        
        if not first_time and (venv_name == None or venv_name == ''):
            print(f'{get_color_str('Please fill in the Venv Name', 'RED')}')

        if not first_time and not valid_project_dir_and_venv:
            print(f'{get_color_str('You CANNOT create the same VENV in the same Project Directory', 'RED')}')

        first_time = False
    
        sha_256_str = sha256_generator()
        print(f'sha256: {sha_256_str}')
        print('Paste this to your answer to go back to main menu')
        print()
        print(f'Project Directory: {project_directory}')
        print()

        venv_name = input(f'Libraries / Dependencies in requirements.txt (Y/n):{GO_UP_ONE_LINE}Project Name / Venv Name: ')
        print()
        print()

        if venv_name == sha_256_str:
            return GO_BACK_TO_MENU_PAGE
        elif check_project_dir_and_venv(project_directory, venv_name):
            valid_project_dir_and_venv = False
        else:
            return venv_name
        
def input_requirement_file(project_directory, venv_name) -> str:
    first_time = True
    yes_no_requirement = None

    while first_time or (not first_time and (yes_no_requirement == None or yes_no_requirement == '')):
        print_option1_page()

        if not first_time:
            print(f'{get_color_str('Please fill in the Valid Answer', 'RED')}')

        first_time = False


        sha_256_str = sha256_generator()
        print(f'sha256: {sha_256_str}')
        print('Paste this to your answer to go back to main menu')
        print()
        print(f'Project Directory: {project_directory}')
        print(f'Project Name / Venv Name: {venv_name}')
        yes_no_requirement = input(f'Libraries / Dependencies in requirements.txt (Y/n): ')

        if yes_no_requirement == sha_256_str:
            return GO_BACK_TO_MENU_PAGE
        
        if yes_no_requirement not in ('Y', 'y', 'N', 'n'):
            yes_no_requirement = None
        
    if yes_no_requirement == 'N' or yes_no_requirement == 'n':
        return NO_REQUIREMENTS_FILE
        
    if yes_no_requirement == 'Y' or yes_no_requirement == 'y':

        first_time = True
        requirement_file = None

        while first_time or (not first_time and requirement_file == None):
            print_option1_page()

            if not first_time:
                print(f'{get_color_str('Please fill in the Valid Requirement File Path', 'RED')}')

            first_time = False

            sha_256_str = sha256_generator()
            print(f'sha256: {sha_256_str}')
            print('Paste this to your answer to go back to main menu')
            print()
            print(f'Project Directory: {project_directory}')
            print(f'Project Name / Venv Name: {venv_name}')
            print(f'Libraries / Dependencies in requirements.txt (Y/n): {yes_no_requirement}')
            requirement_file = input('requirements.txt path: ')


            if requirement_file == None or requirement_file == '':
                return NO_REQUIREMENTS_FILE
            
            elif requirement_file == sha_256_str:
                return GO_BACK_TO_MENU_PAGE
            
            elif check_dir_connectivity(requirement_file):
                return requirement_file
            
            else:
                requirement_file = None


def input_libraries(project_directory, venv_name, requirement_file):
    if requirement_file != NO_REQUIREMENTS_FILE:
        return None
    
    first_time = True
    yes_no_libraries = None

    while first_time or (not first_time and (yes_no_libraries == None or yes_no_libraries == '')):
        print_option1_page()

        if not first_time:
            print(f'{get_color_str('Please fill in the Valid Answer', 'RED')}')

        first_time = False

        sha_256_str = sha256_generator()
        print(f'sha256: {sha_256_str}')
        print('Paste this to your answer to go back to main menu')
        print()
        print(f'Project Directory: {project_directory}')
        print(f'Project Name / Venv Name: {venv_name}')
        print(f'Libraries / Dependencies in requirements.txt (Y/n): N')
        yes_no_libraries = input('Set Up Venv with Libraries (Y/n): ')

        if yes_no_libraries == sha_256_str:
            return GO_BACK_TO_MENU_PAGE
        
        if yes_no_libraries not in ('Y', 'y', 'N', 'n'):
            yes_no_libraries = None

    if yes_no_libraries == 'N' or yes_no_libraries == 'n':
        return NO_LIBRARIES
        
    if yes_no_libraries == 'Y' or yes_no_libraries == 'y':

        first_time = True
        libraries = None
        valid_libraries = True
        available = None
        not_available = None

        while first_time or (not first_time and (not valid_libraries)):
            print_option1_page()

            if not first_time and not valid_libraries:
                not_available = list_to_str(not_available, sep = ', ')
                print(get_color_str(f'These are not availabe libraries: {not_available}', 'RED'))
                print(get_color_str('Please type in the libraries again: ', 'RED'))
                not_available = None
                available = None


            first_time = False

            sha_256_str = sha256_generator()
            print(f'sha256: {sha_256_str}')
            print('Paste this to your answer to go back to main menu')
            print()
            print(f'Project Directory: {project_directory}')
            print(f'Project Name / Venv Name: {venv_name}')
            print(f'Libraries / Dependencies in requirements.txt (Y/n): N')
            print(f'Set Up Venv with Libraries (Y/n): {yes_no_libraries}')
            libraries = input('Libraries (Separate by ","): ')

            if libraries == None or libraries == '':
                return NO_LIBRARIES
            
            elif libraries == sha_256_str:
                return GO_BACK_TO_MENU_PAGE
            
            libraries = str_to_list(libraries)
            available, not_available = check_libraries(libraries)

            if len(not_available) > 0:
                valid_libraries = False
                libraries = None
            else:
                available = list_to_str(available, ' ')
                return available


            
def input_venv_info() -> tuple[str, str, str, list]:

    project_directory = input_project_directory()
    if project_directory == GO_BACK_TO_MENU_PAGE:
        return GO_BACK_TO_MENU_PAGE, None, None, None

    venv_name = input_venv_name(project_directory)
    if venv_name == GO_BACK_TO_MENU_PAGE:
        return None, GO_BACK_TO_MENU_PAGE, None, None

    requirement_file = input_requirement_file(project_directory, venv_name)
    if requirement_file == GO_BACK_TO_MENU_PAGE:
        return None, None, GO_BACK_TO_MENU_PAGE, None

    libraries = input_libraries(project_directory, venv_name, requirement_file)
    if libraries == GO_BACK_TO_MENU_PAGE:
        return None, None, None, GO_BACK_TO_MENU_PAGE
    

    return project_directory, venv_name, requirement_file, libraries




    



