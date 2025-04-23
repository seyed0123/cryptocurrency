from typing import List
import sympy  # use this or other modules for generating required prime numbers
from typing import Tuple,Optional
import random
from math import ceil
import secrets
import sys
class AES:
    # =============================================================================
    #                            AES CONSTANTS
    # =============================================================================

    #: S-Box for SubBytes (encryption)
    S_BOX = [
        0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
        0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
        0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
        0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
        0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
        0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
        0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
        0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
        0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
        0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
        0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
        0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
        0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
        0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
        0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
        0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
    ]

    #: Inverse S-Box for InvSubBytes (decryption)
    INV_S_BOX = [
        0x52,0x09,0x6A,0xD5,0x30,0x36,0xA5,0x38,0xBF,0x40,0xA3,0x9E,0x81,0xF3,0xD7,0xFB,
        0x7C,0xE3,0x39,0x82,0x9B,0x2F,0xFF,0x87,0x34,0x8E,0x43,0x44,0xC4,0xDE,0xE9,0xCB,
        0x54,0x7B,0x94,0x32,0xA6,0xC2,0x23,0x3D,0xEE,0x4C,0x95,0x0B,0x42,0xFA,0xC3,0x4E,
        0x08,0x2E,0xA1,0x66,0x28,0xD9,0x24,0xB2,0x76,0x5B,0xA2,0x49,0x6D,0x8B,0xD1,0x25,
        0x72,0xF8,0xF6,0x64,0x86,0x68,0x98,0x16,0xD4,0xA4,0x5C,0xCC,0x5D,0x65,0xB6,0x92,
        0x6C,0x70,0x48,0x50,0xFD,0xED,0xB9,0xDA,0x5E,0x15,0x46,0x57,0xA7,0x8D,0x9D,0x84,
        0x90,0xD8,0xAB,0x00,0x8C,0xBC,0xD3,0x0A,0xF7,0xE4,0x58,0x05,0xB8,0xB3,0x45,0x06,
        0xD0,0x2C,0x1E,0x8F,0xCA,0x3F,0x0F,0x02,0xC1,0xAF,0xBD,0x03,0x01,0x13,0x8A,0x6B,
        0x3A,0x91,0x11,0x41,0x4F,0x67,0xDC,0xEA,0x97,0xF2,0xCF,0xCE,0xF0,0xB4,0xE6,0x73,
        0x96,0xAC,0x74,0x22,0xE7,0xAD,0x35,0x85,0xE2,0xF9,0x37,0xE8,0x1C,0x75,0xDF,0x6E,
        0x47,0xF1,0x1A,0x71,0x1D,0x29,0xC5,0x89,0x6F,0xB7,0x62,0x0E,0xAA,0x18,0xBE,0x1B,
        0xFC,0x56,0x3E,0x4B,0xC6,0xD2,0x79,0x20,0x9A,0xDB,0xC0,0xFE,0x78,0xCD,0x5A,0xF4,
        0x1F,0xDD,0xA8,0x33,0x88,0x07,0xC7,0x31,0xB1,0x12,0x10,0x59,0x27,0x80,0xEC,0x5F,
        0x60,0x51,0x7F,0xA9,0x19,0xB5,0x4A,0x0D,0x2D,0xE5,0x7A,0x9F,0x93,0xC9,0x9C,0xEF,
        0xA0,0xE0,0x3B,0x4D,0xAE,0x2A,0xF5,0xB0,0xC8,0xEB,0xBB,0x3C,0x83,0x53,0x99,0x61,
        0x17,0x2B,0x04,0x7E,0xBA,0x77,0xD6,0x26,0xE1,0x69,0x14,0x63,0x55,0x21,0x0C,0x7D
    ]

    #: Round constant for Key Expansion
    RCON = [
        0x00000000,
        0x01000000,
        0x02000000,
        0x04000000,
        0x08000000,
        0x10000000,
        0x20000000,
        0x40000000,
        0x80000000,
        0x1b000000,
        0x36000000,
        0x6c000000,
        0xd8000000,
        0xab000000,
        0x4d000000,
        0x9a000000
    ]

    #: Number of columns (Nb) is always 4 for AES
    NB = 4

    # Key lengths -> (Nk, Nr) mapping
    # Nk = Number of 32-bit words in key, Nr = Number of rounds
    KEY_SIZES = {
        16: (4, 10),  # 128-bit
        24: (6, 12),  # 192-bit
        32: (8, 14)   # 256-bit
    }


    def __init__(self, key: bytes):
        """
        Initialize AES instance with the given key.
        :param key: Key as bytes (16, 24, or 32 bytes).
        """
        self.key = key
        len_key = len(key)
        self.expanded_key = self.key_expansion(key)
        self.Nr = AES.KEY_SIZES[len_key][1]


    # =============================================================================
    #                        HELPER & UTILITY FUNCTIONS
    # =============================================================================

    @staticmethod
    def sub_word(word: int) -> int:
        """
        Apply the S-Box to a 4-byte word.
        """
        bytess = []
        for i in range(4):
            bytess.append((word >> 24-8*(i)) & 0xff  )

        bytess = list(map(lambda x:AES.S_BOX[x],bytess))
        res = 0
        for i in range(4):
            res|= bytess[i] << (8*(3-i))

        return res

    @staticmethod
    def rot_word(word: int) -> int:
        """
        Cyclically permute the bytes of a word.
        """
        bytess = []
        for i in range(4):
            bytess.append((word >> 24-8*(i)) & 0xff  )

        return (bytess[1] << 24) | (bytess[2] << 16) | (bytess[3] << 8) | bytess[0]

    @staticmethod
    def bytes_to_matrix(b: bytes) -> List[List[int]]:
        """
        Converts a 16, 24, or 32-byte array into a 4xNb matrix (column-major order).

        """
        m = []
        for i in range(4):
            m.append([])
        for row in range(4):
            for i in range(4):
                m[row].append(b[row*4+i])
        return m

    @staticmethod
    def matrix_to_bytes(matrix: List[List[int]]) -> bytes:
        """
        Converts a 4xNb matrix back to a bytes object.
        """
        b = []
        for row in matrix:
            b.extend(row)

        return bytes(b)

    @staticmethod
    def xor_bytes(a: bytes, b: bytes) -> bytes:
        """
        XOR two byte strings of the same length.
        """
        ret = []
        for i in range(len(a)):
            ret.append(a[i]^b[i])
        return ret

    @staticmethod
    def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
        """
        Applies PKCS7 padding to make data a multiple of the block size.
        """
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    @staticmethod
    def pkcs7_unpad(data: bytes) -> bytes:
        """
        Removes PKCS7 padding from data.
        """
        if not data:
            return data
        padding_length = data[-1]
        return data[:-padding_length]

    # =============================================================================
    #                          KEY EXPANSION
    # =============================================================================

    @staticmethod
    def key_expansion(key: bytes) -> List[int]:
        """
        Given a key (128, 192, or 256 bits), generate the expanded key schedule.

        :param key: Original key as bytes.
        :return: Expanded key as a list of 32-bit integers (words).
        """
        key_size = len(key)
        if key_size not in AES.KEY_SIZES:
            raise ValueError("Key must be 128, 192, or 256 bits (16, 24, or 32 bytes).")

        Nk, Nr = AES.KEY_SIZES[key_size]  # Number of 32-bit words, rounds
        # Convert key to an array of 32-bit integers (words)
        key_words = []
        for i in range(0, key_size, 4):
            key_words.append(
                (key[i] << 24) ^ (key[i+1] << 16) ^ (key[i+2] << 8) ^ key[i+3]
            )

        # Generate Nb*(Nr+1) words
        expanded_words = [0] * AES.NB * (Nr + 1)
        expanded_words[:Nk] = key_words[:]

        for i in range(Nk, AES.NB * (Nr + 1)):
            temp = expanded_words[i - 1]
            if i % Nk == 0:
                temp = AES.sub_word(AES.rot_word(temp)) ^ AES.RCON[i // Nk]
            elif Nk > 6 and i % Nk == 4:
                temp = AES.sub_word(temp)
            expanded_words[i] = expanded_words[i - Nk] ^ temp

        return expanded_words


    # =============================================================================
    #                      AES ENCRYPTION ROUTINES
    # =============================================================================

    @staticmethod
    def sub_bytes(state: List[List[int]]) -> None:
        """
        Substitute each byte in the state with the S-Box.
        """
        for row in state:
            for i in range(len(row)):
                row[i] = AES.S_BOX[row[i]]

    @staticmethod
    def shift_rows(state: List[List[int]]) -> None:
        """
        Shift rows to the left
        """
        state[1] = state[1][1:] + state[1][:1]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][3:] + state[3][:3]


    @staticmethod
    def xtime(a: int) -> int:
        """
        Multiply by 2 in the Galois Field GF(2^8).
        """
        a <<= 1
        if a & 0x100:
            a ^= 0x1B
        return a & 0xFF

    @staticmethod
    def mix_columns(state: List[List[int]]) -> None:
        """
        Mix columns in the state by performing matrix multiplication in GF(2^8).
        Uses AES.xtime().
        """
        for i in range(4):
            s0,s1,s2,s3 = [state[0][i],state[1][i],state[2][i],state[3][i]]

            t0 = AES.xtime(s0) ^ AES.xtime(s1) ^ s1 ^ s2 ^ s3
            t1 = s0 ^ AES.xtime(s1) ^ AES.xtime(s2) ^ s2 ^ s3
            t2 = s0 ^ s1 ^ AES.xtime(s2) ^ AES.xtime(s3) ^ s3
            t3 = AES.xtime(s0) ^ s0 ^ s1 ^ s2 ^ AES.xtime(s3)

            state[0][i],state[1][i],state[2][i],state[3][i] = t0,t1,t2,t3
        

    @staticmethod
    def add_round_key(state: List[List[int]], round_key: List[int], round_idx: int) -> None:
        """
        XOR the state with the round key.
        """
        # Each round key is 4 words = 4 x 32 bits = 16 bytes
        for i in range(4):
            byts = [state[0][i],state[1][i],state[2][i],state[3][i]]
            word = AES.xor_bytes(bytes(byts),round_key[round_idx*4+i].to_bytes(4,byteorder='big'))
            state[0][i],state[1][i],state[2][i],state[3][i] = word[:]

    @staticmethod
    def encrypt_block(plaintext_block: bytes, expanded_key: List[int],num_round:int) -> bytes:
        """
        Encrypt a single 16-byte block using AES (128, 192, or 256).
        """
        # Convert plaintext block to state matrix
        state = AES.bytes_to_matrix(plaintext_block)

        AES.add_round_key(state,expanded_key,0)

        for i in range(1,num_round):
            AES.sub_bytes(state)
            AES.shift_rows(state)
            AES.mix_columns(state)
            AES.add_round_key(state,expanded_key,i)
        
        AES.sub_bytes(state)
        AES.shift_rows(state)
        AES.add_round_key(state,expanded_key,num_round)

        return AES.matrix_to_bytes(state)
    
    # =============================================================================
    #                      AES DECRYPTION ROUTINES
    # =============================================================================

    @staticmethod
    def inv_sub_bytes(state: List[List[int]]) -> None:
        """
        Inverse S-Box substitution for decryption.
        """
        for row in state:
            for i in range(len(row)):
                row[i] = AES.INV_S_BOX[row[i]]

    @staticmethod
    def inv_shift_rows(state: List[List[int]]) -> None:
        """
        Inverse shift rows to the right
        """
        state[1] = state[1][-1:] + state[1][:-1]
        state[2] = state[2][-2:] + state[2][:-2]
        state[3] = state[3][-3:] + state[3][:-3]

    @staticmethod
    def mul(a: int, b: int) -> int:
        """
        Multiply two bytes a and b in GF(2^8).

        :param a: Byte a.
        :param b: Byte b.
        :return: Result of multiplication in GF(2^8).
        """
        r = 0
        for _ in range(8):
            if b & 1:
                r ^= a
            hi_bit = a & 0x80
            a <<= 1
            if hi_bit:
                a ^= 0x1b
            a &= 0xFF
            b >>= 1
        return r & 0xFF

    @staticmethod
    def inv_mix_columns(state: List[List[int]]) -> None:
        """
        Inverse MixColumns for decryption in GF(2^8).
        """
        for c in range(AES.NB):
            a = state[0][c]
            b = state[1][c]
            d = state[2][c]
            e = state[3][c]

            # Precompute
            au = AES.mul(a, 0x0e) ^ AES.mul(b, 0x0b) ^ AES.mul(d, 0x0d) ^ AES.mul(e, 0x09)
            bu = AES.mul(a, 0x09) ^ AES.mul(b, 0x0e) ^ AES.mul(d, 0x0b) ^ AES.mul(e, 0x0d)
            du = AES.mul(a, 0x0d) ^ AES.mul(b, 0x09) ^ AES.mul(d, 0x0e) ^ AES.mul(e, 0x0b)
            eu = AES.mul(a, 0x0b) ^ AES.mul(b, 0x0d) ^ AES.mul(d, 0x09) ^ AES.mul(e, 0x0e)

            state[0][c] = au
            state[1][c] = bu
            state[2][c] = du
            state[3][c] = eu


    @staticmethod
    def decrypt_block(ciphertext_block: bytes, expanded_key: List[int],num_round: int) -> bytes:
        """
        Decrypt a single 16-byte block using AES (128, 192, or 256).
        """
        # Convert ciphertext block to state matrix
        state = AES.bytes_to_matrix(ciphertext_block)

        AES.add_round_key(state, expanded_key, num_round)

        for i in range(num_round - 1, 0, -1):
            AES.inv_shift_rows(state)
            AES.inv_sub_bytes(state)
            AES.add_round_key(state, expanded_key, i)
            AES.inv_mix_columns(state)
        
        AES.inv_shift_rows(state)
        AES.inv_sub_bytes(state)
        AES.add_round_key(state, expanded_key, 0)

        return AES.matrix_to_bytes(state)

    # =============================================================================
    #                    MULTI-BLOCK ENCRYPT/DECRYPT
    # =============================================================================

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        AES encrypt the plaintext with the given key.
        Applies PKCS7 padding.

        :return: Ciphertext as bytes.
        """
        block_size = 16
        padded_plaintext = AES.pkcs7_pad(plaintext, block_size)
        num_blocks = len(padded_plaintext) // block_size
        results = []
        for i in range(num_blocks):
            start = i* block_size
            block = padded_plaintext[start: start+block_size]
            encrypted_block = AES.encrypt_block(block, self.expanded_key, self.Nr)
            results.append(encrypted_block)
        return b''.join(results)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        AES decrypt the ciphertext with the given key.
        Removes PKCS7 padding.

        :return: Decrypted plaintext as bytes (unpadded).
        """
        block_size = 16
        num_blocks = len(ciphertext) // block_size
        results = []
        for i in range(num_blocks):
            start = i * block_size
            block = ciphertext[start:start + block_size]
            results.append(AES.decrypt_block(block, self.expanded_key, self.Nr))
        plaintext = b''.join(results)
        return AES.pkcs7_unpad(plaintext)
