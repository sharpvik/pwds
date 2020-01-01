"""-----------------------------------------------------------------------------
This is the `storage` module. Its purpose is to abstract away local storage
transactions like reading and writing encrypted passwords.
-----------------------------------------------------------------------------"""

from typing import List

import config # type: ignore




def read_encrypted_passwords() -> bytes:
    with open(config.PWDS_STORE_FILE, 'rb') as pwds_store_file:
        return pwds_store_file.read()





def read_salt() -> bytes:
    with open(config.SALT_FILE, 'rb') as salt_file:
        return salt_file.read()





def read_mastermac() -> str:
    with open(config.MASTERMAC_FILE, 'r') as mastermac_file:
        return mastermac_file.read()





def read_dictionary() -> List[str]:
    with open(config.DICTIONARY_FILE, 'r') as dictionary_file:
        return dictionary_file.read().splitlines()
