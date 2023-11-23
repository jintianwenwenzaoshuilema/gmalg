# -*- coding: UTF-8 -*-

from typing import List

__all__ = ["ZUC"]

_S0 = bytes([
    0x3e, 0x72, 0x5b, 0x47, 0xca, 0xe0, 0x00, 0x33, 0x04, 0xd1, 0x54, 0x98, 0x09, 0xb9, 0x6d, 0xcb,
    0x7b, 0x1b, 0xf9, 0x32, 0xaf, 0x9d, 0x6a, 0xa5, 0xb8, 0x2d, 0xfc, 0x1d, 0x08, 0x53, 0x03, 0x90,
    0x4d, 0x4e, 0x84, 0x99, 0xe4, 0xce, 0xd9, 0x91, 0xdd, 0xb6, 0x85, 0x48, 0x8b, 0x29, 0x6e, 0xac,
    0xcd, 0xc1, 0xf8, 0x1e, 0x73, 0x43, 0x69, 0xc6, 0xb5, 0xbd, 0xfd, 0x39, 0x63, 0x20, 0xd4, 0x38,
    0x76, 0x7d, 0xb2, 0xa7, 0xcf, 0xed, 0x57, 0xc5, 0xf3, 0x2c, 0xbb, 0x14, 0x21, 0x06, 0x55, 0x9b,
    0xe3, 0xef, 0x5e, 0x31, 0x4f, 0x7f, 0x5a, 0xa4, 0x0d, 0x82, 0x51, 0x49, 0x5f, 0xba, 0x58, 0x1c,
    0x4a, 0x16, 0xd5, 0x17, 0xa8, 0x92, 0x24, 0x1f, 0x8c, 0xff, 0xd8, 0xae, 0x2e, 0x01, 0xd3, 0xad,
    0x3b, 0x4b, 0xda, 0x46, 0xeb, 0xc9, 0xde, 0x9a, 0x8f, 0x87, 0xd7, 0x3a, 0x80, 0x6f, 0x2f, 0xc8,
    0xb1, 0xb4, 0x37, 0xf7, 0x0a, 0x22, 0x13, 0x28, 0x7c, 0xcc, 0x3c, 0x89, 0xc7, 0xc3, 0x96, 0x56,
    0x07, 0xbf, 0x7e, 0xf0, 0x0b, 0x2b, 0x97, 0x52, 0x35, 0x41, 0x79, 0x61, 0xa6, 0x4c, 0x10, 0xfe,
    0xbc, 0x26, 0x95, 0x88, 0x8a, 0xb0, 0xa3, 0xfb, 0xc0, 0x18, 0x94, 0xf2, 0xe1, 0xe5, 0xe9, 0x5d,
    0xd0, 0xdc, 0x11, 0x66, 0x64, 0x5c, 0xec, 0x59, 0x42, 0x75, 0x12, 0xf5, 0x74, 0x9c, 0xaa, 0x23,
    0x0e, 0x86, 0xab, 0xbe, 0x2a, 0x02, 0xe7, 0x67, 0xe6, 0x44, 0xa2, 0x6c, 0xc2, 0x93, 0x9f, 0xf1,
    0xf6, 0xfa, 0x36, 0xd2, 0x50, 0x68, 0x9e, 0x62, 0x71, 0x15, 0x3d, 0xd6, 0x40, 0xc4, 0xe2, 0x0f,
    0x8e, 0x83, 0x77, 0x6b, 0x25, 0x05, 0x3f, 0x0c, 0x30, 0xea, 0x70, 0xb7, 0xa1, 0xe8, 0xa9, 0x65,
    0x8d, 0x27, 0x1a, 0xdb, 0x81, 0xb3, 0xa0, 0xf4, 0x45, 0x7a, 0x19, 0xdf, 0xee, 0x78, 0x34, 0x60
])

_S1 = bytes([
    0x55, 0xc2, 0x63, 0x71, 0x3b, 0xc8, 0x47, 0x86, 0x9f, 0x3c, 0xda, 0x5b, 0x29, 0xaa, 0xfd, 0x77,
    0x8c, 0xc5, 0x94, 0x0c, 0xa6, 0x1a, 0x13, 0x00, 0xe3, 0xa8, 0x16, 0x72, 0x40, 0xf9, 0xf8, 0x42,
    0x44, 0x26, 0x68, 0x96, 0x81, 0xd9, 0x45, 0x3e, 0x10, 0x76, 0xc6, 0xa7, 0x8b, 0x39, 0x43, 0xe1,
    0x3a, 0xb5, 0x56, 0x2a, 0xc0, 0x6d, 0xb3, 0x05, 0x22, 0x66, 0xbf, 0xdc, 0x0b, 0xfa, 0x62, 0x48,
    0xdd, 0x20, 0x11, 0x06, 0x36, 0xc9, 0xc1, 0xcf, 0xf6, 0x27, 0x52, 0xbb, 0x69, 0xf5, 0xd4, 0x87,
    0x7f, 0x84, 0x4c, 0xd2, 0x9c, 0x57, 0xa4, 0xbc, 0x4f, 0x9a, 0xdf, 0xfe, 0xd6, 0x8d, 0x7a, 0xeb,
    0x2b, 0x53, 0xd8, 0x5c, 0xa1, 0x14, 0x17, 0xfb, 0x23, 0xd5, 0x7d, 0x30, 0x67, 0x73, 0x08, 0x09,
    0xee, 0xb7, 0x70, 0x3f, 0x61, 0xb2, 0x19, 0x8e, 0x4e, 0xe5, 0x4b, 0x93, 0x8f, 0x5d, 0xdb, 0xa9,
    0xad, 0xf1, 0xae, 0x2e, 0xcb, 0x0d, 0xfc, 0xf4, 0x2d, 0x46, 0x6e, 0x1d, 0x97, 0xe8, 0xd1, 0xe9,
    0x4d, 0x37, 0xa5, 0x75, 0x5e, 0x83, 0x9e, 0xab, 0x82, 0x9d, 0xb9, 0x1c, 0xe0, 0xcd, 0x49, 0x89,
    0x01, 0xb6, 0xbd, 0x58, 0x24, 0xa2, 0x5f, 0x38, 0x78, 0x99, 0x15, 0x90, 0x50, 0xb8, 0x95, 0xe4,
    0xd0, 0x91, 0xc7, 0xce, 0xed, 0x0f, 0xb4, 0x6f, 0xa0, 0xcc, 0xf0, 0x02, 0x4a, 0x79, 0xc3, 0xde,
    0xa3, 0xef, 0xea, 0x51, 0xe6, 0x6b, 0x18, 0xec, 0x1b, 0x2c, 0x80, 0xf7, 0x74, 0xe7, 0xff, 0x21,
    0x5a, 0x6a, 0x54, 0x1e, 0x41, 0x31, 0x92, 0x35, 0xc4, 0x33, 0x07, 0x0a, 0xba, 0x7e, 0x0e, 0x34,
    0x88, 0xb1, 0x98, 0x7c, 0xf3, 0x3d, 0x60, 0x6c, 0x7b, 0xca, 0xd3, 0x1f, 0x32, 0x65, 0x04, 0x28,
    0x64, 0xbe, 0x85, 0x9b, 0x2f, 0x59, 0x8a, 0xd7, 0xb0, 0x25, 0xac, 0xaf, 0x12, 0x03, 0xe2, 0xf2
])

