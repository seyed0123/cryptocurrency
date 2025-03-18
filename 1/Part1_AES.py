from typing import List

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
        for col in range(4):
            for i in range(4):
                m[i].append(b[col*4+i])
        return m

    @staticmethod
    def matrix_to_bytes(matrix: List[List[int]]) -> bytes:
        """
        Converts a 4xNb matrix back to a bytes object.
        """
        b = []
        for col in range(4):
            for i in range(4):
                b.append(matrix[i][col])

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
        map(lambda row: lambda y: AES.S_BOX[row[y]],state)

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
        map(lambda row: lambda y: AES.INV_S_BOX[row[y]],state)

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
        num_block = len(plaintext) // block_size
        results = []
        for i in range(num_block):
            start = i * block_size
            results.append(AES.encrypt_block(plaintext[start:start+block_size],self.expanded_key,self.Nr))
        if num_block * 128 != len(plaintext):
            results.append(AES.encrypt_block(AES.pkcs7_pad(plaintext[num_block*block_size:]),self.expanded_key,self.Nr))
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

def main(): # SINGLE TEST FOR CORRECT FUNCTIONALITY
    """
    Demonstration of an end-to-end AES encryption/decryption pipeline using the AES class.
    1. Input a string.
    2. Encrypt using AES (128, 192, or 256 bits) via the AES class.
    3. Print ciphertext in hex.
    4. Decrypt and print final plaintext.
    """
    input_string = "Hello, AES from scratch with 256-bit key?"
    print("Original plaintext:", input_string)    
    # Convert to bytes
    plaintext = input_string.encode("utf-8")
    
    #  You can also try 16 or 24 bytes for 128 or 192 bits.
    key = b"xQOzaF0eypaierZmCQxuHyvv"
    print(f"Key: {key}")  

    # Create an AES instance with the given key
    aes_instance = AES(key)
    # Encrypt
    ciphertext = aes_instance.encrypt(plaintext)
    print("Ciphertext (hex):", ciphertext.hex())

    # Decrypt
    decrypted = aes_instance.decrypt(ciphertext)
    print("Decrypted plaintext:", decrypted.decode("utf-8"))


# if __name__ == "__main__":
#     main()

