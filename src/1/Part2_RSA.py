import sympy  # use this or other modules for generating required prime numbers
from typing import Tuple
import random
from math import ceil
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

if __name__ == "__main__":
    'this is the main func'
    rsa = RSA(bit_size=128,p = 305416400905440115772647883216561380153,q= 184591891995343037399549487648794439563)  # Smaller bit size for demonstration purposes
    message = b"Hello, RSA encryption with chunking!"
    
    # Encrypt the message
    encrypted = rsa.encrypt(message)
    print("Encrypted:", encrypted.hex())
    
    # Decrypt the message
    decrypted = rsa.decrypt(encrypted)
    print("Decrypted:", decrypted.decode())