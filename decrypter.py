from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives.ciphers.aead import (AESCCM, AESGCM, ChaCha20Poly1305)
import tools

# Function to read encrypted keys from the file.
def readEncryptedKeys():
    print("[INFO] Reading encrypted keys from 'raw_data/store_in_me.enc'")
    target_file = open("raw_data/store_in_me.enc", "rb")
    encryptedKeys = b""
    for line in target_file:
        encryptedKeys += line
    target_file.close()
    print("[DEBUG] Encrypted keys read successfully.")
    return encryptedKeys

# Function to read encrypted text from the specified file.
def readEncryptedText(filename):
    print(f"[INFO] Reading encrypted text from 'encrypted/{filename}'")
    source_filename = 'encrypted/' + filename
    file = open(source_filename, 'rb')
    encryptedText = b""
    for line in file:
        encryptedText += line
    file.close()
    print(f"[DEBUG] Encrypted text for '{filename}' read successfully.")
    return encryptedText

# Write the decrypted plaintext to the target file.
def writePlainText(filename, plainText):
    print(f"[INFO] Writing decrypted text to 'files/{filename}'")
    target_filename = 'files/' + filename
    target_file = open(target_filename, 'wb')
    target_file.write(plainText)
    target_file.close()
    print(f"[DEBUG] Plain text written successfully for '{filename}'")

# Perform AES decryption using a single key.
def AESAlgo(key):
    print("[INFO] Decrypting secret information using AES Algorithm.")
    f = Fernet(key)
    encryptedKeys = readEncryptedKeys()
    secret_data = f.decrypt(encryptedKeys)
    print("[DEBUG] AES decryption completed.")
    return secret_data

# Decrypt using AES rotation with two keys.
def AESAlgoRotated(filename, key1, key2):
    print(f"[INFO] Decrypting file '{filename}' using AES with rotated keys.")
    f = MultiFernet([Fernet(key1), Fernet(key2)])
    encryptedText = readEncryptedText(filename)
    plainText = f.decrypt(encryptedText)
    writePlainText(filename, plainText)
    print(f"[DEBUG] AES rotated decryption completed for '{filename}'")

# Function to decrypt using the ChaCha20Poly1305 algorithm.
def ChaChaAlgo(filename, key, nonce):
    print(f"[INFO] Decrypting file '{filename}' using ChaCha20Poly1305.")
    aad = b"authenticated but unencrypted data"
    chacha = ChaCha20Poly1305(key)
    encryptedText = readEncryptedText(filename)
    plainText = chacha.decrypt(nonce, encryptedText, aad)
    writePlainText(filename, plainText)
    print(f"[DEBUG] ChaCha20Poly1305 decryption completed for '{filename}'")

# Function to decrypt using the AESGCM algorithm.
def AESGCMAlgo(filename, key, nonce):
    print(f"[INFO] Decrypting file '{filename}' using AESGCM.")
    aad = b"authenticated but unencrypted data"
    aesgcm = AESGCM(key)
    encryptedText = readEncryptedText(filename)
    plainText = aesgcm.decrypt(nonce, encryptedText, aad)
    writePlainText(filename, plainText)
    print(f"[DEBUG] AESGCM decryption completed for '{filename}'")

# Function to decrypt using the AESCCM algorithm.
def AESCCMAlgo(filename, key, nonce):
    print(f"[INFO] Decrypting file '{filename}' using AESCCM.")
    aad = b"authenticated but unencrypted data"
    aesccm = AESCCM(key)
    encryptedText = readEncryptedText(filename)
    plainText = aesccm.decrypt(nonce, encryptedText, aad)
    writePlainText(filename, plainText)
    print(f"[DEBUG] AESCCM decryption completed for '{filename}'")

# Main decryption function.
def decrypter():
    print("[INFO] Starting decryption process.")
    tools.empty_folder('files')  # Clean the 'files' directory.
    key_1 = b""
    list_directory = tools.list_dir('key')
    filename = './key/' + list_directory[0]

    print(f"[INFO] Reading public key from '{filename}'")
    with open(filename, "rb") as public_key:
        for line in public_key:
            key_1 += line
    print("[DEBUG] Public key read successfully.")

    secret_information = AESAlgo(key_1)
    list_information = secret_information.split(b':::::')
    
    # Unpacking the keys and nonces
    key_1_1, key_1_2, key_2, key_3, key_4, nonce12, nonce13 = list_information[:7]
    
    files = sorted(tools.list_dir('encrypted'))
    print(f"[INFO] Found {len(files)} files to decrypt.")

    # Loop through each file and decrypt using appropriate algorithm.
    for index, file in enumerate(files):
        print(f"[INFO] Decrypting file {index + 1} of {len(files)}: '{file}'")
        if index % 4 == 0:
            AESAlgoRotated(file, key_1_1, key_1_2)
        elif index % 4 == 1:
            ChaChaAlgo(file, key_2, nonce12)
        elif index % 4 == 2:
            AESGCMAlgo(file, key_3, nonce12)
        else:
            AESCCMAlgo(file, key_4, nonce13)
        print(f"[INFO] Decryption complete for '{file}'.")

    print("[INFO] Decryption process completed successfully.")
