from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("backend/libs/funcs/secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("backend/libs/funcs/secret.key", "rb").read()

def ensure_key_exists():
    if not os.path.exists("backend/libs/funcs/secret.key"):
        generate_key()

def encrypt_message(message):
    ensure_key_exists()
    key = load_key()
    print(f"Key used for encryption: {key}")
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    print(f"Encrypted message: {encrypted_message}")
    return encrypted_message

def decrypt_message(encrypted_message):
    ensure_key_exists()
    key = load_key()
    print(f"Key used for decryption: {key}")
    print(f"Encrypted message before decryption: {encrypted_message}")
    f = Fernet(key)
    try:
        decrypted_message = f.decrypt(encrypted_message)
        print(f"Decrypted message: {decrypted_message.decode()}")
        return decrypted_message.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        raise

if __name__ == "__main__":
    pass