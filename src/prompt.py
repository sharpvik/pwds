"""-----------------------------------------------------------------------------
This module contains functions that ease out prompting user for input.
-----------------------------------------------------------------------------"""

import termcolor as tc



"""-----------------------------------------------------------------------------
The `yes_no` function returns True if the answer was 'y' and False otherwise.
Any answer except 'y' is considered to be against the proposition (`msg`).
-----------------------------------------------------------------------------"""

def yes_no(msg: str) -> bool:
    return input(f'{msg} (y/n) ').strip().lower() == 'y'





def show_password(msg: str, pwd: str):
    print(msg, end='')
    tc.cprint(pwd, 'blue', attrs=['bold'])
