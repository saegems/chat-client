import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import zlib
from config.config import SECRET_KEY, INIT_VECTOR


def encrypt(value: str) -> str:
    try:
        if not SECRET_KEY or not INIT_VECTOR:
            raise ValueError("Secret key or init vector not initialized")

        iv = INIT_VECTOR.encode('utf-8')
        key = SECRET_KEY.encode('utf-8')

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        padding_length = 16 - (len(value) % 16)
        padded_value = value + chr(padding_length) * padding_length

        encrypted = encryptor.update(
            padded_value.encode('utf-8')) + encryptor.finalize()
        return base64.b64encode(encrypted).decode('utf-8')

    except Exception as ex:
        raise RuntimeError(f"Encryption error: {str(ex)}") from ex


def decrypt(encrypted: str) -> str:
    try:
        if not SECRET_KEY or not INIT_VECTOR:
            raise ValueError("Secret key or init vector not initialized")

        iv = INIT_VECTOR.encode('utf-8')
        key = SECRET_KEY.encode('utf-8')

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        encrypted_bytes = base64.b64decode(encrypted)
        decrypted_padded = decryptor.update(
            encrypted_bytes) + decryptor.finalize()

        padding_length = decrypted_padded[-1]
        decrypted = decrypted_padded[:-padding_length]

        return decrypted.decode('utf-8')

    except Exception as ex:
        raise RuntimeError(f"Decryption error: {str(ex)}") from ex


def compress(encrypted: str) -> str:
    try:
        input_bytes = encrypted.encode('utf-8')
        compressed = zlib.compress(input_bytes, level=6)
        compressed_string = base64.b64encode(compressed).decode('utf-8')

        if len(compressed_string) > 255:
            raise ValueError("Compressed string exceeds 255 characters")

        return compressed_string

    except Exception as ex:
        raise RuntimeError(f"Compression error: {str(ex)}") from ex


def decompress(compressed: str) -> str:
    try:
        compressed_bytes = base64.b64decode(compressed)
        decompressed = zlib.decompress(compressed_bytes)
        return decompressed.decode('utf-8')

    except Exception as ex:
        raise RuntimeError(f"Decompression error: {str(ex)}") from ex
