#!/usr/bin/python3

# embedded libs
from getpass import getpass
from os import path
import json

# third-party libs
from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20

# my libs
from util import bash



# constants
MASTERHASH_FILE = '.masterhash'
PWDS_FILE = 'pwds'



# functions
def getsecret(pwd):
    return SHA256.new(data=pwd[::-1].encode()).hexdigest().encode()[:32]

def storepwds(masterpwd, pwds):
    pwds = json.dumps(pwds).encode()
    secret = getsecret(masterpwd)
    cipher = Salsa20.new(key=secret)

    with open(PWDS_FILE, 'wb') as pwds_file:
        pwds_file.write( cipher.nonce + cipher.encrypt(pwds) )

def storehash(pwd):
    pwdhash = SHA256.new( data=pwd.encode() ).hexdigest()
    with open(MASTERHASH_FILE, 'w') as masterhash_file:
        masterhash = masterhash_file.write(pwdhash)




def init():
    # warning
    if path.exists('.masterhash') or path.exists('pwds'):
        print(
            bash.bold( bash.warning('CAUTION! This will wipe out all your passwords and `.masterhash`!') )
        )
        proceed = input(
            'Do you want to continue (y/n)? '
        ).strip().lower() == 'y'

        if not proceed:
            return

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



if __name__ == '__main__':
    init()