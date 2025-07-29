from typing import List, Tuple
import hashlib

class GODEL:

    IP_TABLE = [115, 160, 17, 33, 68, 190, 93, 220, 135, 70, 146, 237, 97, 10, 163, 148, 221, 89, 28, 197, 55, 156, 19, 60, 41, 136, 116, 102, 139, 238, 38, 122, 171, 177, 218, 83, 37, 255, 129, 14, 94, 72, 96, 161, 147, 254, 98, 183, 235, 143, 217, 179, 25, 3, 181, 104, 205, 112, 138, 62, 155, 101, 44, 6, 133, 158, 202, 35, 134, 211, 2, 79, 128, 173, 5, 229, 228, 185, 39, 169, 245, 252, 251, 242, 144, 142, 113, 118, 130, 193, 210, 76, 53, 200, 107, 207, 232, 119, 153, 230, 212, 127, 176, 67, 92, 36, 1, 203, 24, 51, 253, 85, 59, 223, 141, 49, 165, 247, 206, 195, 7, 123, 201, 117, 157, 199, 240, 15, 180, 172, 16, 80, 30, 244, 150, 149, 175, 188, 8, 208, 9, 32, 114, 186, 23, 120, 204, 248, 78, 214, 145, 159, 132, 31, 69, 226, 164, 191, 233, 109, 174, 103, 61, 45, 77, 84, 111, 137, 222, 20, 56, 90, 29, 194, 74, 152, 46, 40, 48, 27, 86, 47, 21, 216, 106, 12, 140, 64, 4, 187, 95, 166, 167, 246, 108, 234, 224, 189, 81, 42, 57, 52, 124, 63, 75, 88, 66, 256, 91, 182, 250, 82, 105, 43, 22, 121, 125, 209, 241, 71, 26, 11, 13, 58, 231, 100, 126, 213, 184, 151, 196, 192, 170, 50, 154, 236, 73, 215, 18, 34, 99, 65, 225, 162, 227, 249, 54, 243, 178, 131, 168, 87, 239, 110, 198, 219]

    FP_TABLE = [107, 71, 54, 189, 75, 64, 121, 139, 141, 14, 222, 186, 223, 40, 128, 131, 3, 239, 23, 170, 183, 215, 145, 109, 53, 221, 180, 19, 173, 133, 154, 142, 4, 240, 68, 106, 37, 31, 79, 178, 25, 200, 214, 63, 164, 177, 182, 179, 116, 234, 110, 202, 93, 247, 21, 171, 201, 224, 113, 24, 163, 60, 204, 188, 242, 207, 104, 5, 155, 10, 220, 42, 237, 175, 205, 92, 165, 149, 72, 132, 199, 212, 36, 166, 112, 181, 252, 206, 18, 172, 209, 105, 7, 41, 191, 43, 13, 47, 241, 226, 62, 28, 162, 56, 213, 185, 95, 195, 160, 254, 167, 58, 87, 143, 1, 27, 124, 88, 98, 146, 216, 32, 122, 203, 217, 227, 102, 73, 39, 89, 250, 153, 65, 69, 9, 26, 168, 59, 29, 187, 115, 86, 50, 85, 151, 11, 45, 16, 136, 135, 230, 176, 99, 235, 61, 22, 125, 66, 152, 2, 44, 244, 15, 157, 117, 192, 193, 251, 80, 233, 33, 130, 74, 161, 137, 103, 34, 249, 52, 129, 55, 210, 48, 229, 78, 144, 190, 138, 198, 6, 158, 232, 90, 174, 120, 231, 20, 255, 126, 94, 123, 67, 108, 147, 57, 119, 96, 140, 218, 91, 70, 101, 228, 150, 238, 184, 51, 35, 256, 8, 17, 169, 114, 197, 243, 156, 245, 77, 76, 100, 225, 97, 159, 196, 49, 236, 12, 30, 253, 127, 219, 84, 248, 134, 81, 194, 118, 148, 246, 211, 83, 82, 111, 46, 38, 208]


    num_rounds = 16
    block_size = 256

    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError('key size is not correct')
        self.key = key
        self.subkeys = self.generate_subkeys(key)


    
    @staticmethod
    def _permute(bits: List[int], table: List[int]) -> List[int]:

        return [ bits[table[i]-1] for i in range(len(table)) ]
    
    @staticmethod
    def _left_rotate(bits: List[int], n: int) -> List[int]:

        return bits[n:] + bits[:n]

    @staticmethod
    def _bits_to_int(bits: List[int]) -> int:

        value = 0
        for bit in bits:
            value = (value << 1) | bit
        return value

    @staticmethod
    def _int_to_bits(value: int, length: int) -> List[int]:

        bits = []
        while value>0:
            bits.insert(0, value & 1)
            value >>= 1

        while len(bits)<length:
            bits.insert(0,0)

        return bits

    @staticmethod
    def _xor_bits(a: List[int], b: List[int]) -> List[int]:

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
    def pkcs7_pad(data: bytes, block_size) -> bytes:

        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    @staticmethod
    def pkcs7_unpad(data: bytes) -> bytes:

        if not data:
            return data
        padding_length = data[-1]
        return data[:-padding_length]

    @staticmethod
    def sha128(data: bytes) -> bytes:
        return hashlib.sha256(data).digest()[:16]
    
    def generate_subkeys(self,master_key: bytes) -> List[bytes]:

        subkeys = []
        k = master_key
        for i in range(1, GODEL.num_rounds+1):
            k = hashlib.sha256(k).digest()

            subkey = GODEL.sha128(k + bytes(i))
            subkey_int = int.from_bytes(subkey, 'big')
            
            subkeys.append(GODEL._int_to_bits(subkey_int, GODEL.block_size/2))

        return subkeys



    def feistel_function(self,r_bits: List[int], subkey: List[int]) -> List[int]:

        xor_bits = GODEL._xor_bits(r_bits,subkey)
        xor_int = GODEL._bits_to_int(xor_bits)
        xor_bytes = xor_int.to_bytes(GODEL.block_size//16,'big')

        hashed = GODEL.sha128(xor_bytes)
        hashed_int = int.from_bytes(hashed, 'big')
        return GODEL._int_to_bits(hashed_int,GODEL.block_size//2)



    def encrypt_block(self, block: bytes) -> bytes:

        block_int = int.from_bytes(block, 'big')
        block_bits = GODEL._int_to_bits(block_int, GODEL.block_size)

        permuted_block = self._permute(block_bits,GODEL.IP_TABLE)

        L = permuted_block[:GODEL.block_size//2]
        R = permuted_block[GODEL.block_size//2:]

        for round in range(GODEL.num_rounds):
            L , R = R , self._xor_bits(self.feistel_function(R,self.subkeys[round]),L)

        combined = R + L
        ciphertext_bits = self._permute(combined, GODEL.FP_TABLE)
        ciphertext_int = GODEL._bits_to_int(ciphertext_bits)
        return ciphertext_int.to_bytes(GODEL.block_size//8,'big')

    def decrypt_block(self, block: bytes) -> bytes:
        block_int = int.from_bytes(block, 'big')
        block_bits = GODEL._int_to_bits(block_int, GODEL.block_size)

        permuted_block = self._permute(block_bits,GODEL.IP_TABLE)

        L = permuted_block[:GODEL.block_size//2]
        R = permuted_block[GODEL.block_size//2:]

        for round in range(GODEL.num_rounds):
            dec_round = GODEL.num_rounds - round -1
            L , R = R , self._xor_bits(self.feistel_function(R,self.subkeys[dec_round]),L)

        combined = R + L
        ciphertext_bits = self._permute(combined, GODEL.FP_TABLE)
        ciphertext_int = GODEL._bits_to_int(ciphertext_bits)
        return ciphertext_int.to_bytes(GODEL.block_size//8,'big')

    def encrypt(self, plaintext: bytes) -> bytes:
        block_size = GODEL.block_size//8
        padded_plaintext = GODEL.pkcs7_pad(plaintext, block_size)
        num_blocks = len(padded_plaintext) // block_size
        results = []
        for i in range(num_blocks):
            start = i* block_size
            block = padded_plaintext[start: start+block_size]
            encrypted_block = self.encrypt_block(block)
            results.append(encrypted_block)

        return b''.join(results)

    def decrypt(self, ciphertext: bytes) -> bytes:
        block_size = GODEL.block_size//8
        num_blocks = len(ciphertext) // block_size
        results = []
        for i in range(num_blocks):
            start = i * block_size
            block = ciphertext[start:start + block_size]
            results.append(self.decrypt_block(block))
        plaintext = b''.join(results)
            
        return GODEL.pkcs7_unpad(plaintext)

def main():
    input_string = "What is encryption?"
    plaintext = input_string.encode("utf-8")

    # 32-byte key (256 bits). 
    key = b"powyrlsiqlmfyrus"
    godel_instance = GODEL(key)
    # Encrypt
    encrypted = godel_instance.encrypt(plaintext)
    print("Encrypted (hex):", encrypted.hex())
    # Decrypt
    decrypted = godel_instance.decrypt(encrypted)
    print("Decrypted plaintext:", decrypted.decode("utf-8"))
    
if __name__ == "__main__":
    'this is the main func'
    main()
