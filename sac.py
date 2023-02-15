#!/usr/bin/env python

import subprocess
import psutil
import signal
import time
import sys
import os

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

# Check for username or command (kill) being provided
if len(sys.argv) < 2:
    print("[ERROR]: Provide a username or command!")
    print("Example: sac.py username\n\t sac.py kill")
    sys.exit(1)

# Assign provided username to a variable
username = sys.argv[1]

# If username is "kill", kill Steam (not like anyone has the username of "kill" right???)
if username == "kill":
    kill_if_running()
    sys.exit(1)

# Check for existence of "accounts.sacpy"
if not os.path.exists('accounts.sacpy'):
    print("[ERROR]: The 'accounts.sacpy' file does not exist.")
    print("Create accounts.sacpy in this directory, containing account information like so:")
    print("username:password\nusername:password\n...")
    sys.exit(1)

# Lists all the accounts in the file (does not show passwords)
if username == "list":
    with open('accounts.sacpy', 'r') as f:
        for line in f:
            line = line.strip()
            args = line.split(':')
            if len(args) == 2:
                print(args[0])
    sys.exit(1)

# Open accounts file, read each line, split each line by ":" and check if the username (arg[0]) matches our provided username
# If it matches, arg[1] is our password. Else print error saying account not found.
with open('accounts.sacpy', 'r') as f:
    for line in f:
        line = line.strip()
        args = line.split(':')
        if len(args) == 2 and args[0] == username:
            password = args[1]
            break
    else:
        print(f"[ERROR]: No matching account found in accounts.sacpy for the username: '{username}'")
        sys.exit(1)

# Launch steam with login parameters and the matched arguments
steam_command = ("steam " + "-login " + username + " " + password + " -console " + " & disown")

# Kill process.
kill_if_running()

print("[INFO]: Starting Steam")
os.system(steam_command)
