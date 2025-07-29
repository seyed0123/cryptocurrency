import hashlib
from typing import Tuple, Dict, Union
import random

class DSA:
    def __init__(self, params: dict):
        """Initialize DSA with parameters"""
        self.p = params.get('p')  # prime modulus
        self.q = params.get('q')  # prime divisor of p-1
        self.g = params.get('g')  # generator
        self.x = params.get('x')  # private key (0 < x < q)
        self.y = params.get('y')  # public key (y = g^x mod p)
        self.message = params.get('message', b'')  # message to sign/verify
        self.r = params.get('r', 0)  # signature component r
        self.s = params.get('s', 0)  # signature component s

    def hash_message(self) -> int:
        """Hash the message using SHA-256 and return as integer"""
        sha256 = hashlib.sha256()
        sha256.update(self.message)
        return int.from_bytes(sha256.digest(), byteorder='big')

    def sign(self,k:int = 0x358d182f103d110f6e957ee3b88c09785aa76476) -> Tuple[str, str, str]:
        """
        Generate DSA signature and return r, s, and y
        Use k = 0x358d182f103d110f6e957ee3b88c09785aa76476 for testing
        """
        if k is None:
            k = random.randint(1, self.q - 1)
        elif k <= 0 or k >= self.q:
            raise ValueError("k must be between 1 and q-1")
    
        r = pow(self.g, k, self.p) % self.q
        h = self.hash_message()
        s = (pow(k, -1, self.q) * (h + self.x * r)) % self.q
        if s == 0:
            raise ValueError("s cannot be 0, try a different k")
        
        self.r = r
        self.s = s
        self.y = pow(self.g, self.x, self.p)

        return (hex(self.r)[2:], hex(self.s)[2:], hex(self.y)[2:])
        

    def verify(self) -> bool:
        """Verify DSA signature"""
        if not (0 < self.r < self.q) or not (0 < self.s < self.q):
                    return False
        
        if not (0 < self.y < self.p) or not (pow(self.y, self.q, self.p) == 1):
            return False
        
        w = pow(self.s, -1, self.q)
        h = self.hash_message()
        u1 = (h * w) % self.q
        u2 = (self.r * w) % self.q
        v = (pow(self.g, u1, self.p) * pow(self.y, u2, self.p) % self.p) % self.q

        return v == self.r

# Example DSA parameters (these would normally be much larger in production)
params = {
    'p': 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1,
    'q': 0xf4f47f05794b256174bba6e9b396a7707e563c5b,
    'g': 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291,
    'x': 0x123456789abcdef,  # Private key
    'message': b"Hello, this is a test message for DSA"
}

# Sign a message
dsa = DSA(params)
r, s, y = dsa.sign()
print(f"Signature (r, s, y):\n{r}\n{s}\n{y}")

# Verify the signature
dsa.r = int(r, 16)
dsa.s = int(s, 16)
dsa.y = int(y, 16)
is_valid = dsa.verify()
print(f"Signature valid: {is_valid}")