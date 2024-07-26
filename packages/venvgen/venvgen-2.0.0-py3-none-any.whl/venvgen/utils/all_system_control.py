# from utils.ANSI_color import *
# from utils.system_control_protocol import *
# from utils.option_manager import *
# from utils import macos_system_control as MacOS
# from utils import window_system_control as Windows

# from .system_control_protocol import *
from .option_manager import option1, option2, option3
import random
import hashlib


def sha256_generator():
    return hashlib.sha256(str(random.randint(-100000000000, 10000000000000)).encode('utf-8')).hexdigest()


    

def menu_choice_process(user_answer):
    if user_answer == '1':
        return option1()
    elif user_answer == '2':
        return option2()
    elif user_answer == '3':
        return option3()


