# mbd libs
from os import path, mkdir
from getpass import getpass

# my libs
import config, requests
from util import bash
from main import storehash, storepwds



# functions
def fetchwords():
    r = requests.get(config.WORDS_FILE_LINK)

    with open(config.WORDS_FILE, 'wb') as words_file:
        for pkg in list(r):
            words_file.write(pkg)



def init_pwds():
    """ warn user if some data has already been stored """
    if path.exists(config.MASTERHASH_FILE) or path.exists(config.PWDS_FILE):
        print(
            bash.bold( bash.warning('CAUTION! This will wipe out all your passwords and `.masterhash`!') )
        )
        proceed = input(
            'Do you want to continue (y/n)? '
        ).strip().lower() == 'y'

        if not proceed:
            return

    """ try to create a folder to store data into """
    try:
        mkdir(config.STORE_FOLDER)
    except FileExistsError:
        pass

    """ get master password + confirmation from user """
    masterpwd = str()

    while True:
        pwd = getpass('Master Password: ')
        pwd_confirm = getpass('Confirm Master Password: ')
        
        if pwd == pwd_confirm:
            masterpwd = pwd
            break

        print( bash.fail('Confirmation failed. Try again.') )
    
    """ store masterhash, master password, fetch words dictionary """
    storehash(masterpwd)
    storepwds( masterpwd, dict() ) # storing empty dictionary
    fetchwords()
