class bash:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    header = lambda s: bash.HEADER + s + bash.END
    blue = lambda s: bash.BLUE + s + bash.END
    green = lambda s: bash.GREEN + s + bash.END
    warning = lambda s: bash.WARNING + s + bash.END
    fail = lambda s: bash.FAIL + s + bash.END
    bold = lambda s: bash.BOLD + s + bash.END
    underline = lambda s: bash.UNDERLINE + s + bash.END

    


def hint():
    print("""Usage hint: ./pwds [operation]
Operations include:
    > `set` - add new password / reset old one
    > `gen` - generate and add/reset new password
    > `cp` - copy password from one domain to another
    > `see` - show password for given domain
    > `rm` - remove password for given domain"""
    )
