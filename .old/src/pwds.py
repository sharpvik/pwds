# mbd libs
import sys, json
from getpass import getpass

# third-party libs
from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20

# my libs
from util import bash
import util, config, ops
from main import storepwds, getsecret



# functions
def ismaster(pwd):
    with open(config.MASTERHASH_FILE, 'r') as masterhash_file:
        masterhash = masterhash_file.read()
    pwdhash = SHA256.new( data=pwd.encode() ).hexdigest()
    return masterhash == pwdhash


def getpwds(masterpwd):
    with open(config.PWDS_FILE, 'rb') as pwds_file:
        pwds = pwds_file.read() # bytes

    secret = getsecret(masterpwd)
    nonce = pwds[:8]
    ciphertext = pwds[8:]
    cipher = Salsa20.new(key=secret, nonce=nonce)
    return json.loads( cipher.decrypt(ciphertext).decode() ) # dict



# entry point
def pwds():
    args = sys.argv[1:]

    """
    First command line argument is supposed to represent the operation user
    wants to perform.
    """
    try:
        op = args[0]
    except IndexError:
        print( bash.fail('Not enoguh command line arguments.') )
        util.hint()
        sys.exit(1)

    """ Retrieve master password. """
    masterpwd = str()
    for i in range(config.MAX_ATTEMPTS):
        pwd = getpass('Master Password: ')
        if ismaster(pwd):
            masterpwd = pwd
            break
        print( bash.fail('Wrong password. Try again.') )
    else:
        print( 
            bash.fail("You've exhausted the maximum number of password attempts.")
        )
        sys.exit(0)

    """ Use master password to retrieve all passwords from storage `pwds`. """
    pwds = getpwds(masterpwd)

    """ Final decision making as to what command to execute. """
    changed = (
        lambda dct, val, pwds: None if val not in dct else dct[val](pwds)
    )({
        'set': ops.re_set,
        'gen': ops.gen,
        'cp': ops.copy,
        'see': ops.see,
        'rm': ops.remove,
    }, op, pwds)

    """ Store passwords again if changed. """
    if changed:
        storepwds(masterpwd, pwds)
    elif changed is None:
        print( bash.warning(f'Operation {op} is not supported.') )
        util.hint()
