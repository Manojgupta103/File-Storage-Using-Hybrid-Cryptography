import os
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import (
    AESCCM, AESGCM, ChaCha20Poly1305)
import tools

# Function to read plaintext data from files.
def readPlainText(filename) -> bytes:
    print(f"[INFO] Reading plaintext from 'files/{filename}'")
    source_filename = 'files/' + filename
    file = open(source_filename, 'rb')
    raw = b""
    for line in file:
        raw += line
    file.close()
    print(f"[DEBUG] Read raw data from '{filename}'.")
    return raw

# Write encrypted data to the target file.
def writeEncryptedText(filename, encryptedData: bytes):
    print(f"[INFO] Writing encrypted data to 'encrypted/{filename}'")
    target_filename = 'encrypted/' + filename
    target_file = open(target_filename, 'wb')
    target_file.write(encryptedData)
    target_file.close()
    print(f"[DEBUG] Encrypted data written for '{filename}'.")

# Write encrypted keys.
def writeEncryptedKeys(encryptedKeys: bytes):
    target_file = open("raw_data/store_in_me.enc", "wb")
    target_file.write(encryptedKeys)
    target_file.close()
    print("[DEBUG] Encrypted keys stored in 'raw_data/store_in_me.enc'.")

# Generate RSA key pairs.
def rsaKeyPairGeneration():
    print("[INFO] Generating RSA key pair.")
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    print("[DEBUG] RSA key pair generated successfully.")
    return {"private": private_key, "public": public_key}

# AES encryption using a single key.
def AESAlgo(data: bytes, key: bytes):
    print("[INFO] Encrypting data using AES.")
    f = Fernet(key)
    secret_data = f.encrypt(data)
    writeEncryptedKeys(secret_data)
    print("[DEBUG] AES encryption completed.")

# Encrypt using AES rotation with two keys.
def AESAlgoRotated(filename, key1: bytes, key2: bytes):
    print(f"[INFO] Encrypting file '{filename}' using rotated AES keys.")
    f = MultiFernet([Fernet(key1), Fernet(key2)])
    raw = readPlainText(filename)
    encryptedData = f.encrypt(raw)
    writeEncryptedText(filename, encryptedData)
    print(f"[DEBUG] Rotated AES encryption completed for '{filename}'.")

# Function for encryption with ChaCha20Poly1305.
def ChaChaAlgo(filename, key: bytes, nonce: bytes):
    print(f"[INFO] Encrypting file '{filename}' using ChaCha20Poly1305.")
    aad = b"authenticated but unencrypted data"
    chacha = ChaCha20Poly1305(key)
    raw = readPlainText(filename)
    encryptedData = chacha.encrypt(nonce, raw, aad)
    writeEncryptedText(filename, encryptedData)
    print(f"[DEBUG] ChaCha20Poly1305 encryption completed for '{filename}'.")

# Function for encryption with AESGCM.
def AESGCMAlgo(filename, key: bytes, nonce: bytes):
    print(f"[INFO] Encrypting file '{filename}' using AESGCM.")
    aad = b"authenticated but unencrypted data"
    aesgcm = AESGCM(key)
    raw = readPlainText(filename)
    encryptedData = aesgcm.encrypt(nonce, raw, aad)
    writeEncryptedText(filename, encryptedData)
    print(f"[DEBUG] AESGCM encryption completed for '{filename}'.")

# Function for encryption with AESCCM.
def AESCCMAlgo(filename, key: bytes, nonce: bytes):
    print(f"[INFO] Encrypting file '{filename}' using AESCCM.")
    aad = b"authenticated but unencrypted data"
    aesccm = AESCCM(key)
    raw = readPlainText(filename)
    encryptedData = aesccm.encrypt(nonce, raw, aad)
    writeEncryptedText(filename, encryptedData)
    print(f"[DEBUG] AESCCM encryption completed for '{filename}'.")

# Main encryption function.
def encrypter():
    print("[INFO] Starting encryption process.")
    tools.empty_folder('key')
    tools.empty_folder('encrypted')
    
    # Generate encryption keys.
    key_1 = Fernet.generate_key()
    key_1_1 = Fernet.generate_key()
    key_1_2 = Fernet.generate_key()
    key_2 = ChaCha20Poly1305.generate_key()
    key_3 = AESGCM.generate_key(bit_length=128)
    key_4 = AESCCM.generate_key(bit_length=128)
    nonce13 = os.urandom(13)
    nonce12 = os.urandom(12)

    print("[INFO] Encrypting files with different algorithms.")
    files = sorted(tools.list_dir('files'))
    for index, file in enumerate(files):
        print(f"[INFO] Encrypting file {index + 1} of {len(files)}: '{file}'")
        if index % 4 == 0:
            AESAlgoRotated(file, key_1_1, key_1_2)
        elif index % 4 == 1:
            ChaChaAlgo(file, key_2, nonce12)
        elif index % 4 == 2:
            AESGCMAlgo(file, key_3, nonce12)
        else:
            AESCCMAlgo(file, key_4, nonce13)
        print(f"[INFO] Encryption complete for '{file}'.")

    # Combine all secret information and encrypt it.
    secret_information = (key_1_1) + b":::::" + (key_1_2) + b":::::" + (key_2) + \
        b":::::" + (key_3) + b":::::" + (key_4) + b":::::" + (nonce12) + b":::::" + (nonce13)
    AESAlgo(secret_information, key_1)

    # Store the primary encryption key.
    with open("./key/Main_Key.pem", "wb") as public_key:
        public_key.write(key_1)
    print("[DEBUG] Main key stored in 'key/Main_Key.pem'.")
    tools.empty_folder('files')
    print("[INFO] Encryption process completed successfully.")
