import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ENCRYPTION_KEY = base64.b64decode(os.getenv("ENCRYPTION_KEY"))


def encryptFile(contents: bytes) -> bytes:
    aesgcm = AESGCM(ENCRYPTION_KEY)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, contents, None)
    return nonce + ciphertext

def decryptFile(encrypted_contents: bytes) -> bytes:
    aesgcm = AESGCM(ENCRYPTION_KEY)
    nonce = encrypted_contents[:12]
    ciphertext = encrypted_contents[12:]
    return aesgcm.decrypt(
        nonce,
        ciphertext,
        None
    )