import hashlib
import json

def hash256(hex_str: str) -> str:
    """Perform double SHA256 on a hex string (interpreted as raw binary)."""
    binary = bytes.fromhex(hex_str)
    hash1 = hashlib.sha256(binary).digest()
    hash2 = hashlib.sha256(hash1).digest()
    return hash2.hex()

def reverse_hex(hex_str: str) -> str:
    """Reverse byte order (little-endian <-> big-endian)."""
    return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))

def merkleroot(txids,target, level=0):
    """Compute Merkle root recursively and print the tree."""
    indent = "  " * level
    print(f"{indent}Level {level}, {len(txids)} txids:")
    ind = 0
    for txid in txids:
        st = f"{indent}  {txid}"
        if txid == target:
            st+="   <-------------  "
            if ind %2 ==0:
                st+='↓↓'
            else:
                st+= '↑↑'
            
        print(st)

        ind+=1

    if len(txids) == 1:
        return txids[0]

    new_level = []
    for i in range(0, len(txids), 2):
        one = txids[i]
        two = txids[i + 1] if i + 1 < len(txids) else txids[i]  # duplicate if odd number
        concat = one + two
        hashed = hash256(concat)
        new_level.append(hashed)
        if one == target or two == target:
            target = hashed

    print()
    return merkleroot(new_level,target, level + 1)

# Sample txids from Bitcoin block #170
# with open('src/3/hash.json', 'r') as f:
#         txids = json.load(f)
# input()
# ind =int(input())
# txids = []
# for i in range(int(input())):
#     txids.append(input())

with open('src/3/hash.json', 'r') as f:
    txids = json.load(f)
ind = 5

# Convert txids from display order (little-endian) to internal order (big-endian)
txids_le = [reverse_hex(txid) for txid in txids]

# Compute Merkle root and convert back to little-endian
raw_root = merkleroot(txids_le,txids_le[ind])
final_merkle_root = reverse_hex(raw_root)

print("\nMerkle Root (hex, little-endian):", final_merkle_root)
