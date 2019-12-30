"""
This module contains functions that secure the whole system through
cryptographic means.
"""

import hashlib
import secrets
import typing
import hmac

from Crypto.Cipher import Salsa20



"""
Encrypt passwords using salted PBKDF2 with 10**5 iteration count as key for
Salsa20 cipher.
"""
def encrypt_pwds(pwds_json: str, mpwd: str) -> typing.Tuple:
    salt: bytes = secrets.token_bytes(16)
    secret: bytes = hashlib.pbkdf2_hmac(
        'sha512', mpwd.encode(), salt, 10**5
    )[:32] # Salsa20 key length must be 32 bytes

    cipher = Salsa20.new(key=secret)

    # first 8 bytes of `pwds_encrypted` are cipher nonce
    pwds_encrypted = cipher.nonce + cipher.encrypt( pwds_json.encode() )

    # `salt` must also be stored and thus is returned as well
    return pwds_encrypted, salt



""" 
Produce HMAC for `pwds_encrypted` using reversed master passwordas key.
"""
def produce_mastermac(pwds_encrypted: bytes, mpwd: str) -> str:
    mastermac: str = hmac.new(
        mpwd[::-1].encode(), pwds_encrypted, hashlib.sha512
    ).hexdigest()

    return mastermac
