import bitcoin
import os
import hashlib
import base58
from Crypto.Hash import RIPEMD160
def generate_private_key():
    return os.urandom(32).hex()

def private_key_to_public_key(private_key):
    decoded_private_key = bytes.fromhex(private_key)
    public_key = bitcoin.fast_multiply(bitcoin.G, int.from_bytes(decoded_private_key, 'big'))
    return bitcoin.encode_pubkey(public_key, 'bin')

def public_key_to_address(public_key):

    sha256 = hashlib.sha256(public_key).digest()
    
    ripemd160 = RIPEMD160.new()
    ripemd160.update(sha256)
    hashed_public_key = ripemd160.digest()
    
    network_byte = b'\x00' + hashed_public_key
    
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    
    binary_address = network_byte + checksum
    
    return base58.b58encode(binary_address).decode('utf-8')

def find_vanity_address(prefix):
    """Find a Bitcoin vanity address starting with the given prefix."""
    print(f"Searching for Bitcoin address starting with '{prefix}'...")
    iter = 0
    while True:
        
        private_key = generate_private_key()
        
        public_key = private_key_to_public_key(private_key)
       
        address = public_key_to_address(public_key)
        
        if address.startswith(prefix):
            print("\nFound a matching address!")
            print(f"Private Key: {private_key}")
            print(f"Bitcoin Address: {address}")
            break
        if iter % 100000 == 0:
          print(iter)
        iter += 1
if __name__ == "__main__":
    
    desired_prefix = "1ALi"
    find_vanity_address(desired_prefix)