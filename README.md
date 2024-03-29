# SACpy

Simple Python based Steam account switcher for Linux.

Created just before Valve added an account switcher to Steam (you should probably just use that) :)))

# Setup:

## Requirements

* Python

* Steam

* OpenSSL

## Accounts

1. Create "accounts.sacpy" in the script's directory containing your accounts in the format of:
  
  ```
  username:password
  username:password
  username:password
  ...
  ```

2. Run `sac.py encrypt accountfilepassword` where "accountfilepassword" is your desired password for the file.

Now you should have an encrypted file named "accounts.sacpy.des3" which holds your account credentials.

# Usage:

Once you have added your account(s) and encrypted the file:

To log in to an account you have added:

* Run `sac.py username accountfilepassword` where "accountfilepassword" is your desired password for the file.

To list the accounts in your accounts file:

* Run `sac.py list accountfilepassword` where "accountfilepassword" is your desired password for the file.

To decrypt your accounts file (To modify it in plain text):

* Run `sac.py decrypt accountfilepassword` where "accountfilepassword" is your desired password for the file.

To kill Steam

* Run `sac.py kill`

# Warnings

* The encryption method currently in use isn't perfect, treat even the encrypted file as you would the decrypted one.

* This script runs Steam using the `-login` argument, meaning your username and password will be visible in your process list (for example, in `htop`).

# TODO:

* Windows support
  * Add OS check (platform.system())
  * Account for different Steam path
* 2FA support (automatic copying of 2FA code to clipboard)
* GUI
* Installable package (`pyinstaller` [?](https://pyinstaller.org))
