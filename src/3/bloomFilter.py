import hashlib
import hmac
import math
from array import array

class CountingBloomFilter:
    def __init__(self, key_hex: str, n: int, p: float):
        self.key = bytes.fromhex(key_hex)
        self.n = n
        self.p = p
        self.m = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2)) 
        self.k = math.floor((self.m / n) * math.log(2))            
        self.counters = array('H', [0] * self.m)                
    
    def _hash_indices(self, serial: int):
        indices = []
        for i in range(self.k):
            msg = str(serial).encode() + i.to_bytes(4, byteorder='big')
            digest = hmac.new(self.key, msg, hashlib.sha256).digest()
            idx = int.from_bytes(digest, 'big') % self.m
            indices.append(idx)
        return indices

    def add(self, serial: int):
        for idx in self._hash_indices(serial):
            if self.counters[idx] < 0xFFFF:
                self.counters[idx] += 1

    def delete(self, serial: int):
        for idx in self._hash_indices(serial):
            if self.counters[idx] > 0:
                self.counters[idx] -= 1

    def check(self, serial: int) -> bool:
        return all(self.counters[idx] > 0 for idx in self._hash_indices(serial))


def process_operations(input_lines):
    key_hex = input_lines[0].strip()
    n, p = map(float, input_lines[1].split())
    n = int(n)
    Q = int(input_lines[2])
    operations = input_lines[3:3+Q]

    cbf = CountingBloomFilter(key_hex, n, p)
    result = []

    for line in operations:
        op, x = line.strip().split()
        x = int(x)
        if op == 'A':
            cbf.add(x)
        elif op == 'D':
            cbf.delete(x)
        elif op == 'C':
            result.append("YES" if cbf.check(x) else "NO")

    return result

if __name__ == "__main__":
    inputs = [input(),input()]
    q = input()
    inputs.append(q)
    for i in range(int(q)):
        inputs.append(input())
    
    output = process_operations(inputs)
    for line in output:
        print(line)
