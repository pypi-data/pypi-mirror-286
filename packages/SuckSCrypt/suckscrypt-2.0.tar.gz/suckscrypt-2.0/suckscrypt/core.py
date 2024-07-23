import numpy as np
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import scrypt

def generate_key():
    """Generate a key and salt for encryption."""
    password = get_random_bytes(8)
    salt = get_random_bytes(16)
    key = scrypt(password, salt, 32, N=2**14, r=8, p=1)
    return key, salt

def generate_key_stream(key, nonce, length):
    """Generate a key stream using ChaCha20."""
    cipher = ChaCha20.new(key=key, nonce=nonce)
    key_stream = cipher.encrypt(bytes(length))
    return np.frombuffer(key_stream, dtype=np.uint8)

def sucks_encrypt(key, plaintext):
    """Encrypt plaintext using XOR with a generated key stream."""
    key_len = len(key)
    plaintext_len = len(plaintext)
    
    nonce = get_random_bytes(8)
    key_stream = generate_key_stream(key, nonce, plaintext_len)
    
    plaintext_array = np.frombuffer(plaintext, dtype=np.uint8)
    encrypted_array = np.bitwise_xor(plaintext_array, key_stream)
    
    return nonce + encrypted_array.tobytes()

def sucks_decrypt(key, encrypted_data):
    """Decrypt encrypted data using XOR with a generated key stream."""
    nonce = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    
    key_stream = generate_key_stream(key, nonce, len(ciphertext))
    plaintext_array = np.bitwise_xor(np.frombuffer(ciphertext, dtype=np.uint8), key_stream)
    
    return plaintext_array.tobytes()