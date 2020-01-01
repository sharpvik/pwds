"""-----------------------------------------------------------------------------
This module contains functions that secure the whole system through
cryptographic means.
-----------------------------------------------------------------------------"""

import hashlib
import secrets
import hmac
import json
from typing import Tuple, Optional, Dict, List

from Crypto.Cipher import Salsa20

import storage
import config



"""-----------------------------------------------------------------------------
Encrypt passwords using salted PBKDF2 with 10**5 iteration count as key for
Salsa20 cipher.
-----------------------------------------------------------------------------"""

def encrypt_passwords(pwds_json: str, mpwd: str) -> Tuple[bytes, bytes]:
    salt: bytes = secrets.token_bytes(16)
    secret: bytes = hashlib.pbkdf2_hmac(
        'sha512', mpwd.encode(), salt, 10**5
    )[:32] # Salsa20 key length must be 32 bytes

    cipher = Salsa20.new(key=secret)

    # first 8 bytes of `pwds_encrypted` are cipher nonce
    pwds_encrypted: bytes = cipher.nonce + cipher.encrypt( pwds_json.encode() )

    # `salt` must also be stored and thus is returned as well
    return pwds_encrypted, salt





"""-----------------------------------------------------------------------------
Produce HMAC for `pwds_encrypted` using reversed salt. This is only used to
check whether salt or encrypted passwords are corrupt.
-----------------------------------------------------------------------------"""

def produce_mastermac(pwds_encrypted: bytes, salt: bytes) -> str:
    mastermac: str = hmac.new(
        salt[::-1], pwds_encrypted, hashlib.sha512
    ).hexdigest()

    return mastermac





"""-----------------------------------------------------------------------------
This function checks whether salt file and/or encrypted passwords got corrupt
using HMAC from config.MASTERMAC_FILE produced by the `produce_mastermac`
function from this module.
-----------------------------------------------------------------------------"""

def salt_and_pwds_store_ok():
    pwds_encrypted: bytes = storage.read_encrypted_passwords()
    salt: bytes = storage.read_salt()
    mac: str = produce_mastermac(pwds_encrypted, salt)
    mastermac: str = storage.read_mastermac()

    return mac == mastermac





"""-----------------------------------------------------------------------------
New passwords are generated based on the desired type (`words` or `random`) and
length. What `length` means obviously depends on password type.
-----------------------------------------------------------------------------"""

def generate_password(pwdtype: str, length: int) -> str:
    pwd: str

    if pwdtype == 'words':
        dictionary: List[str] = storage.read_dictionary()
        pwd = ' '.join( [secrets.choice(dictionary) for i in range(length)] )
    else:
        pwd = ''.join(
            [secrets.choice(config.CHARACTER_SET) for i in range(length)]
        )

    return pwd





"""-----------------------------------------------------------------------------
Passwords are decrypted using salt from config.SALT_FILE and secret that is
generated the same way as in the `encrypt_passwords` function.
-----------------------------------------------------------------------------"""

def decrypt_passwords(mpwd: str) -> Optional[ Dict[str, str] ]:
    salt: bytes = storage.read_salt()
    secret: bytes = hashlib.pbkdf2_hmac(
        'sha512', mpwd.encode(), salt, 10**5
    )[:32] # Salsa20 key length must be 32 bytes

    # first 8 bytes of `pwds_encrypted` are cipher nonce
    pwds_encrypted: bytes = storage.read_encrypted_passwords()
    nonce: bytes = pwds_encrypted[:8]
    pwds_encrypted = pwds_encrypted[8:]

    cipher = Salsa20.new(key=secret, nonce=nonce)    
    pwds_json: str = cipher.decrypt(pwds_encrypted).decode()

    # return None if JSON decoder throws exception
    try:
        pwds: Dict[str, str] = json.loads(pwds_json)
        return pwds
    except json.decoder.JSONDecodeError:
        return None
