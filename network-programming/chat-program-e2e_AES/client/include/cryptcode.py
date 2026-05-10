import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

SALT_LENGTH = 16          # bytes
NONCE_LENGTH = 12         # 96 bits is standard for GCM
KEY_LENGTH = 32           # AES-256
PBKDF2_ITERATIONS = 100_000  # tuneable (higher = more secure but slower)

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from password + salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_message(plaintext: str, password: str, salt: bytes) -> bytes:
    """
    Encrypt a string. Returns nonce + ciphertext (with attached authentication tag).
    """
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_LENGTH)   # must be unique per message
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), associated_data=None)
    return nonce + ciphertext          # prepend nonce for the receiver

def decrypt_message(packet: bytes, password: str, salt: bytes) -> str:
    """
    Decrypt a packet (nonce + ciphertext). Raises InvalidTag if key is wrong.
    """
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = packet[:NONCE_LENGTH]
    ciphertext = packet[NONCE_LENGTH:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return plaintext.decode('utf-8')