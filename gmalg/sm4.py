"""SM4 Algorithm Implementation Module."""

import os
from typing import Optional
from typing import List

from .base import BlockCipher
from .errors import *
from .utils import ROL32

__all__ = ["SM4"]

_S_BOX = bytes([
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
])

_CK = [
    0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269, 0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
    0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249, 0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
    0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229, 0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
    0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209, 0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279
]


def _BS(X):
    return ((_S_BOX[(X >> 24) & 0xff] << 24) |
            (_S_BOX[(X >> 16) & 0xff] << 16) |
            (_S_BOX[(X >> 8) & 0xff] << 8) |
            (_S_BOX[X & 0xff]))


def _T0(X):
    X = _BS(X)
    return X ^ ROL32(X, 2) ^ ROL32(X, 10) ^ ROL32(X, 18) ^ ROL32(X, 24)


def _T1(X):
    X = _BS(X)
    return X ^ ROL32(X, 13) ^ ROL32(X, 23)


def _key_expand(key: bytes, rkey: List[int]):
    """Key expansion."""

    K0 = int.from_bytes(key[0:4], "big") ^ 0xa3b1bac6
    K1 = int.from_bytes(key[4:8], "big") ^ 0x56aa3350
    K2 = int.from_bytes(key[8:12], "big") ^ 0x677d9197
    K3 = int.from_bytes(key[12:16], "big") ^ 0xb27022dc

    for i in range(0, 32, 4):
        K0 = K0 ^ _T1(K1 ^ K2 ^ K3 ^ _CK[i])
        rkey[i] = K0
        K1 = K1 ^ _T1(K2 ^ K3 ^ K0 ^ _CK[i + 1])
        rkey[i + 1] = K1
        K2 = K2 ^ _T1(K3 ^ K0 ^ K1 ^ _CK[i + 2])
        rkey[i + 2] = K2
        K3 = K3 ^ _T1(K0 ^ K1 ^ K2 ^ _CK[i + 3])
        rkey[i + 3] = K3


class SM4(BlockCipher):
    """SM4 Algorithm."""

    @classmethod
    def key_length(self) -> int:
        """Get key length in bytes."""

        return 16

    @classmethod
    def block_length(self) -> int:
        """Get block length in bytes."""

        return 16

    def __init__(self, key: bytes) -> None:
        """SM4 Algorithm.

        Args:
            key: 16 bytes key.

        Raises:
            IncorrectLengthError: Incorrect key length.
        """

        if len(key) != self.key_length():
            raise IncorrectLengthError(
                "Key", f"{self.key_length()} bytes", f"{len(key)} bytes")

        self._key: bytes = key
        self._rkey: List[int] = [0] * 32
        _key_expand(self._key, self._rkey)

        self._block_buffer = bytearray()

    def encrypt(self, block: bytes) -> bytes:
        """Encrypt.

        Args:
            block: Plain block to encrypt, must be 16 bytes.

        Returns:
            bytes: 16 bytes cipher block.

        Raises:
            IncorrectLengthError: Incorrect block length.
        """

        if len(block) != self.block_length():
            raise IncorrectLengthError(
                "Block", f"{self.block_length()} bytes", f"{len(block)} bytes")

        RK = self._rkey

        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")

        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[i])
            X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
            X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[i + 2])
            X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[i + 3])

        BUFFER = self._block_buffer
        BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, "big"))
        BUFFER.extend(X2.to_bytes(4, "big"))
        BUFFER.extend(X1.to_bytes(4, "big"))
        BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)

    def decrypt(self, block: bytes) -> bytes:
        """Decrypt.

        Args:
            block: cipher block to decrypt, must be 16 bytes.

        Returns:
            bytes: 16 bytes plain block.

        Raises:
            IncorrectLengthError: Incorrect block length.
        """

        if len(block) != self.block_length():
            raise IncorrectLengthError(
                "Block", f"{self.block_length()} bytes", f"{len(block)} bytes")

        RK = self._rkey

        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")

        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[31 - i])
            X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[29 - i])
            X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[28 - i])

        BUFFER = self._block_buffer
        BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, "big"))
        BUFFER.extend(X2.to_bytes(4, "big"))
        BUFFER.extend(X1.to_bytes(4, "big"))
        BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)


