# SACpy

Simple Python based Steam account switcher for Linux

# Setup:

## Requirements

* Python

* Steam

## Accounts

* Create "accounts.sacpy" in the script's directory containing your accounts in the format of:
  
  ```
  username:password
  username:password
  username:password
  ...
  ```

# Usage:

To log in to an account you have added:

* Run `sac.py username`

To list the accounts in your accounts file

* Run `sac.py list`

To kill Steam

* Run `sac.py kill`

# TODO:

* Windows support
  * Add OS check (platform.system())
  * Account for different Steam path
* 2FA support (automatic copying of 2FA code to clipboard)
* GUI
* Installable package (`pyinstaller` [?](https://pyinstaller.org))
