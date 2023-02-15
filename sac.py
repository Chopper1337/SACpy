#!/usr/bin/env python

import subprocess
import psutil
import signal
import time
import sys
import os
from pyfzf import FzfPrompt

# TODO:
# * Encode/Decode or Encryption/Decryption of passwords
# * Cleaner "steam_command"

# Check if Steam is running, returns boolean
def steam_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "steam":
            print("[INFO]: Steam running")
            return True
    print("[INFO]: Steam not running")
    return False

# Kills the Steam process
def kill_steam():
    print("[INFO]: Killing Steam")
    proc = subprocess.Popen(["pgrep", "steam"], stdout=subprocess.PIPE)
    for pid in proc.stdout:
        os.system("notify-send \"Killing Steam\"")
        try:
            os.kill(int(pid), signal.SIGTERM)
        except OSError as ex:
            continue

    # Wait for Steam to terminate !!
    time.sleep(8)

# Kill Steam only if it's running
def kill_if_running():
    if(steam_running()):
        kill_steam()

# Assign provided username to a variable
command = sys.argv[1] if len(sys.argv) > 1 else None

# If username is "kill", kill Steam (not like anyone has the username of "kill" right???)
if command == "kill":
    kill_if_running()
    sys.exit(1)

# Check for existence of "accounts.sacpy"
if not os.path.exists('accounts.sacpy'):
    print("[ERROR]: The 'accounts.sacpy' file does not exist.")
    print("Create accounts.sacpy in this directory, containing account information like so:")
    print("username:password\nusername:password\n...")
    sys.exit(1)

# Lists all the accounts in the file (does not show passwords)
if command == "list":
    with open('accounts.sacpy', 'r') as f:
        for line in f:
            line = line.strip()
            args = line.split(':')
            if len(args) == 2:
                print(args[0])
    sys.exit(1)

# Open the file and read the account data. Then prompt the user to select an account.
with open('accounts.sacpy', 'r') as f:
    accounts = {}
    lines = f.read().splitlines()
    if len(lines) == 0:
        print("[ERROR]: No accounts found in accounts.sacpy")
        sys.exit(1)
    for line in lines:
        line = line.strip()
        args = line.split(':')
        if len(args) == 2:
            accounts[args[0]] = args[1]
        else:
            print("[ERROR]: Invalid account format in accounts.sacpy")
            sys.exit(1)
    usernames = list(accounts.keys())
    fzf = FzfPrompt()
    selection = fzf.prompt(usernames, '--header="Select an account"')
    if selection == None:
        sys.exit(1)
    username = selection[0]
    password = accounts[username] 

# Launch steam with login parameters and the matched arguments
steam_command = f"steam -login {username} {password} -console & disown"
print(steam_command)

# Kill process.
kill_if_running()

print("[INFO]: Starting Steam")
os.system(steam_command)
