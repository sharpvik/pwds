"""-----------------------------------------------------------------------------
The `fun` module contains commonly used functions that may have to be shared
between multiple Python modules. In other words, all the "fun" is here :)
-----------------------------------------------------------------------------"""

import getpass
import os
from typing import Dict

import requests

import secure
import config
import logger as logr



"""-----------------------------------------------------------------------------
Check if `Pwds` Password Manager has already been launched on this machine.
-----------------------------------------------------------------------------"""

def already_launched():
    return os.path.exists(config.DATA_FOLDER)



"""-----------------------------------------------------------------------------
Ask user to input new Master Password and return it. Warnings included.
-----------------------------------------------------------------------------"""

def new_master_password() -> str:
    logr.caution(
"""
Now, you are going to choose your Master Password. Make sure it is a strong
password that is hard to guess.

Don't include common letter and number sequences like `123` and `abc`, make it
at least 8 characters long.

None of the rules above are enforced by the tool but are strongly recommended.
"""
    )

    mpwd: str

    while True:
        mpwd1: str = getpass.getpass('Master Password: ').strip()
        mpwd2: str = getpass.getpass('Confirm Master Password: ').strip()

        if mpwd1 != mpwd2:
            logr.fail('Confirmation failed. Passwords differ')

        else:
            mpwd = mpwd1
            break

    return mpwd



"""-----------------------------------------------------------------------------
Save encrypted passwords to `.pwds-store`, salt to `.salt`, HMAC verifier to
`.mastermac`.
-----------------------------------------------------------------------------"""

def pwds_store_write(pwds_json: str, mpwd: str):
    # type declarations
    pwds_encrypted: bytes
    salt: bytes

    # encrypt `pwds_json`
    pwds_encrypted, salt = secure.encrypt_pwds(pwds_json, mpwd)

    # produce HMAC for pwds_encrypted to verity that it hasn't been corrupted
    mastermac: bytes = secure.produce_mastermac(pwds_encrypted, salt).encode()

    todo: Dict = {
        pwds_encrypted: config.PWDS_STORE_FILE,
        mastermac: config.MASTERMAC_FILE,
        salt: config.SALT_FILE,
    }

    for data, path in todo.items():
        with open(path, 'wb') as file:
            file.write(data)
            logr.success(f'Write to `{path}` complete')



def fetch_and_store_dictionary():
    logr.log('Fetching dictionary...')

    r = requests.get(config.DICTIONARY_LINK)

    with open(config.DICTIONARY_FILE, 'wb') as words_file:
        for pkg in list(r):
            words_file.write(pkg)

    logr.success('Dictionary fetched and stored')
