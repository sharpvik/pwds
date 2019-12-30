# General Architecture

## Setup

Creates symlink between `config.EXEC_PATH` and `/path/to/pwds/src/main.py`.

> Setup script (say `setup.py`) is not yet implemented!

> Windows installer is not here either!



## Using the Tool

Args as follows (parsing with `click` lib):
1. `launch`
    - Gets master password (**no enforcements** as requested by the Reddit
      community)
    - Uses `appdirs` to store `.mastermac` by `HMAC`, 
      `.pwds` by `Salsa20`, and prefetched `.words`
2. `give`
3. `gen`
    - Uses `secrets.choice(lst)` to generate new passwords from `.words`
4. `see`
5. `cp`
6. `rm`



## Dependencies

| Lib Name       | Description                                                 |
|---------------:|-------------------------------------------------------------|
| `click`        | Easy command line argument parsing                          |
| `appdirs`      | Knowing where to store program data files                   |
| `requests`     | `HTTP` requests                                             |
| `pycryptodome` | Implementations of cryptographic algorithms                 |
| `colorama`     | Multiplatform teminal output coloring                       |
| `temcolor`     | Terminal output coloring                                    |



--------------------------------------------------------------------------------

## Footnotes

### Some Time in the Future

- Argon2 for hashing
- Allow custom word dicrionaries for password generation
