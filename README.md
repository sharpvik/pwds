# Pwds Password Manager



## User Guide


### UNIX-based Operating Systems (MacOS included)

Check that the package manager used at the top of the `install` script is right,
then run the following:

```bash
./install   # compiles Python code and produces `init` and `pwds`
./init      # and then follow instructions
./pwds      # to see available operations
./pwds [OP] # where `OP` is some supported operation (e.g. `gen`)
```


### Windows

> Windows installer script is coming soon.



## Vulnerabilities

If you think you can just replace the `.masterhash` file with your own hash and
just "crack it all open", then you are mistaken. Your master password is used to
generate the `secret` for `Salsa20` cipher, and if it's wrong, nothing is gonna
come out of it.

The `.masterhash` is there only to provide nice workflow and tell you whether
the password you are typing in is actually going to be able to decrypt `.pwds`.

