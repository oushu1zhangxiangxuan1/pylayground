# crypto_utils.py
from cryptography.fernet import Fernet

def encrypt_message(message, key):
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()


def main():
    key = Fernet.generate_key()
    message = "Secret Message"
    encrypted_message = encrypt_message(message, key)
    print(f"Encrypted: {encrypted_message}")

    decrypted_message = decrypt_message(encrypted_message, key)
    print(f"Decrypted: {decrypted_message}")

if __name__ == "__main__":
    main()
