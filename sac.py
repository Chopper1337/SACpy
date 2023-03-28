#!/usr/bin/env python

import subprocess
import psutil
import signal
import time
import sys
import os

# TODO:
# * Replace the `time.sleep(8)` with a proper check for Steam being terminated

# Check for existence of the accounts file, encrypted or not
def accounts_file_exists(encrypted: bool):
    if encrypted:
        filename = "accounts.sacpy.des3"
        msg = "Please encrypt your 'accounts.sacpy' file!"
    else:
        filename = "accounts.sacpy"
        msg = "Please create your 'accounts.sacpy' file!"

    if os.path.exists(filename):
        return True;
    else:
        print(f"[ERROR]: The '{filename}' file does not exist.")
        print(msg)
        sys.exit(1)

# Check if Steam is running, returns boolean
def steam_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "steam":
            print("[INFO]: Steam running")
            os.system(f"notify-send \"Steam running\"")
            return True
    print("[INFO]: Steam not running")
    os.system(f"notify-send \"Steam not running\"")
    return False

# Launch Steam with provided username and password
def launch_steam(username, password):
    # Launch steam with login parameters and the matched arguments
    steam_command = f"steam -login {username} {password} -console & disown"

    # Kill process.
    kill_if_running()

    print(f"[INFO]: Starting Steam account {username}")
    os.system(f"notify-send \"Starting Steam account {username}\"")
    os.system(steam_command)

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

# Escape all special characters in a string
def escape_string(s: str):
    for c in ['\\', '"', '$', '`', '!', '(', ')', '[', ']', '{', '}', '|', ';', "'", ' ', '>', '<', '&', '*', '?', '~', '^', '#', '%', '@', ' ']:
        s = s.replace(c, f"\\{c}")
    return s

# Encrypt the accounts file with openssl des3
def encrypt_accounts_file(pw: str):
    os.system(f"openssl des3 -k {pw} < accounts.sacpy > accounts.sacpy.des3")

# Decrypt the accounts file with openssl des3
def decrypt_accounts_file(pw: str):
    if os.path.exists('accounts.sacpy.des3'):
        os.system(f"openssl des3 -d -k {pw} < accounts.sacpy.des3 > accounts.sacpy")

def clean_up():
    os.remove("accounts.sacpy")

def list_accounts():
    decrypt_accounts_file(sys.argv[2])
    with open('accounts.sacpy', 'r') as f:
        for line in f:
            line = line.strip()
            args = line.split(':')
            if len(args) == 2:
                print(args[0])
    clean_up()
    sys.exit(1)

# Check for username or command (kill) being provided
if len(sys.argv) < 2:
    print("[ERROR]: Provide a username or command!")
    print("Example: sac.py username filepasswordhere (to log in)\n\t sac.py list filepasswordhere (to list accounts in your accounts.sacpy file)\n\t sac.py encrypt filepasswordhere (to encrypt your accounts.sacpy file)\n\t sac.py decrypt filepasswordhere (to decrypt your accounts.sacpy file)\n\t sac.py kill (to kill Steam)")
    sys.exit(1)

# Assign provided username to a variable
username = sys.argv[1]

# If username is "kill", kill Steam (not like anyone has the username of "kill" right???)
if username == "kill":
    kill_if_running()
    sys.exit(1)

# If the username is "encrypt", check the decrypted file exists, encrypt it and remove decrypted file
if username == "encrypt":
    accounts_file_exists(False)
    pw = sys.argv[2]
    encrypt_accounts_file(pw)
    clean_up()
    sys.exit(1)

# Check if the accounts file exists
accounts_file_exists(True)

# If the username is "encrypt", check the decrypted file exists, encrypt it and remove decrypted file
if username == "decrypt":
    accounts_file_exists(True)
    pw = sys.argv[2]
    decrypt_accounts_file(pw)
    print("You have just decrypted the accounts file, your login credentials are no longer protected!")
    sys.exit(1)

if len(sys.argv) < 3:
    print("[ERROR]: Provide a command/username and account file password")
    sys.exit(1)

### Beyond this point, we need the file to be decrypted ###
decrypt_accounts_file(sys.argv[2])

# Lists all the accounts in the file (does not show passwords)
if username == "list":
    list_accounts()

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

clean_up()
launch_steam(username,escape_string(password))
