"""-----------------------------------------------------------------------------
The `config` module contains metadata about the tool.
-----------------------------------------------------------------------------"""

import pathlib
import os
import string

import appdirs # type: ignore



""" Project Descriptors """

APP_NAME: str = 'pwds'
VERSION: str = '0.1alpha'
LICENSE: str = 'GPLv.3'
DESCRIPTION: str = 'Command Line Password Manager'
AUTHOR: str = 'Viktor A. Rozenko Voitenko'
AUTHOR_EMAIL: str = 'sharp.vik@gmail.com'





""" Github """

GITHUB_LINK: str = 'github.com'
AUTHOR_NICK: str = 'sharpvik'
AUTHOR_GITHUB_LINK: str = f'{GITHUB_LINK}/{AUTHOR_NICK}'
APP_GITHUB_LINK: str = f'{AUTHOR_GITHUB_LINK}/{APP_NAME}'





""" External Sources """

DICTIONARY_LINK: str = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'





""" Local Storage """

APP_FOLDER = pathlib.Path( os.path.abspath(__file__) ).parent.parent
DATA_FOLDER = pathlib.Path( appdirs.user_data_dir(APP_NAME, AUTHOR_NICK) )
EXEC_PATH = pathlib.Path(DATA_FOLDER.parent.parent, 'bin', APP_NAME) # UNIX OSs
MAIN_PATH = pathlib.Path(APP_FOLDER, 'src', 'main.py')
DICTIONARY_FILE = pathlib.Path(DATA_FOLDER, '.dictionary')
MASTERMAC_FILE = pathlib.Path(DATA_FOLDER, '.mastermac')
PWDS_STORE_FILE = pathlib.Path(DATA_FOLDER, '.pwds-store')
SALT_FILE = pathlib.Path(DATA_FOLDER, '.salt')





""" Project Config """

LOGGER_ON: bool = True
CHARACTER_SET: str = string.ascii_letters + string.digits + string.punctuation
