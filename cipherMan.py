import os
import base64
import getpass
import argparse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Function to generate encryption key from password
def generate_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

# Encrypt file
def encrypt_file(filepath: str, password: bytes):
    # Generate salt for encryption
    salt = os.urandom(16)  # Random salt for encryption
    encryption_key = generate_key(password, salt)

    # Encrypt the file
    with open(filepath, 'rb') as f:
        plaintext = f.read()
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(filepath + ".xo", 'wb') as f:
        f.write(iv + ciphertext)

    os.remove(filepath)

# Decrypt file
def decrypt_file(filepath: str, password: bytes):
    with open(filepath, 'rb') as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    # Use the password for decryption
    encryption_key = generate_key(password, password)  # Using password itself as salt for decryption

    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        original_filepath = filepath[:-3]
        with open(original_filepath, 'wb') as f:
            f.write(plaintext)

        os.remove(filepath)
    except Exception as e:
        print(f"Error: {e}. Incorrect password or corrupted file.")
        return False  # Return False if decryption fails

    return True

# Function to ask the user to re-enter the password
def get_password(prompt="Enter password: "):
    while True:
        password = getpass.getpass(prompt)
        confirm_password = getpass.getpass("Re-enter password: ")
        if password == confirm_password:
            return password.encode()
        else:
            print("Passwords do not match. Please try again.")

# Main function to handle the command line logic
def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files in a specified directory.")
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help="Choose 'encrypt' or 'decrypt'.")
    parser.add_argument('--dir', required=True, help="Path to the directory containing files to process.")
    args = parser.parse_args()

    # Verify the provided directory exists
    directory = args.dir
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    password = get_password("Enter password for encryption/decryption: ")

    # Process files in the specified directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if args.mode == 'encrypt' and not filename.endswith('.xo'):
                print(f"Encrypting {filename}...")
                encrypt_file(filepath, password)
            elif args.mode == 'decrypt' and filename.endswith('.xo'):
                print(f"Decrypting {filename}...")
                success = False
                while not success:
                    success = decrypt_file(filepath, password)
                    if not success:
                        print("Incorrect password. Please try again.")
                        password = get_password("Re-enter password for decryption: ")

if __name__ == "__main__":
    main()
