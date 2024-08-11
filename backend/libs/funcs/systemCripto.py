from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("backend/libs/funcs/secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("backend/libs/funcs/secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

if __name__ == '__main__':
    generate_key()

    message = "Minha mensagem secreta"
    encrypted = encrypt_message(message)
    print(f"Mensagem Criptografada: {encrypted}")

    decrypted = decrypt_message(encrypted)
    print(f"Mensagem Descriptografada: {decrypted}")