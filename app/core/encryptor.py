import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from app.core.config import settings


class Encryptor:
    def __init__(self):
        self._algorithm = "AES-256-CBC"
        self._key = settings.encryptor_secret_key
        self._iv = os.urandom(16)

    def _to_buffer_32(self, key: str) -> bytes:
        """Ensures the key is exactly 32 bytes long."""
        key_bytes = key.encode("utf-8")
        return key_bytes[:32].ljust(32, b"\0")

    def encrypt(self, text: str, key: str = None) -> str:
        """Encrypts the text using AES-256-CBC."""
        key = self._to_buffer_32(key or self._key)
        cipher = AES.new(key, AES.MODE_CBC, self._iv)
        encrypted = cipher.encrypt(pad(text.encode("utf-8"), AES.block_size))
        return f"{base64.b64encode(self._iv).decode()}:{base64.b64encode(encrypted).decode()}"

    def decrypt(self, encrypted_text: str, key: str = None) -> str:
        """Decrypts the encrypted text."""
        try:
            key = self._to_buffer_32(key or self._key)
            iv_b64, encrypted_b64 = encrypted_text.split(":")
            iv = base64.b64decode(iv_b64)
            encrypted = base64.b64decode(encrypted_b64)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(encrypted), AES.block_size).decode("utf-8")
        except Exception:
            return ""

