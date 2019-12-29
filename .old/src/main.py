#!/usr/bin/python3

# mbd libs
import json, sys, requests
from os import path, mkdir
from getpass import getpass

# third-party libs
from Crypto.Hash import SHA256
from Crypto.Cipher import Salsa20

# my libs
import ops, util
from util import bash
from init_pwds import init_pwds as init
from pwds import pwds
import config



# functions
def getsecret(pwd):
    return SHA256.new(data=pwd[::-1].encode()).hexdigest().encode()[:32]


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

