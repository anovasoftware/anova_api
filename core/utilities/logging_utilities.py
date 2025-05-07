from termcolor import cprint
from colorama import init

init()


def log_message(message, message_type=''):
    if message_type in ['success', 'green']:
        cprint(message, 'green')
    elif message_type in ['failure', 'red']:
        cprint(message, 'red')
    else:
        print(f'{message}')


