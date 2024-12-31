from cryptography.fernet import Fernet
import os
import base64
from hashlib import sha256

def generate_key(password: str) -> bytes:
    """
    Generate a Fernet key from a password.
    Fernet requires a URL-safe Base64-encoded 32-byte key.
    """
   
    key = sha256(password.encode()).digest() 
    return base64.urlsafe_b64encode(key) 

def encrypt_file(file_path: str, password: str):
    """
    Encrypt a file using a password.
    """
    key = generate_key(password)
    cipher = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            data = file.read()  
        encrypted_data = cipher.encrypt(data)  
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)  
        os.remove(file_path)  
        print(f"File {file_path} encrypted successfully as {encrypted_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decrypt_file(file_path: str, password: str):
    """
    Decrypt a file using a password.
    """
    key = generate_key(password)
    cipher = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()  
        decrypted_data = cipher.decrypt(encrypted_data)  
        decrypted_file_path = file_path.replace('.enc', '')  
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)  
        os.remove(file_path)  
        print(f"File {file_path} decrypted successfully as {decrypted_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("File Encryptor/Decryptor")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt a file? ").strip().upper()
    if choice in ['E', 'D']:
        file_path = input("Enter the file path: ").strip()
        password = input("Enter the password: ").strip()
        if choice == 'E':
            encrypt_file(file_path, password)
        elif choice == 'D':
            decrypt_file(file_path, password)
    else:
        print("Invalid choice. Exiting.")