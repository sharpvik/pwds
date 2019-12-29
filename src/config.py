from pathlib import Path
from os import path

MAX_ATTEMPTS = 3

WORDS_FILE_LINK = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'

PROJECT_FOLDER = Path( path.abspath(__file__) ).parent.parent

STORE_FOLDER = Path(PROJECT_FOLDER, 'store')

WORDS_FILE = Path(PROJECT_FOLDER, 'store/.words')

MASTERHASH_FILE = Path(PROJECT_FOLDER, 'store/.masterhash')

PWDS_FILE = Path(PROJECT_FOLDER, 'store/.pwds')

