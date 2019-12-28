#!/usr/bin/python3

# embedded libs
import json, sys
from getpass import getpass

# third-party libs
from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20

# my libs
import ops, util
from util import bash



# constants
MAX_ATTEMPTS = 3
MASTERHASH_FILE = '.masterhash'
PWDS_FILE = '.pwds'



# functions
switch = lambda dct, val, pwds: None if val not in dct else dct[val](pwds)

def ismaster(pwd):
    with open(MASTERHASH_FILE, 'r') as masterhash_file:
        masterhash = masterhash_file.read()
    pwdhash = SHA256.new( data=pwd.encode() ).hexdigest()
    return masterhash == pwdhash

def getsecret(pwd):
    return SHA256.new(data=pwd[::-1].encode()).hexdigest().encode()[:32]

def getpwds(masterpwd):
    with open(PWDS_FILE, 'rb') as pwds_file:
        pwds = pwds_file.read() # bytes

    secret = getsecret(masterpwd)
    nonce = pwds[:8]
    ciphertext = pwds[8:]
    cipher = Salsa20.new(key=secret, nonce=nonce)
    return json.loads( cipher.decrypt(ciphertext).decode() ) # dict

def storepwds(masterpwd, pwds):
    pwds = json.dumps(pwds).encode()
    secret = getsecret(masterpwd)
    cipher = Salsa20.new(key=secret)

    with open(PWDS_FILE, 'wb') as pwds_file:
        pwds_file.write( cipher.nonce + cipher.encrypt(pwds) )



# entry point
def main(args):
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
    for i in range(MAX_ATTEMPTS):
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
    changed = switch({
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



if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print()
