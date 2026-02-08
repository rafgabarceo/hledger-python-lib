# hledger-python-lib
A Python wrapper for wrapping hledger calls

## Installation
`uv` is the main way to utilize this Python package. `hledger` must be installed beforehand.

## TODO
- [ ] Read an input `.hledger.journal` file into memory.
    - [ ] User suppliable
    - [ ] Defaults to the home location if non is provided
    - [ ] Once read into memory, move this file into a temporary location
        - [ ] Implement a Lock on this temporary location

- [ ] List accounts
- [ ] List transactions of an account

- [ ] Perform transformations using add
    - [ ] The transformations should be performed in the temporary location.
    - [ ] The transformations must be asynchronous, thus locking is important.
    - [ ] State of the locker must be a hidden implementation.
        - [ ] Implement this as an internal state of some class


- [ ] Perform transformations using edit
    - [ ] Edit entries
        - [ ] Modify date
        - [ ] Modify the payee
        - [ ] Add or remove comments
        - [ ] Modify credit and debit
        - [ ] Perform validation 