class DES:
    # -----------------------------------------------------------------------------
    #                           DES PERMUTATION TABLES
    # -----------------------------------------------------------------------------

    #: Initial Permutation table (64 bits)
    IP_TABLE = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    #: Final Permutation table (64 bits)
    FP_TABLE = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]

    #: PC1 (Permuted Choice 1) - 64-bit key -> 56-bit key
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1,  58, 50, 42, 34, 26, 18,
        10, 2,  59, 51, 43, 35, 27,
        19, 11, 3,  60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7,  62, 54, 46, 38, 30, 22,
        14, 6,  61, 53, 45, 37, 29,
        21, 13, 5,  28, 20, 12, 4
    ]

    #: PC2 (Permuted Choice 2) - 56-bit key -> 48-bit subkey
    PC2 = [
        14, 17, 11, 24, 1,  5,
        3,  28, 15, 6,  21, 10,
        23, 19, 12, 4,  26, 8,
        16, 7,  27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    #: Number of left shifts in each round
    SHIFT_TABLE = [ 
        1, 1, 2, 2, 2, 2, 2, 2,
        1, 2, 2, 2, 2, 2, 2, 1
    ]

    #: Expansion table (32 bits -> 48 bits)
    E_TABLE = [
        32, 1,  2,  3,  4,  5,
        4,  5,  6,  7,  8,  9,
        8,  9,  10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    #: S-Boxes (eight of them, each 4x16)
    S_BOXES = [
        # S1
        [
            [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
            [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
            [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
            [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]
        ],
        # S2
        [
            [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
            [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
            [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
            [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
        ],
        # S3
        [
            [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
            [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
            [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
            [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
        ],
        # S4
        [
            [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
            [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
            [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
            [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
        ],
        # S5
        [
            [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
            [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
            [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
            [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]
        ],
        # S6
        [
            [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
            [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
            [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
            [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]
        ],
        # S7
        [
            [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
            [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
            [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
            [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]
        ],
        # S8
        [
            [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
            [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
            [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
            [ 2,  1, 14,  7,  4, 10,  8, 13, 15,  9,  3,  5,  6, 12, 11,  0]
        ]
    ]

    #: P-Box permutation (32 bits)
    P_TABLE = [
        16, 7,  20, 21,
        29, 12, 28, 17,
        1,  15, 23, 26,
        5,  18, 31, 10,
        2,  8,  24, 14,
        32, 27, 3,  9,
        19, 13, 30, 6,
        22, 11, 4,  25
    ]

    num_round = 16

    def __init__(self, key: bytes, method: str = "xor_based"):
        """
        Initialize DES instance with the given 8-byte key.
        :param key: 8-byte key (64 bits) - note that only 56 bits are effectively used.
        :param method: Feistel function type ("standard", "xor_based", "and_based".).
        """
        self.key = key
        self.method = method
        key_int = int.from_bytes(key, 'big')
        key_bits = DES._int_to_bits(key_int, 64)
        self.subkeys = DES.generate_subkeys(key_bits)


    # -----------------------------------------------------------------------------
    #                           HELPER FUNCTIONS
    # -----------------------------------------------------------------------------

    @staticmethod
    def _permute(bits: List[int], table: List[int]) -> List[int]:
        """
        Permute the given bits according to a permutation table.
        """
        return [ bits[table[i]-1] for i in range(len(table)) ]
    
    @staticmethod
    def _left_rotate(bits: List[int], n: int) -> List[int]:
        """
        Left-rotate a list of bits by n positions.
        """
        return bits[n:] + bits[:n]

    @staticmethod
    def _bits_to_int(bits: List[int]) -> int:
        """
        Convert a list of bits to an integer.
        """
        value = 0
        for bit in bits:
            value = (value << 1) | bit
        return value

    @staticmethod
    def _int_to_bits(value: int, length: int) -> List[int]:
        """
        Convert an integer to a list of bits of a given length.
        """
        bits = []
        while value>0:
            bits.insert(0, value & 1)
            value >>= 1

        while len(bits)<length:
            bits.insert(0,0)

        return bits

    @staticmethod
    def _xor_bits(a: List[int], b: List[int]) -> List[int]:
        """
        XOR two lists of bits.
        """
        ret = []
        for i in range(len(a)):
            ret.append(a[i] ^ b[i])
        return ret
    @staticmethod
    def _and_bits(a,b):
        ret = []
        for i in range(len(a)):
            ret.append(a[i] & b[i])
        return ret
    
    @staticmethod
    def pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
        """
        Applies PKCS7 padding to make data a multiple of the block size.
        """
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    @staticmethod
    def pkcs7_unpad(data: bytes) -> bytes:
        """
        Removes PKCS7 padding from data.
        """
        if not data:
            return data
        padding_length = data[-1]
        return data[:-padding_length]
    # -----------------------------------------------------------------------------
    #                   KEY SCHEDULING (SUBKEY GENERATION)
    # -----------------------------------------------------------------------------

    @staticmethod
    def generate_subkeys(key_64: List[int]) -> List[List[int]]:
        """
        Generate 16 round subkeys (each 48 bits) from a 64-bit key (as bits).
        8 bits in the 64 are parity bits, so effective key length is 56 bits.

        :return: A list of 16 subkeys (each 48 bits).
        """
        key_56 = DES._permute(key_64, DES.PC1)
        C = key_56[:28]
        D = key_56[28:]
        subkeys = []
        for i in range(DES.num_round):
            C = DES._left_rotate(C,DES.SHIFT_TABLE[i])
            D = DES._left_rotate(D,DES.SHIFT_TABLE[i])

            combine = C + D
            subkey = DES._permute(combine,DES.PC2)
            subkeys.append(subkey)
        return subkeys

    # -----------------------------------------------------------------------------
    #                           FEISTEL FUNCTION
    # -----------------------------------------------------------------------------

    @staticmethod
    def feistel_function(r_bits: List[int], subkey: List[int], method: str = "standard") -> List[int]:
        """
        Implements both the standard Feistel function (DES-style) and the XOR-Based Feistel function.

        :param r_bits: The 32-bit right half of the data.
        :param subkey: The 48-bit subkey for this round.
        :param method: The Feistel function type. Options:
                       - "standard": Standard DES Feistel function (expansion, XOR, S-Boxes, P-Box)
                       - "xor_based": XOR-Based Feistel function (simple XOR with subkey)
                       - "and_based": AND-Based Fesitel function (simple AND with subkey)
        :return: 32-bit transformed output.
        """
        # INSIDE feistel_function METHOD
        if method == "xor_based":
            expanded = DES._permute(r_bits, DES.E_TABLE)  
            xored = DES._xor_bits(expanded, subkey)         
            return xored[:32]  

        elif method == "and_based":
            expanded = DES._permute(r_bits, DES.E_TABLE)  
            and_result = [rb & sk for rb, sk in zip(expanded, subkey)]  
            return and_result[:32]  

        elif method == "standard":
            expaned_r = DES._permute(r_bits,DES.E_TABLE)

            xor_bits = DES._xor_bits(expaned_r,subkey)
            group_size = 6
            subed_bits = []

            for i in range(8):
                start = i*group_size
                group = xor_bits[start:start+group_size]
                row = DES._bits_to_int([group[0],group[5]])
                column = DES._bits_to_int(group[1:5])
                selected = DES._int_to_bits(DES.S_BOXES[i][row][column],4)
                subed_bits += selected
            subed_bits = DES._permute(subed_bits,DES.P_TABLE)
            return subed_bits

        else:
            raise ValueError("Invalid method! Choose 'standard',  'xor_based' or 'and_based'.")

    # -----------------------------------------------------------------------------
    #                       DES ENCRYPTION/DECRYPTION ROUND
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    #                   BLOCK ENCRYPTION/DECRYPTION METHODS
    # -----------------------------------------------------------------------------

    def encrypt_block(self, block: bytes) -> bytes:
        """
        Encrypt a single 8-byte block using DES.
        """
        block_int = int.from_bytes(block, 'big')
        block_bits = DES._int_to_bits(block_int, 64)

        permuted_block = self._permute(block_bits,DES.IP_TABLE)

        L = permuted_block[:32]
        R = permuted_block[32:]

        for round in range(DES.num_round):
            L , R = R , self._xor_bits(self.feistel_function(R,self.subkeys[round],method=self.method),L)

        combined = R + L
        ciphertext_bits = self._permute(combined, DES.FP_TABLE)
        ciphertext_int = DES._bits_to_int(ciphertext_bits)
        return ciphertext_int.to_bytes(8,'big')

    def decrypt_block(self, block: bytes) -> bytes:
        """
        Decrypt a single 8-byte block using DES.
        """

        block_int = int.from_bytes(block, 'big')
        block_bits = DES._int_to_bits(block_int, 64)

        permuted_block = self._permute(block_bits,DES.IP_TABLE)

        L = permuted_block[:32]
        R = permuted_block[32:]

        for round in range(DES.num_round):
            dec_round = DES.num_round - round -1
            L , R = R , self._xor_bits(self.feistel_function(R,self.subkeys[dec_round],method=self.method),L)

        combined = R + L
        ciphertext_bits = self._permute(combined, DES.FP_TABLE)
        ciphertext_int = DES._bits_to_int(ciphertext_bits)
        return ciphertext_int.to_bytes(8,'big')

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt a plaintext (bytes) using DES with the given 8-byte key.
        This function handles block-by-block encryption, including padding.

        :return: Encrypted data in bytes.
        """
        block_size = 8
        padded_plaintext = DES.pkcs7_pad(plaintext, block_size)
        num_blocks = len(padded_plaintext) // block_size
        results = []
        for i in range(num_blocks):
            start = i* block_size
            block = padded_plaintext[start: start+block_size]
            encrypted_block = self.encrypt_block(block)
            results.append(encrypted_block)

        return b''.join(results)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt a ciphertext (bytes) using DES with the given 8-byte key.
        This function handles block-by-block decryption, then removes padding.

        :return: Decrypted data in bytes (with padding removed).
        """
        block_size = 8
        num_blocks = len(ciphertext) // block_size
        results = []
        for i in range(num_blocks):
            start = i * block_size
            block = ciphertext[start:start + block_size]
            results.append(self.decrypt_block(block))
        plaintext = b''.join(results)
            
        return DES.pkcs7_unpad(plaintext)
class DiffieHellman:

    def __init__(self, p: int, g: int, private_key: Optional[int] = None):
        """
        Initialize DiffieHellman with a prime p and generator g.
        Optionally supply a custom private_key (for testing). If not provided,
        a random private_key will be generated.

        """
        self.p = p
        self.g = g
        self.private_key = private_key if private_key is not None else self._generate_private_key()
        self.public_key = pow(self.g,self.private_key,p)
    
    def _generate_private_key(self) -> int:
        """
        Generate a random private key using the 'secrets' module.
        """
        return secrets.randbelow(self.p - 1) + 1

    def get_public_key(self) -> int:
        """
        Simple getter for pu_key.
        """
        return self.public_key

    def compute_shared_secret(self, other_public_key: int) -> int:
        """
        Compute the shared secret/key using the other party's public key.
        """
        return pow(other_public_key,self.private_key,self.p)
class RSA:
    """
    Supports encryption and decryption with *chunking*.
    """

    def __init__(self, bit_size: int = 1024, e: int = 65537,p=None, q=None, seed=42):
        """
        Initialize RSA with a specified bit_size for p and q.

        :param bit_size: Bit length for each prime p and q.
        """
        random.seed(seed)
        if p is None or q is None:
            while True:
                p = sympy.randprime(2**(bit_size - 1), 2**bit_size)
                q = sympy.randprime(2**(bit_size - 1), 2**bit_size)
                if p != q:
                    break
        
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        if sympy.gcd(e,self.n)!=1:
            raise ValueError("e must be coprime with φ(n)")
        self.e = e
        self.d = pow(e,-1,self.phi)

    def get_public_key(self) -> Tuple[int, int]:
        """
        Returns the public key (n, e).
        """
        return (self.n,self.e)

    def get_private_key(self) -> Tuple[int, int]:
        """
        Returns the private key (n, d).
        """
        return(self.n,self.d)

    def encrypt_chunk(self, chunk: bytes,chunk_size:int) -> bytes:
        """
        Encrypts a single chunk of bytes (must be < n).
        """
        m = int.from_bytes(chunk, byteorder='big')
        c = pow(m, self.e ,self.n)
        return c.to_bytes(chunk_size, byteorder='big')

    def decrypt_chunk(self, chunk: bytes,chunk_size:int) -> bytes:
        """
        Decrypts a single chunk of bytes.
        """
        m = int.from_bytes(chunk, byteorder='big')
        c = pow(m, self.d ,self.n)
        return c.to_bytes(chunk_size, byteorder='big')

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts data using chunking.
        """
        chunk_size = (self.n.bit_length() + 7) // 8
        num_chunks = ceil(len(data) / chunk_size)
        res = []
        for i in range(num_chunks):
            start =i*chunk_size
            chunk = data[start:start+chunk_size]
            res.append(self.encrypt_chunk(chunk,chunk_size))

        return b''.join(res)

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypts data using chunking.
        """
        chunk_size = (self.n.bit_length() + 7) // 8 
        num_chunks = ceil(len(data) / chunk_size)
        res = []
        for i in range(num_chunks):
            start =i*chunk_size
            chunk = data[start:start+chunk_size]
            res.append(self.decrypt_chunk(chunk,chunk_size))
            
        return b''.join(res)

def int_to_fixed_bytes(number: int, length: int) -> bytes:
    raw_bytes = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')

    if len(raw_bytes) > length:
        return raw_bytes[-length:]
    else:
        return raw_bytes.rjust(length, b'\x00')
    
def process_input(input_lines: list) -> str:
    """
    Parse the structured input and process AES encryption or decryption.

    Expected input format (3 lines):
      Line 1: mode: <encrypt/decrypt>
      Line 2: key: <key string>   (16, 24, or 32 bytes when encoded)
      Line 3: plaintext: <message>  if encrypt
              OR
              ciphertext: <hex-encoded string>  if decrypt

    Returns the processed output as a string.
    """
    data = {}
    for line in input_lines:
        if not line.strip() or ':' not in line:
            continue
            
        # Split on first colon only
        parts = line.split(':', 1)
        key = parts[0].strip().lower()
        value = parts[1].strip()
        
        # Special handling for multi-line messages
        if key == 'message':
            # Check if we already have a message (for multi-line)
            if 'message' in data:
                data['message'] += '\n' + value
            else:
                data['message'] = value
        else:
            data[key] = value

    scenario = data.get("scenario")
    # print('\n\n')
    
    
    if scenario == "DH_AES":
        p = int(data['p'])
        g = int(data['g'])
        alice_key = int(data['alice_private'])
        alice_dh = DiffieHellman(p,g,alice_key)
        print(f'alice_public: {alice_dh.get_public_key()}')
        bob_key = int(data['bob_private'])
        bob_dh = DiffieHellman(p,g,bob_key)
        print(f'bob_public: {bob_dh.get_public_key()}')
        shared_secret = bob_dh.compute_shared_secret(alice_dh.get_public_key())
        print(f'shared_secret: {shared_secret}')
        aes_key = shared_secret.to_bytes(16, byteorder='big')
        print(f'aes_key: {aes_key.hex()}')
        aes = AES(aes_key)
        cipher_text = aes.encrypt(data['message'].encode('utf-8'))
        print(f'ciphertext: {cipher_text.hex()}')
        decrypted = aes.decrypt(cipher_text)
        print(f'decrypted_message: {decrypted.decode("utf-8")}')
    elif scenario =='DH_DES':
        p = int(data['p'])
        g = int(data['g'])
        alice_key = int(data['alice_private'])
        alice_dh = DiffieHellman(p,g,alice_key)
        print(f'alice_public: {alice_dh.get_public_key()}')
        bob_key = int(data['bob_private'])
        bob_dh = DiffieHellman(p,g,bob_key)
        print(f'bob_public: {bob_dh.get_public_key()}')
        shared_secret = bob_dh.compute_shared_secret(alice_dh.get_public_key())
        print(f'shared_secret: {shared_secret}')
        des_key = shared_secret.to_bytes(8, byteorder='big')
        print(f'des_key: {des_key.hex()}')
        des = DES(des_key)
        cipher_text = des.encrypt(data['message'].encode('utf-8'))
        print(f'ciphertext: {cipher_text.hex()}')
        decrypted = des.decrypt(cipher_text)
        print(f'decrypted_message: {decrypted.decode("utf-8")}')
    elif scenario == 'RSA_DES':
        rsa_bit_size = int(data['rsa_bit_size'])
        p = int(data['p'])
        q = int(data['q'])
        rsa = RSA(rsa_bit_size,p=p,q=q)
        print(f'rsa_public_n: {rsa.n}')
        print(f'rsa_public_e: {rsa.e}')
        print(f'rsa_private_d: {rsa.d}')
        encrypted_key = rsa.encrypt(bytes.fromhex(data['des_key']))
        print(f'encrypted_des_key: {encrypted_key.hex()}')
        decrypted_key = rsa.decrypt(encrypted_key)
        print(f'decrypted_des_key: {decrypted_key[-8:].hex()}')
        key = decrypted_key.hex()
        des = DES(bytes.fromhex(key))
        cipher_text = des.encrypt(data['message'].encode('utf-8'))
        print(f'ciphertext: {cipher_text.hex()}')
        decrypted = des.decrypt(cipher_text)
        print(f'decrypted_message: {decrypted.decode("utf-8")}')

    elif scenario == 'RSA_AES':
        rsa_bit_size = int(data['rsa_bit_size'])
        p = int(data['p'])
        q = int(data['q'])
        rsa = RSA(rsa_bit_size,p=p,q=q)
        print(f'rsa_public_n: {rsa.n}')
        print(f'rsa_public_e: {rsa.e}')
        print(f'rsa_private_d: {rsa.d}')
        encrypted_key = rsa.encrypt(bytes.fromhex(data['aes_key']))
        print(f'encrypted_aes_key: {encrypted_key.hex()}')
        decrypted_key = rsa.decrypt(encrypted_key)
        print(f'decrypted_aes_key: {decrypted_key[-16:].hex()}')
        key = decrypted_key.hex().lstrip('0')
        aes = AES(bytes.fromhex(key))
        cipher_text = aes.encrypt(data['message'].encode('utf-8'))
        print(f'ciphertext: {cipher_text.hex()}')
        decrypted = aes.decrypt(cipher_text)
        print(f'decrypted_message: {decrypted.decode("utf-8")}')
    else:
        return "Error: Invalid mode specified."

if __name__ == "__main__":
    # Expecting exactly 3 lines of input
    input_lines = sys.stdin.read().splitlines()
    result = process_input(input_lines)
    # print(result)