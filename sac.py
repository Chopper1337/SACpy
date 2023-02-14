import subprocess
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

if not os.path.exists('accounts.sacpy'):
    print("[ERROR]: The 'accounts.sacpy' file does not exist.")
    print("Create accounts.sacpy in this directory, containing account information like so:")
    print("username:password\nusername:password\n...")
    sys.exit(1)

if len(sys.argv) < 2:
    print("[ERROR]: Provide a username!")
    sys.exit(1)

username = sys.argv[1]

with open('accounts.sacpy', 'r') as f:
    for line in f:
        line = line.strip()
        args = line.split(':')
        if len(args) == 2 and args[0] == username:
            arg1 = args[0]
            arg2 = args[1]
            break
    else:
        print(f"[ERROR]: No matching account found in accounts.sacpy for the username: '{username}'")
        sys.exit(1)

proc = subprocess.Popen(["pgrep", "steam"], stdout=subprocess.PIPE)

# Kill process.
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

# Launch steam with login parameters and the matched arguments
steam_command = ("steam " + "-login " + arg1 + " " +  arg2 + " -console " + " & disown")
#subprocess.run(steam_command)
os.system(steam_command)
