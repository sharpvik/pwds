#!/usr/bin/python3

"""
IMPORTANT! READ CAREFULLY!

This is NOT a conventional `setup.py` script that uses `setuptools`.
This script contains some information about the project under 
`Project Description`, and a few lines of code that "install" `pwds` for you.

This script only works on UNIX-based Operating Systems and may require superuser
privileges to run properly! If you see any Permission Errors, do the following:

    ~$ chmod +x setup.py
    ~$ sudo ./setup.py

There is an `INSTALLATION_PATH` constant under `Prerequisites` -- it contains
the location where symbolic link to the script is goin to be created. You are
free to change that location if necessary.
"""

from os import path, symlink as ln, chmod
from pathlib import Path
import stat


""" Project Description """
NAME = 'pwds'
VERSION = '0.1alpha'
DESCRIPTION = 'Password Manager'
LICENSE = 'GPLv.3'
AUTHOR = 'Viktor A. Rozenko Voitenko'
AUTHOR_EMAIL = 'sharp.vik@gmail.com'


""" Prerequisites """
INSTALLATION_PATH = '/usr/local/bin/' + NAME # change if necessary
PROJECT_FOLDER = Path( path.abspath(__file__) ).parent
SRC_FOLDER = str( Path(PROJECT_FOLDER, 'src') )
MAIN_SCRIPT_PATH = str( Path(SRC_FOLDER, 'main.py') )


""" Installation """
try:
    ln(MAIN_SCRIPT_PATH, INSTALLATION_PATH)
except FileExistsError:
    pass

# give owner all necessary privileges over `src/main.py`
chmod(MAIN_SCRIPT_PATH, stat.S_IRWXU)