class SM4_CBC(SM4):
    """SM4 CBC Mode Algorithm."""

    def __init__(self, key: bytes, iv: Optional[bytes] = None) -> None:
        """SM4 CBC Mode.

        Args:
            key: 16 bytes key.
            iv: 16 bytes initialization vector (IV), defaults to random if None.

        Raises:
            IncorrectLengthError: Incorrect key or IV length.
        """
        super().__init__(key)

        if iv is None:
            # Generate a random IV if not provided
            self._iv = os.urandom(self.block_length())
        else:
            if len(iv) != self.block_length():
                raise IncorrectLengthError(
                    "IV", f"{self.block_length()} bytes", f"{len(iv)} bytes")
            self._iv = iv

        self._previous_cipher_block = self._iv

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using SM4 CBC mode.

        Args:
            data: Data to encrypt. Must be a multiple of the block size.

        Returns:
            bytes: Encrypted data.
        """
        # Pad the data to make it a multiple of the block size (16 bytes)
        data = self._pad(data)

        cipher_text = bytearray()
        # Process each 16-byte block
        for i in range(0, len(data), self.block_length()):
            block = data[i:i + self.block_length()]
            # XOR with the previous cipher block (for CBC mode)
            block = bytes(a ^ b for a, b in zip(
                block, self._previous_cipher_block))
            encrypted_block = super().encrypt(block)
            cipher_text.extend(encrypted_block)

            # Update the previous cipher block to the current encrypted block
            self._previous_cipher_block = encrypted_block

        return bytes(cipher_text)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data using SM4 CBC mode.

        Args:
            data: Encrypted data to decrypt. Must be a multiple of the block size.

        Returns:
            bytes: Decrypted data.
        """
        # Decrypt in blocks and remove padding
        decrypted_data = bytearray()
        for i in range(0, len(data), self.block_length()):
            block = data[i:i + self.block_length()]
            decrypted_block = super().decrypt(block)

            # XOR with the previous cipher block to get the original plaintext
            decrypted_block = bytes(a ^ b for a, b in zip(
                decrypted_block, self._previous_cipher_block))
            decrypted_data.extend(decrypted_block)

            # Update the previous cipher block to the current encrypted block
            self._previous_cipher_block = block

        # Remove padding
        return self._unpad(decrypted_data)

    def _pad(self, data: bytes) -> bytes:
        """Pad data to a multiple of the block size (16 bytes)."""
        padding_length = self.block_length() - len(data) % self.block_length()
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad(self, data: bytes) -> bytes:
        """Remove padding from decrypted data."""
        padding_length = data[-1]
        return data[:-padding_length]



