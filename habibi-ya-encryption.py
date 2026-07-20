import os
import base64 as b64
from pathlib import path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key():
   
    raw_key= os.urandom(32)
    base64_key= b64.b64encode(raw_key).decode('utf-8')
    print("\n" + "="*50)
    print("YOUR AES-256 KEY (Write this down on paper): ")
    print(base64_key)
    print("="*50 + "\n")
    return base64_key

def encrypt_file(file_path, base64_key):
  
    path= path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

  
    try:
        key = b64.b64decode(base64_key.encode('utf-8'))
        aesgcm = AESGCM(key)
    except Exception:
        print("Error: Invalid Key format.")
        return

    
    data= path.read_bytes()
    iv = os.urandom(12)
    encrypted_data = aesgcm.encrypt(iv, data, None)
    path.write_bytes(iv + encrypted_data)
    print(f"Success: '{file_path}' has been encrypted.")

def decrypt_file(file_path, base64_key):

    path= path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        key = b64.b64decode(base64_key.encode('utf-8'))
        aesgcm = AESGCM(key)
    except Exception:
        print("Error: Invalid Key format.")
        return

    raw_data = path.read_bytes()
    iv = raw_data[:12]
    ciphertext = raw_data[12:]

    try:
        decrypted_data = aesgcm.decrypt(iv, ciphertext, None)
        path.write_bytes(decrypted_data)
        print(f"Success: '{file_path}' has been decrypted.")
    except Exception:
        print("Decryption Failed Either the key is incorrect or the file has been tampered with.")

def main():
    print("--- Habibi ya encryption (AES-256 GCM) ---")
    print("1. Generate a new key")
    print("2. Encrypt a file")
    print("3. Decrypt a file")
    
    choice = input("Select an option (1/2/3): ").strip()
    
    if choice == '1':
        generate_key()
    elif choice in ('2', '3'):
        file_path = input("Enter the path to the file: ").strip('" ')
        key = input("Enter your Base64 Key: ").strip()
        
        if choice == '2':
            encrypt_file(file_path, key)
        else:
            decrypt_file(file_path, key)
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()