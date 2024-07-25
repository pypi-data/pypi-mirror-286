import zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_ecb(key, plaintext):
    """Compresses plaintext, then encrypts using ECB mode (no IV) and the given key."""
    key = key.encode()

    # Compress plaintext
    compressed_plaintext = zlib.compress(plaintext.encode())

    # Padding is applied after compression
    padded_plaintext = _pad_text(compressed_plaintext)

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext_base64


def decrypt_ecb(key, ciphertext_base64):
    """Decrypts ciphertext using ECB mode (no IV) and the given key, then decompresses."""
    key = key.encode()

    ciphertext = base64.b64decode(ciphertext_base64)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad after decryption, then decompress
    compressed_plaintext = _unpad_text(padded_plaintext)
    plaintext = zlib.decompress(compressed_plaintext)

    return plaintext.decode()

# Padding functions 
def _pad_text(text):
    """Pads text (bytes) to a multiple of 16 bytes using PKCS#7 padding."""
    pad_length = 16 - (len(text) % 16)
    return text + bytes([pad_length]) * pad_length

def _unpad_text(text):
    """Removes PKCS#7 padding from text (bytes)."""
    pad_length = text[-1]
    return text[:-pad_length]

def get_checksum(key:str)->int:
    # Convert last two characters of key to integer
    return int(key[-2:], 16)