import requests
from cryptography.fernet import Fernet

# Load the same key used by the receiver
with open("key.key", "rb") as f:
    key = f.read()
fernet = Fernet(key)

# Log message to send (you can change this)
log_data = "Keylogger test message: User pressed CTRL + C"

# Encrypt the message
encrypted_data = fernet.encrypt(log_data.encode())

# Send the encrypted message via POST
url = "http://127.0.0.1:5000/upload"
response = requests.post(url, data=encrypted_data)

# Print server response
print("Status Code:", response.status_code)
print("Server Response:", response.text)
