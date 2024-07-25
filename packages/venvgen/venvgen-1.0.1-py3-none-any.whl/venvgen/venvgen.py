from .utils.ui_controler import menu_screen
from .general.ui_helper import introduction_screen, print_current_page
import warnings



def main():
    
    warnings.filterwarnings("ignore")

    end_program = False

    while not end_program:
        introduction_screen()
        print_current_page('menu')
        end_program = menu_screen()





