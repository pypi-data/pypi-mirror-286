import os
from typing import Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def decrypt_aes256(encrypted_data: bytes, key: bytes, iv: Optional[bytes] = None) -> str:
    #ToDo Improve description
    """
    Decrypts the encrypted data with the provided key.
    
    You could also use an iv, but if you don't it will be taken the default one. The default iv are 16 zero bytes.
    key: 32 bytes long
    iv:  16 bytes long
    """
    # Check key length for AES-256
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long for AES-256.")
    
    # If IV is not provided, use a default one (here it's assumed to be 16 bytes for AES)
    if iv is None:
        iv = b'\x00' * 16
    elif len(iv) != 16:
        raise ValueError("IV must be 16 bytes long.")
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    # Convert bytes to string and return
    return unpadded_data.decode('utf-8')

def encrypt_aes256(plaintext: str, key: bytes, iv: Optional[bytes] = None) -> tuple[bytes, bytes]:
    """
    Encrypts the plaintext with the provided key.

    You could also use an iv, but if you don't it will be taken the default one. The default iv value is random chosen.
    key: 32 bytes long
    iv:  16 bytes long
    """
    # Check key length for AES-256
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long for AES-256.")
    
    # If IV is not provided, generate a random 16-byte IV
    if iv is None:
        iv = os.urandom(16)
    elif len(iv) != 16:
        raise ValueError("IV must be 16 bytes long.")
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the plaintext to be compatible with AES block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
    
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return the IV concatenated with the encrypted data (common practice)
    return iv, encrypted_data