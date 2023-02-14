# SACpy

Simple Python based Steam account switcher for Linux

# Setup

## Requirements

* Python

* Steam

## Accounts

* Create "accounts.sacpy" containing your accounts in the format of:
  
  ```
  username:password
  username:password
  username:password
  ...
  ```

# Usage

To log in to an account you have added:

* Run `python sac.py username`

To kill Steam

* Run `python sac.py kill`

# TODO:

* Windows support
* 2FA support (automatic copying of 2FA code to clipboard)
* GUI
