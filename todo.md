# General Architecture



## Setup

Creates symlink between `/usr/local/bin/pwds` and `/path/to/pwds/src/main.py.



## Main

Args as follows (parsing with `click` lib):
1. `init`
    - Gets master password (enforce **good** master password)
    - Uses `appdirs` to store `.mastermac` by `HMAC`, 
      `.pwds` by `Salsa20`, and prefetched `.words`

2. `set`
3. `gen`
    - Uses `secrets.choice(lst)` to generate new passwords from `.words`
4. `see`
5. `cp`
6. `rm`



## Dependencies

- `click`
- `appdirs`
- `json`
- `sys`
- `requests`
- `os`
- `getpass`
- `Crypto`



## Footnotes


### Expect Soon

- Remove the MAX_ATTEMPTS limit


### Some Time in the Future

- Argon2 for hashing
- Allow custom word dicrionaries for password generation
