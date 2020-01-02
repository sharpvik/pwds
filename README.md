# Pwds Password Manager

*Pwds* is a simple command line password manager tool.



## Contents

1. [Status](#status)
2. [User Guide](#user-guide)
    - [Setup](#user-guide-setup)
    - [Run It](#run-it)
3. [Brief Algorithm Description](#algorithm-description)
    - [Storing Passwords](algorithm-description-storing-passwords)
    - [Verifying That Salt and Passwords Have Not Been Corrupted](algorithm-description-verifying)
    - [Decrypting Passwords](algorithm-description-decrypting-passwords)
4. [User Guide](#user-guide)
5. [Dependencies](#dependencies)
6. [Contribute](#contribute)



## <a name="status"></a> Status

| Command  | Status |
|---------:|--------|
| `launch` | `OK`   |
| `give`   | `OK`   |
| `gen`    | `OK`   |
| `see`    | `OK`   |
| `copy`   | `OK`   |
| `remove` | `OK`   |



## <a name="user-guide"></a> User Guide

### <a name="user-guide-setup"></a> Setup

> Setup script (say `setup.py`) is not yet implemented!

> Windows installer is not here either!

For now, you can

```bash
git clone https://github.com/sharpvik/pwds.git
cd pwds
pip3 install pipenv # if you don't have it yet
pipenv shell        # to create virtual environment
pipenv install      # to install dependecies from Pipfile
```


### <a name="run-it"></a> Run It

```
Usage: 
    user@user:pwds$ python3 src/main.py [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    copy    Copy password from given source domain to target.
    gen     Generate new password for a given domain.
    give    Give/reset password to a given domain.
    launch  Initialize pwds.
    remove  Remove domain-password entry.
    see     See password for given domain.
```



## <a name="algorithm-description"></a> Brief Algorithm Description

This tool is supposed to run locally, although, in future updates, I'm planning
to make it into a web service. All passwords are stored in an encrypted file in
location specified in [config.py]. In that same folder you can find `salt`,
`mastermac`, and `dictionary`. All these files are hidden (their names start
with a dot, like this `.name`).

What follows is a symbolic description of the algorithm.

### <a name="algorithm-description-storing-passwords"></a> Storing Passwords

```
secrets.token_bytes(16)                     => random salt
PBKDF2(random salt, master password)        => secret
Salsa20(secret, JSON object with passwords) => encrypted passwords
HMAC(random salt, encrypted passwords)      => mastermac
store(random salt, encrypted passwords, mastermac)
```

### <a name="algorithm-description-verifying"></a> Verifying That Salt and Passwords Have Not Been Corrupted

```
read(salt, encrypted passwords, mastermac)  => salt
                                            => encrypted passwords
                                            => mastermac
HMAC(random salt, encrypted passwords)      => test mac
assert test mac == mastermac
```

### <a name="algorithm-description-decrypting-passwords"></a> Decrypting Passwords

```
read(salt, encrypted passwords, mastermac)  => salt
                                            => encrypted passwords
                                            => mastermac
PBKDF2(random salt, master password)        => secret
Salsa20(secret, encrypted passwords)        => passwords
```



## <a name="dependencies"></a> Dependencies

| Lib Name       | Description                                 | Documentation                   |
|---------------:|---------------------------------------------|---------------------------------|
| `click`        | Easy command line argument parsing          | click.palletsprojects.com       |
| `appdirs`      | Knowing where to store program data files   | github.com/ActiveState/appdirs  |
| `requests`     | `HTTP` requests handling                    | 2.python-requests.org/en/master |
| `pycryptodome` | Implementations of cryptographic algorithms | pycryptodome.readthedocs.io     |
| `colorama`     | Multiplatform teminal output coloring       | github.com/tartley/colorama     |
| `temcolor`     | Terminal output coloring                    | pypi.org/project/termcolor      |

> Only third-party libraries are listed here. Actually, many more modules are
> used, however, those are Python standard library modules, so they just work.



## <a name="contribute"></a> Contribute

If you wish to contribute to this project, please inspect the [src](src) folder.
The algorithm is failry simple and can be deduced from just reading the code.
I'm trying really hard to keep it as clean as possible.

If there's a bug or something... don't hesitate to raise an issue here.

If you wish to contact me in person, see this [config.py] file -- it has my
personal email address (it is also present on my [GitHub profile page]).

[config.py]: src/config.py
[GitHub profile page]: https://github.com/shapvik