_D = [
    0b100010011010111, 0b010011010111100, 0b110001001101011, 0b001001101011110,
    0b101011110001001, 0b011010111100010, 0b111000100110101, 0b000100110101111,
    0b100110101111000, 0b010111100010011, 0b110101111000100, 0b001101011110001,
    0b101111000100110, 0b011110001001101, 0b111100010011010, 0b100011110101100
]


def _BS(X):
    return (
        (_S0[(X >> 24) & 0xff] << 24) ^
        (_S1[(X >> 16) & 0xff] << 16) ^
        (_S0[(X >> 8) & 0xff] << 8) ^
        (_S1[X & 0xff])
    )


def _ROL(X, count):
    count &= 0x1f
    return ((X << count) | (X >> (32 - count))) & 0xffffffff


def _L1(X):
    return X ^ _ROL(X, 2) ^ _ROL(X, 10) ^ _ROL(X, 18) ^ _ROL(X, 24)


def _L2(X):
    return X ^ _ROL(X, 8) ^ _ROL(X, 14) ^ _ROL(X, 22) ^ _ROL(X, 30)


class ZUC:
    """ZUC"""

    KEY_LEN = 16
    IV_LEN = 16

    def __init__(self, key: bytes, iv: bytes) -> None:
        if len(key) != ZUC.KEY_LEN:
            raise ValueError(f"Invalid key length {len(key)} bytes, key must be {ZUC.KEY_LEN} bytes.")
        if len(iv) != ZUC.IV_LEN:
            raise ValueError(f"Invalid iv length {len(iv)} bytes, iv must be {ZUC.IV_LEN} bytes.")

        self._key: bytes = key
        self._iv: bytes = iv

        self._lfsr: List[int] = [0] * 16
        self._R1 = 0
        self._R2 = 0

        self._init()

        # discard first word
        self.generate()

    def _lfsr_work(self, u: int = 0):
        S = self._lfsr
        s16 = (0x8000 * S[15] + 0x20000 * S[13] + 0x200000 * S[10] + 0x100000 * S[4] + 0x101 * S[0] + u) % 0x7fffffff
        S.append(0x7fffffff if s16 == 0 else s16)
        S.pop(0)

    def _F(self, X0: int, X1: int, X2: int) -> int:
        R1 = self._R1
        R2 = self._R2

        W = ((X0 ^ R1) + R2) & 0xffffffff
        W1 = (R1 + X1) & 0xffffffff
        W2 = R2 ^ X2

        self._R1 = _BS(_L1(((W1 & 0xffff) << 16) ^ (W2 >> 16)))
        self._R2 = _BS(_L2(((W2 & 0xffff) << 16) ^ (W1 >> 16)))

        return W

    def _init(self):
        S = self._lfsr

        # key expansion
        for i in range(16):
            S[i] = (self._key[i] << 23) | (_D[i] << 8) | (self._iv[i])

        # initalize
        for _ in range(32):
            X0 = (S[15] >> 15 << 16) | (S[14] & 0xffff)
            X1 = ((S[11] & 0xffff) << 16) | (S[9] >> 15)
            X2 = ((S[7] & 0xffff) << 16) | (S[5] >> 15)
            self._lfsr_work(self._F(X0, X1, X2) >> 1)

    def generate(self) -> int:
        """Generate pseudo-random words.

        Returns:
            int: a 32-bit pseudo-random word.
        """

        S = self._lfsr
        X0 = (S[15] >> 15 << 16) | (S[14] & 0xffff)
        X1 = ((S[11] & 0xffff) << 16) | (S[9] >> 15)
        X2 = ((S[7] & 0xffff) << 16) | (S[5] >> 15)
        X3 = ((S[2] & 0xffff) << 16) | (S[0] >> 15)

        Z = self._F(X0, X1, X2) ^ X3
        self._lfsr_work()

        return Z


class EEA3:
    """ZUC Confidentiality Algorithm"""


class EIA3:
    """ZUC Integrity Algorithm"""
