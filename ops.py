# embedded libs
from getpass import getpass
import json
from random import SystemRandom
from string import ascii_letters, digits, punctuation

# my libs
from util import bash



# constants
WORDS_FILE = 'words'
RAND = SystemRandom()
ALPHABET = ascii_letters + digits + punctuation

with open(WORDS_FILE, 'r') as words_file:
    WORDS = words_file.read().split('\n')



# internal functions
def _rand_choice(lst):
    randint = RAND.randrange( len(lst) )
    return lst[randint]

def _words_pwd(n):
    return ' '.join( [_rand_choice(WORDS) for i in range(n)] )

def _random_pwd(length):
    return ''.join( [_rand_choice(ALPHABET) for i in range(length)] )



# supported operations
def re_set(pwds):
    domain = input(
        'What domain is your new password for (e.g. "google")? '
    ).strip().lower()
    new_pwd = str()

    while True:
        pwd = getpass('New Password: ')
        pwd_confirm = getpass('Confirm New Password: ')

        if pwd == pwd_confirm:
            new_pwd = pwd
            break

        print( bash.fail('Confirmation failed. Try again.') )

    if domain in pwds:
        print(
            bash.warning('Looks like this domain already has an assigned password.')
        )
        change = input(
            'Are you sure you want to change it (y/n)? '
        ).strip().lower() == 'y'

        if change:
            pwds[domain] = new_pwd
            return True

        return False

    else:
        pwds[domain] = new_pwd
        return True



def gen(pwds):
    pwd_type = input(
        'What type of password do you want (words/random)? '
    ).strip().lower()

    if pwd_type not in ('words', 'random'):
        print(
            bash.warning('Password type `{pwd_type}` is not supported.') +
            bash.warning('Generation failed.')
        )
        return False

    length = int( input('How long do you want your password to be? ') )

    domain = input(
        'What domain is your new password for (e.g. "google")? '
    ).strip().lower()

    new_pwd = str()

    while True:
        pwd = _words_pwd(length) if pwd_type == 'words' else _random_pwd(length)

        print(  'Potential new password: ' + bash.bold( bash.blue(pwd) )  )
        ok = input('Do you like this one (y/n)? ').strip().lower() == 'y'

        if ok:
            new_pwd = pwd
            break

    if domain in pwds:
        print(
            bash.warning('Looks like this domain already has an assigned password.')
        )
        change = input(
            'Are you sure you want to change it (y/n)? '
        ).strip().lower() == 'y'

        if change:
            pwds[domain] = new_pwd
            return True

        return False

    else:
        pwds[domain] = new_pwd
        return True



def copy(pwds):
    domain_from = input(
        'From what domain to copy password (e.g. "google")? '
    ).strip().lower()

    if domain_from not in pwds:
        print(
            bash.fail(f'Domain {domain_from} does not exist. Failed to copy.')
        )
        return False

    domain_to = input(
        'What domain to copy password to (e.g. "google")? '
    ).strip().lower()

    pwds[domain_to] = pwds[domain_from]
    return True



def see(pwds):
    domain = input(
        'What domain password would you like to see (e.g. "google")? '
    ).strip().lower()

    pwd = pwds.pop(domain, None)

    if pwd is None:
        print( bash.warning('Domain `{domain}` is not there.') )
    else:
        print(  f'Password for `{domain}`: ' + bash.bold( bash.blue(pwd) )  )

    return False



def remove(pwds):
    domain = input(
        'What domain would you like to remove (e.g. "google")? '
    ).strip().lower()

    exists = pwds.pop(domain, False)

    if not exists:
        print( 
            bash.warning(f'Domain `{domain}` has never been stored in the first place.') +
            bash.warning(f'Cannot remove `{domain}`.')
        )

    return exists != False
