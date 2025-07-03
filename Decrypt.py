from cryptography.fernet import Fernet

with open("key.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

with open("keylog.txt", "r") as f:
    for line in f:
        decrypted = fernet.decrypt(line.strip().encode()).decode()
        print(decrypted)