class SM4_ECB(SM4):
    """SM4 ECB Mode Algorithm."""

    def __init__(self, key: bytes) -> None:
        """SM4 ECB Mode.

        Args:
            key: 16 bytes key.

        Raises:
            IncorrectLengthError: Incorrect key length.
        """
        super().__init__(key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using SM4 ECB mode.

        Args:
            data: Data to encrypt. Must be a multiple of the block size.

        Returns:
            bytes: Encrypted data.
        """
        # Pad the data to make it a multiple of the block size (16 bytes)
        data = self._pad(data)

        cipher_text = bytearray()
        # Process each 16-byte block
        for i in range(0, len(data), self.block_length()):
            block = data[i:i + self.block_length()]
            encrypted_block = super().encrypt(block)
            cipher_text.extend(encrypted_block)

        return bytes(cipher_text)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data using SM4 ECB mode.

        Args:
            data: Encrypted data to decrypt. Must be a multiple of the block size.

        Returns:
            bytes: Decrypted data.
        """
        # Decrypt in blocks
        decrypted_data = bytearray()
        for i in range(0, len(data), self.block_length()):
            block = data[i:i + self.block_length()]
            decrypted_block = super().decrypt(block)
            decrypted_data.extend(decrypted_block)

        # Remove padding
        return self._unpad(decrypted_data)

    def _pad(self, data: bytes) -> bytes:
        """Pad data to a multiple of the block size (16 bytes)."""
        padding_length = self.block_length() - len(data) % self.block_length()
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad(self, data: bytes) -> bytes:
        """Remove padding from decrypted data."""
        padding_length = data[-1]
        return data[:-padding_length]
    
    
class SM4_CFB(SM4):
    """SM4 CFB (Cipher Feedback Mode)."""

    def __init__(self, key: bytes, iv: Optional[bytes] = None):
        """
        Initialize CFB mode.
        :param key: 16-byte encryption key.
        :param iv: 16-byte initialization vector (IV), randomly generated if not provided.
        """
        super().__init__(key)
        if iv and len(iv) != 16:
            raise ValueError("IV must be exactly 16 bytes long.")
        self.iv = iv or os.urandom(16)  # Ensure IV exists.

    def pad(self, data: bytes) -> bytes:
        """
        Apply PKCS7 padding to ensure data is a multiple of 16 bytes.
        :param data: Input data.
        :return: Padded data.
        """
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    def unpad(self, data: bytes) -> bytes:
        """
        Remove PKCS7 padding.
        :param data: Padded input data.
        :return: Unpadded data.
        """
        padding_length = data[-1]
        if padding_length > 16 or padding_length == 0:
            raise ValueError("Invalid padding detected.")
        return data[:-padding_length]

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt using CFB mode.
        :param plaintext: Data to encrypt.
        :return: IV + encrypted data.
        """
        plaintext = self.pad(plaintext)  # Ensure the length is a multiple of 16 bytes.
        ciphertext = b""
        iv = self.iv  # Initial IV

        for i in range(0, len(plaintext), 16):
            iv_encrypted = self.encrypt_block(iv)  # Encrypt IV to generate keystream.
            encrypted_block = bytes(a ^ b for a, b in zip(iv_encrypted, plaintext[i:i+16]))  
            ciphertext += encrypted_block
            iv = encrypted_block  # Use current ciphertext block as IV for next iteration.

        return self.iv + ciphertext  # Prepend IV to ciphertext for proper decryption.

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt using CFB mode.
        :param ciphertext: Data to decrypt (first 16 bytes are IV).
        :return: Decrypted plaintext.
        """
        if len(ciphertext) < 16:
            raise ValueError("Ciphertext must be at least 16 bytes long.")

        iv, ciphertext = ciphertext[:16], ciphertext[16:]  # Extract IV.
        plaintext = b""

        for i in range(0, len(ciphertext), 16):
            iv_encrypted = self.encrypt_block(iv)  # Encrypt IV to generate keystream.
            decrypted_block = bytes(a ^ b for a, b in zip(iv_encrypted, ciphertext[i:i+16]))  
            plaintext += decrypted_block
            iv = ciphertext[i:i+16]  # Use current ciphertext block as IV for next iteration.

        return self.unpad(plaintext)  # Remove padding before returning.

    def encrypt_hex(self, plaintext: str) -> str:
        """
        Encrypt plaintext and return the result as a hex string.
        :param plaintext: Plaintext to encrypt (string).
        :return: Hex-encoded ciphertext.
        """
        encrypted_bytes = self.encrypt(plaintext.encode())
        return encrypted_bytes.hex()

    def decrypt_hex(self, ciphertext_hex: str) -> str:
        """
        Decrypt a hex-encoded ciphertext.
        :param ciphertext_hex: Hex string of encrypted data.
        :return: Decrypted plaintext.
        """
        encrypted_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_bytes = self.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()

    def display_info(self):
        """Print the current key and IV in hex format."""
        print(f"Key: {self.key.hex()}")
        print(f"IV:  {self.iv.hex()}")
        
        
class SM4_OFB(SM4):
    """SM4 OFB (Output Feedback Mode)."""

    def __init__(self, key: bytes, iv: Optional[bytes] = None):
        """
        Initialize OFB mode.
        :param key: 16-byte encryption key.
        :param iv: 16-byte initialization vector (IV), randomly generated if not provided.
        """
        super().__init__(key)
        if iv and len(iv) != 16:
            raise ValueError("IV must be exactly 16 bytes long.")
        self.iv = iv or os.urandom(16)  # Ensure IV exists.

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt using OFB mode.
        :param plaintext: Data to encrypt.
        :return: IV + encrypted data.
        """
        ciphertext = b""
        keystream = self.iv  # Initial keystream (IV)

        for i in range(0, len(plaintext), 16):
            keystream = self.encrypt_block(keystream)  # Encrypt the previous keystream.
            block = bytes(a ^ b for a, b in zip(keystream, plaintext[i:i+16]))
            ciphertext += block

        return self.iv + ciphertext  # Prepend IV to ciphertext for decryption.

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt using OFB mode.
        :param ciphertext: Data to decrypt (first 16 bytes are IV).
        :return: Decrypted plaintext.
        """
        if len(ciphertext) < 16:
            raise ValueError("Ciphertext must be at least 16 bytes long.")

        iv, ciphertext = ciphertext[:16], ciphertext[16:]  # Extract IV.
        plaintext = b""
        keystream = iv  # Initial keystream (IV)

        for i in range(0, len(ciphertext), 16):
            keystream = self.encrypt_block(keystream)  # Encrypt the previous keystream.
            block = bytes(a ^ b for a, b in zip(keystream, ciphertext[i:i+16]))
            plaintext += block

        return plaintext  # OFB does not require padding/unpadding.

    def encrypt_hex(self, plaintext: str) -> str:
        """
        Encrypt plaintext and return the result as a hex string.
        :param plaintext: Plaintext to encrypt (string).
        :return: Hex-encoded ciphertext.
        """
        encrypted_bytes = self.encrypt(plaintext.encode())
        return encrypted_bytes.hex()

    def decrypt_hex(self, ciphertext_hex: str) -> str:
        """
        Decrypt a hex-encoded ciphertext.
        :param ciphertext_hex: Hex string of encrypted data.
        :return: Decrypted plaintext.
        """
        encrypted_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_bytes = self.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()

    def display_info(self):
        """Print the current key and IV in hex format."""
        print(f"Key: {self.key.hex()}")
        print(f"IV:  {self.iv.hex()}")
        
