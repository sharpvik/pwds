import json
import os
from typing import Tuple, Dict

import click
import colorama # type: ignore

import config
import fun
import logger as logr
import prompt
import secure



colorama.init() # make color printing multiplatform



@click.group()
def main():
    pass





"""-----------------------------------------------------------------------------
The `launch` command
    - Gets master password and enforces *good* master password practices
    - Uses `appdirs` to store `.mastermac` by `HMAC`, `.pwds-store` by
      `Salsa20`, and prefetched `.dictionary`
-----------------------------------------------------------------------------"""

@main.command(help='Initialize pwds. This will remove any existing data.')
def launch():
    # warn user if already launched
    if fun.already_launched():
        logr.caution(
"""
CAUTION! It looks like `Pwds` Password Manger has already been launched before
on this machine. Running launch again will erase any existing data.
"""
        )

        proceed: bool = prompt.yes_no('Are you sure you want to continue?')

        if not proceed:
            return

    # get master password
    logr.caution(
"""
Now, you are going to choose your Master Password. Make sure it is a strong
password that is hard to guess.

Don't include common letter and number sequences like `123` and `abc`, make it
at least 8 characters long.

None of the rules above are enforced by the tool but are strongly recommended.
"""
    )
    mpwd: str = fun.new_password('Master Password')

    # dealing with local storage
    try:
        os.mkdir(config.DATA_FOLDER)
        logr.success('Storage folder created')
    except FileExistsError:
        pass

    # store passwords
    fun.pwds_store_write( dict(), mpwd )

    logr.success('New master password is set')

    # Fetching dictionary is a relatively long thing to do as it requests big
    # file from config.DICTIONARY_LINK to be requested from the internded, thus,
    # it is beneficial to skip that step whenever possible.
    if not os.path.exists(config.DICTIONARY_FILE):
        fun.fetch_and_store_dictionary()

    logr.success('Launch complete')





@main.command(help='Give/reset password to a given domain.')
@click.argument('domain')
def give(domain: str):
    # user auth by decrypting password dictionary
    mpwd: str
    pwds: Dict[str, str]
    mpwd, pwds = fun.auth()

    # get new password
    pwd: str = fun.new_password(f'Password for `{domain}`')

    # (re)set password
    pwds[domain] = pwd

    # store passwords
    fun.pwds_store_write(pwds, mpwd)





@main.command(help='Generate new password for a given domain.')
@click.argument('domain')
@click.option(
    '--pwdtype', default='words', help='Password type: `words` or `random`.'
)
@click.option(
    '--length', default=4,
    help='Length is a number of words if `pwdstype` is `words` or length of \
random string for `pwdtype` `rand`.'
)
def gen(domain: str, pwdtype: str, length: int):
    # user auth by decrypting password dictionary
    mpwd: str
    pwds: Dict[str, str]
    mpwd, pwds = fun.auth()

    # const declarations
    ALLOWED_PWD_TYPES: Tuple[str, str] = ('words', 'random')

    # validate --pwdtype
    if pwdtype not in ALLOWED_PWD_TYPES:
        opts: str = ' or '.join([f'`{t}`' for t in ALLOWED_PWD_TYPES])
        logr.fail(f'--pwdtype option must be {opts}')
        return

    # allow user to pick and choose
    while True:
        # generate potential password
        potential: str = secure.generate_password(pwdtype, length)

        # display potential password
        prompt.show_password('Potential password: ', potential)

        # ask user if they like it
        ok: bool = prompt.yes_no('Do you like it?')

        if ok:
            pwds[domain] = potential
            break

    # store passwords
    fun.pwds_store_write(pwds, mpwd)






@main.command(help='See password for given domain.')
@click.argument('domain')
def see(domain: str):
    mpwd: str
    pwds: Dict[str, str]
    mpwd, pwds = fun.auth()

    if domain in pwds:
        prompt.show_password(f'Password for `{domain}`: ', pwds[domain])
    else:
        logr.fail(f'Domain `{domain}` does not exist')





@main.command(help='Copy password from given source domain to target.')
@click.argument('source')
@click.argument('target')
def copy(source: str, target: str):
    # user auth by decrypting password dictionary
    mpwd: str
    pwds: Dict[str, str]
    mpwd, pwds = fun.auth()

    if source not in pwds:
        logr.fail(f'Domain `{source}` does not exist')
        return

    # check if target domain exists and get user confirmation to proceed
    if target in pwds:
        logr.caution(
f"""Looks like domain `{target}` already has an assigned password."""
        )

        proceed: bool = prompt.yes_no('Do you want to replace it?')

        if not proceed:
            return

    # copy password
    pwds[target] = pwds[source]

    # store passwords
    fun.pwds_store_write(pwds, mpwd)





@main.command(help='Remove domain-password entry.')
@click.argument('domain')
def remove(domain: str):
    mpwd: str
    pwds: Dict[str, str]
    mpwd, pwds = fun.auth()

    # pop password if it exists
    # nothing happens even if it doesn't
    pwds.pop(domain, None)

    # store passwords
    fun.pwds_store_write(pwds, mpwd)






if __name__ == '__main__':
    main()
