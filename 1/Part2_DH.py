import secrets
from typing import Optional

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