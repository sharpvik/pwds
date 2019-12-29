#!/usr/bin/python3

# embedded libs
import json, sys, requests
from os import path, mkdir
from getpass import getpass

# third-party libs
from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20

# my libs
import ops, util
from util import bash
import config



# functions
def fetchwords():
    r = requests.get(config.WORDS_FILE_LINK)

    with open(config.WORDS_FILE, 'wb') as words_file:
        for pkg in list(r):
            words_file.write(pkg)


switch = lambda dct, val, pwds: None if val not in dct else dct[val](pwds)


def ismaster(pwd):
    with open(config.MASTERHASH_FILE, 'r') as masterhash_file:
        masterhash = masterhash_file.read()
    pwdhash = SHA256.new( data=pwd.encode() ).hexdigest()
    return masterhash == pwdhash


def getsecret(pwd):
    return SHA256.new(data=pwd[::-1].encode()).hexdigest().encode()[:32]


def getpwds(masterpwd):
    with open(config.PWDS_FILE, 'rb') as pwds_file:
        pwds = pwds_file.read() # bytes

    secret = getsecret(masterpwd)
    nonce = pwds[:8]
    ciphertext = pwds[8:]
    cipher = Salsa20.new(key=secret, nonce=nonce)
    return json.loads( cipher.decrypt(ciphertext).decode() ) # dict


def storehash(pwd):
    pwdhash = SHA256.new( data=pwd.encode() ).hexdigest()
    with open(config.MASTERHASH_FILE, 'w') as masterhash_file:
        masterhash = masterhash_file.write(pwdhash)


def storepwds(masterpwd, pwds):
    pwds = json.dumps(pwds).encode()
    secret = getsecret(masterpwd)
    cipher = Salsa20.new(key=secret)

    with open(config.PWDS_FILE, 'wb') as pwds_file:
        pwds_file.write( cipher.nonce + cipher.encrypt(pwds) )



def init():
    # warning
    if path.exists(config.MASTERHASH_FILE) or path.exists(config.PWDS_FILE):
        print(
            bash.bold( bash.warning('CAUTION! This will wipe out all your passwords and `.masterhash`!') )
        )
        proceed = input(
            'Do you want to continue (y/n)? '
        ).strip().lower() == 'y'

        if not proceed:
            return

    mkdir(config.STORE_FOLDER)

    masterpwd = str()

    while True:
        pwd = getpass('Master Password: ')
        pwd_confirm = getpass('Confirm Master Password: ')
        
        if pwd == pwd_confirm:
            masterpwd = pwd
            break

        print( bash.fail('Confirmation failed. Try again.') )
    
    storehash(masterpwd)
    storepwds( masterpwd, dict() ) # storing empty dictionary
    fetchwords()



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



def main():
    try:
        arg = sys.argv[1]
        init() if arg == 'init' else pwds()

    except IndexError:
        print( bash.fail('Not enoguh command line arguments.') )
        util.hint()
        sys.exit(1)
        
    except KeyboardInterrupt:
        print()



if __name__ == '__main__':
    main()

