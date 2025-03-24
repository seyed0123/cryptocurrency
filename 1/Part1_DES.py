from typing import List, Tuple

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
        for i in range(16):
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
        if method == "xor_based":
            #TODO
            return DES._xor_bits(r_bits,subkey[:32])
            pass

        elif method == "and_based":
            #TODO
            return DES._and_bits(r_bits,subkey[:32])
            pass

        elif method == "standard":
            #TODO
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

        L, R = permuted_block[:32], permuted_block[32:]

        for round in range(16):
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

        L,R = permuted_block[:32],permuted_block[:32]

        for round in range(16):
            dec_round = 15-round
            L , R = R , self._xor_bits(self.feistel_function(R,self.subkeys[dec_round],method=self.method),L)

        combined = R + L
        ciphertext_bits = self._permute(combined, DES.FP_TABLE)
        ciphertext_int = DES._bits_to_int(ciphertext_bits)
        return ciphertext_int.to_bytes(8,'big')
    
        pass

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

def main():  # SINGLE TEST FOR CORRECT FUNCTIONALITY
    """
    Demonstration of an end-to-end DES encryption/decryption pipeline.
    1. Takes an input string.
    2. Encrypts it with a given 8-byte key.
    3. Prints the encrypted bytes in hex.
    4. Decrypts and prints the final plaintext.
    """
    method = "xor_based"
    input_string = "Hello, DES from scratch!"
    plaintext = input_string.encode("utf-8")

    # 8-byte key (64 bits). 
    #NOTE: Only 56 bits are effectively used; the rest are parity bits.
    key = b"9017rMne"
    print("Original plaintext:", input_string)
    des_instance = DES(key, method)
    # Encrypt
    encrypted = des_instance.encrypt(plaintext)
    print("Encrypted (hex):", encrypted.hex())
    # Decrypt
    decrypted = des_instance.decrypt(encrypted)
    print("Decrypted plaintext:", decrypted.decode("utf-8"))
    
if __name__ == "__main__":
    main()
