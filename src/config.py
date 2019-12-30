"""
The `config` module contains metadata about the tool.
"""

import pathlib
import os

import appdirs



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
DATA_FOLDER = pathlib.Path( appdirs.user_data_dir(APP_NAME, AUTHOR) )
EXEC_PATH = pathlib.Path(DATA_FOLDER.parent, 'bin', APP_NAME)
DICTIONARY_FILE = pathlib.Path(DATA_FOLDER, '.dictionary')
MASTERMAC_FILE = pathlib.Path(DATA_FOLDER, '.mastermac')
PWDS_STORE_FILE = pathlib.Path(DATA_FOLDER, '.pwds-store')
SALT_FILE = pathlib.Path(DATA_FOLDER, '.salt')
