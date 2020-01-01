""" This module contains commonly used utility functions for logging. """

import termcolor as tc

import config # type: ignore



""" Make logger messages optional. """

def optional(logger_func):
    def out_func(msg: str):
        if config.LOGGER_ON:
            logger_func(msg)

    return out_func



""" Three following functions are not intense and are optional. """

@optional
def log(msg: str):
    tc.cprint(f'Log: {msg}.', attrs=['dark'])

@optional
def success(msg: str):
    tc.cprint(f'Success: {msg}.', 'green')

@optional
def warning(msg: str):
    tc.cprint(f'Warning: {msg}.', 'yellow')

@optional
def failure(msg: str):
    tc.cprint(f'Failure: {msg}.', 'red')



""" These are not optional. Average intensity. """

def warn(msg: str):
    tc.cprint(f'Warning: {msg}.', 'yellow')

def fail(msg: str):
    tc.cprint(f'Failure: {msg}.', 'red')



""" These functions are intense. """

def great(msg: str):
    tc.cprint(msg, 'green', attrs=['bold'])

def caution(msg: str):
    tc.cprint(msg, 'yellow', attrs=['bold'])

def alert(msg: str):
    tc.cprint(msg, 'red', attrs=['bold'])
