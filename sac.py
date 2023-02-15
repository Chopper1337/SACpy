import subprocess
import psutil
import signal
import time
import sys
import os

# TODO:
# * Encode/Decode or Encryption/Decryption of passwords
# * Cleaner "steam_command"
# * Kill Steam process
# * Use of functions
# * Check if Steam is running

def steam_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "steam":
            return True
    return False

# Kills the Steam process
def KillSteam():
    print("Killing Steam process...")
    proc = subprocess.Popen(["pgrep", "steam"], stdout=subprocess.PIPE)
    for pid in proc.stdout:
        os.system("notify-send \"Killing Steam\"")
        os.kill(int(pid), signal.SIGTERM)
        # Check if the process that we killed is alive.
        try:
            os.kill(int(pid), 0)
            raise Exception("""wasn't able to kill the process
            HINT:use signal.SIGKILL or signal.SIGABORT""")
        except OSError as ex:
            continue

        # Wait for Steam to terminate !!
        time.sleep(8)


# Check for username or command (kill) being provided
if len(sys.argv) < 2:
    print("[ERROR]: Provide a username or command!")
    print("Example: sac.py username\n\t sac.py kill")
    sys.exit(1)

# Assign provided username to a variable
username = sys.argv[1]

# If username is "kill", kill Steam (not like anyone has the username of "kill" right???)
if username == "kill":
    KillSteam()
    sys.exit(1)

# Check for existence of "accounts.sacpy"
if not os.path.exists('accounts.sacpy'):
    print("[ERROR]: The 'accounts.sacpy' file does not exist.")
    print("Create accounts.sacpy in this directory, containing account information like so:")
    print("username:password\nusername:password\n...")
    sys.exit(1)

# Open accounts file, read each line, split it by ":" and check if the username matches our provided username
# If it matches, let the second arg be our password. Else print error saying account not found.
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
if(steam_running()):
    KillSteam()
else:
    os.system(steam_command)
