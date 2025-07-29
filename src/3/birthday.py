import hashlib
import random
from math import sqrt,ceil
import time

class Birthday_attack():
    def __init__(self,output_bits) -> None:
        self.set_mod(output_bits)

    def set_mod(self,bits):
        self.mod = 2**bits

    def sha256(self,data: str) -> int:
        st = hashlib.sha256(data.encode('utf-8')).hexdigest()
        return int(st,16) % self.mod
    
    def generate_variants(self,data):
        count = ceil(sqrt(self.mod))
        variants = set()

        invisible_chars = [
            '\x20',  
            '\t',     
            '\n',     
            '\x00',  
            '\u200B', 
            '\u3000', 
        ]

        while len(variants) < count:
            parts = data.split(" ")


            num_inserts = random.randint(1, min(len(parts), 5))

            for _ in range(num_inserts):
                pos = random.randint(0, len(parts) - 1)
                char = random.choice(invisible_chars)
                if random.choice([True, False]):
                    parts[pos] += char
                else:
                    parts.insert(pos, char)

            modified = " ".join(parts).strip()

            if random.random() > 0.5:
                modified += random.choice(invisible_chars) * random.randint(1, 3)

            variants.add(modified)

        return list(variants)
    def attack(self, a, b):
        start_time = time.time()
        a_primes = self.generate_variants(a)
        b_primes = self.generate_variants(b)
        hash_map = {}
        for txa in a_primes:
            hash_val = self.sha256(txa)
            hash_map[hash_val] = txa  

        
        for txb in b_primes:
            hash_val = self.sha256(txb)
            if hash_val in hash_map:
                txa_match = hash_map[hash_val]
                elapsed = time.time() - start_time
                print("Collision found!")
                print(f"Variant A: {txa_match}")
                print(f"Variant B: {txb}")
                print(f"Hash: {hash_val}")
                print(f"Time taken: {elapsed:.2f} seconds")
                return (txa_match, txb, hash_val,elapsed)

        print("No collision found.")
        return None
    
if __name__ == "__main__":
    simulator = Birthday_attack(16)

    original_a = "recipient: 0xAliEthAddress1234567890abcdef, amount: 0.1 ETH, fee: 0.001 ETH"
    original_b = "recipient: 0xAttackerEthAddressfedcba0987654321, amount: 0.1 ETH, fee: 0.001 ETH"


    print("Scenario 1: 16-bit collision ")
    simulator.attack(original_a, original_b)

    simulator.set_mod(24)
    print("\nScenario 2: 24-bit collision ")
    simulator.attack(original_a, original_b)

    simulator.set_mod(32)
    print("\nScenario 3: 32-bit collision ")
    simulator.attack(original_a, original_b)


"""
Scenario 1: 16-bit collision 
Collision found!
Variant A: recipient: 0xAliEthAddress1234567890abcdef,   amount: 0.1 ETH,　 fee:​ 0.001    ETH
Variant B: recipient: 0xAttackerEthAddressfedcba0987654321, amount: 0.1 ETH, fee:　 
 0.001 ​　 ETH

Hash: 5269
Time taken: 0.01 seconds

Scenario 2: 24-bit collision 
Collision found!
Variant A: recipient: 0xAliEthAddress1234567890abcdef, amount:   0.1 ETH, fee: 0.001 ETH
Variant B: recipient: 0xAttackerEthAddressfedcba0987654321,   amount:    0.1 ETH, fee:　 0.001 
 ETH
Hash: 8484634
Time taken: 0.13 seconds

Scenario 3: 32-bit collision 
Collision found!
Variant A: recipient: 0xAliEthAddress1234567890abcdef, amount: 0.1 ETH, 　　 fee: 0.001 ETH
Variant B: recipient: 0xAttackerEthAddressfedcba0987654321, amount: 0.1　 ETH, fee: 　 0.001 ETH
Hash: 2085217838
Time taken: 2.05 seconds
"""
    
