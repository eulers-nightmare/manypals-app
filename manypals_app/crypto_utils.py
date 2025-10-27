from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

# Generate encryption key once and reuse it
def get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

def encrypt_message(text: str) -> str:
    f = Fernet(get_key())
    return f.encrypt(text.encode()).decode()

def decrypt_message(token: str) -> str:
    f = Fernet(get_key())
    return f.decrypt(token.encode()).decode()
