"""-----------------------------------------------------------------------------
The `fun` module contains commonly used functions that may have to be shared
between multiple Python modules. In other words, all the "fun" is here :)
-----------------------------------------------------------------------------"""

import getpass
import os
import sys
import json
from typing import Dict, Tuple, Optional

import requests

import secure # type: ignore
import config # type: ignore
import storage # type: ignore
import logger as logr # type: ignore



"""-----------------------------------------------------------------------------
Check if `Pwds` Password Manager has already been launched on this machine.
-----------------------------------------------------------------------------"""

def already_launched():
    return os.path.exists(config.DATA_FOLDER)





"""-----------------------------------------------------------------------------
Ask user to input new password and return it.
-----------------------------------------------------------------------------"""

def new_password(pwd_name: str) -> str:
    pwd: str

    while True:
        pwd1: str = getpass.getpass(f'{pwd_name}: ').strip()
        pwd2: str = getpass.getpass(f'Confirm {pwd_name}: ').strip()

        if pwd1 != pwd2:
            logr.fail('Confirmation failed. Passwords differ')

        else:
            pwd = pwd1
            break

    return pwd





"""-----------------------------------------------------------------------------
Save encrypted passwords to `.pwds-store`, salt to `.salt`, HMAC verifier to
`.mastermac`.
-----------------------------------------------------------------------------"""

def pwds_store_write(pwds: Dict[str, str], mpwd: str):
    # type declarations
    pwds_encrypted: bytes
    salt: bytes

    # encrypt `pwds_json`
    pwds_json: str = json.dumps(pwds)
    pwds_encrypted, salt = secure.encrypt_passwords(pwds_json, mpwd)

    # produce HMAC for pwds_encrypted to verity that it hasn't been corrupted
    mastermac: bytes = secure.produce_mastermac(pwds_encrypted, salt).encode()

    todo: Dict = {
        pwds_encrypted: config.PWDS_STORE_FILE,
        mastermac: config.MASTERMAC_FILE,
        salt: config.SALT_FILE,
    }

    # write to `.pwds-store`
    for data, path in todo.items():
        with open(path, 'wb') as file:
            file.write(data)
            logr.success(f'Write to `{path}` complete')





"""-----------------------------------------------------------------------------
There is a default dictionary that I'm using to generate word-based passwords --
it is hosted by GitHub in some repo (for full link see config.DICTIONARY_LINK).
This function is used to fetch and store this dicrionary in appropriate place.
-----------------------------------------------------------------------------"""

def fetch_and_store_dictionary():
    logr.log('Fetching dictionary...')

    r = requests.get(config.DICTIONARY_LINK)

    with open(config.DICTIONARY_FILE, 'wb') as words_file:
        for pkg in list(r):
            words_file.write(pkg)

    logr.success('Dictionary fetched and stored')





"""-----------------------------------------------------------------------------
This is a *very important function*. It runs every time we want to do something
with passwords. This will ask user for master password, try to decrypt password
storage and return a dictionary of password if successfull.

This function only ever returns if it receives correct master password. The only
way to break out of it otherwise it to CTRL+C in the terminal. This is why we
don't need any confirmation return values like `auth_ok: bool`.
-----------------------------------------------------------------------------"""

def auth() -> Tuple[ str, Dict[str, str] ]:
    # check if salt and/or encrypted password file are corrupt
    if not secure.salt_and_pwds_store_ok():
        logr.alert(
f"""
Salt or password store appear to be corrupt. There isn't much we can do.
If you have a backup of those files, fetch it and replace both of them, if not,
please run `pwds launch`.

On your computer salt and passwords are stored here:
{config.SALT_FILE}
{config.PWDS_STORE_FILE}
"""
        )
        sys.exit(1)

    mpwd: str
    pwds: Optional[ Dict[str, str] ]

    while True:
        mpwd = getpass.getpass('Master Password: ').strip()
        pwds = secure.decrypt_passwords(mpwd)

        if pwds is not None:
            break
        else:
            logr.fail('Master Password incorrect. Try again.')

    return mpwd, pwds
