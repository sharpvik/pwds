import json
import os
# import platform # e.g. platform.system() => 'Linux' / 'Darwin' / 'Windows'

import click
import colorama
import termcolor as tc

import fun
import config



colorama.init() # make color printing multiplatform



@click.group()
def main():
    pass



"""
The `launch` command
    - Gets master password and enforces *good* master password practices
    - Uses `appdirs` to store `.mastermac` by `HMAC`, `.pwds-store` by
      `Salsa20`, and prefetched `.dictionary`
"""
@main.command(help='Initialize pwds. This will remove any existing data.')
def launch():
    # warn user if already launched
    if fun.already_launched():
        tc.cprint(
"""
CAUTION! It looks like `Pwds` Password Manger has already been launched before
on this machine. Running launch again will erase any existing data.
""",
            'yellow',
            attrs=['bold']
        )

        proceed = input(
            'Are you sure you want to continue (y/n)? '
        ).strip().lower() == 'y'

        if not proceed:
            return

    # get master password
    mpwd: str = fun.new_master_password()

    # dealing with local storage
    try:
        os.mkdir(config.DATA_FOLDER)
    except FileExistsError:
        pass

    pwds_json: str = json.dumps( dict() )
    fun.pwds_store_write(pwds_json, mpwd)
    fun.fetch_and_store_dictionary()



@main.command(help='Give/reset password to a given domain')
@click.argument('domain')
def give(domain: str):
    pass



@main.command(help='Generate new password for a given domain')
@click.argument('domain')
@click.option(
    '--pwdtype', default='words', help='Password type `words` or `random`'
)
@click.option(
    '--length', default=4,
    help="""Length is a number of words if `pwdstype` is `words` or length of
random string for `pwdtype` `rand`"""
)
def gen(domain: str, pwdtype: str, length: int):
    pass



@main.command(help='Give/reset password to some domain')
@click.argument('domain')
def see(domain: str):
    pass



@main.command(help='Give/reset password to some domain')
@click.argument('domain')
def copy(domain: str):
    pass



@main.command(help='Give/reset password to some domain')
@click.argument('domain')
def remove(domain: str):
    pass



if __name__ == '__main__':
    main()
