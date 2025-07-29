import hashlib
import sys

def hash256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def reverse_hex(hex_str: str) -> str:
    return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))

class MerkleTree:
    def __init__(self, txids):

        self.leaves = [bytes.fromhex(reverse_hex(txid)) for txid in txids]
        self.levels = [self.leaves]
        self.build_tree()

    def build_tree(self):

        current = self.leaves
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                left = current[i]

                right = current[i + 1] if (i + 1) < len(current) else left
                parent = hash256(left + right)
                next_level.append(parent)
            self.levels.append(next_level)
            current = next_level

    def get_root(self) -> str:

        root_le = self.levels[-1][0]
        return reverse_hex(root_le.hex())

    def get_proof(self, index: int) -> list:

        proof = []
        idx = index
        for level in self.levels[:-1]:
            # sibling index = idx XOR 1
            sib_idx = idx ^ 1
            if sib_idx < len(level):
                sib_raw_le = level[sib_idx]
            else:

                sib_raw_le = level[idx]

            proof.append(reverse_hex(sib_raw_le.hex()))
            idx //= 2
        return proof

    @staticmethod
    def verify_proof(txid_be: str,
                     index: int,
                     proof: list,
                     merkle_root_be: str) -> bool:

        current_le = bytes.fromhex(reverse_hex(txid_be))
        idx = index
        for sibling_be in proof:
            sibling_le = bytes.fromhex(reverse_hex(sibling_be))
            if idx % 2 == 0:
                current_le = hash256(current_le + sibling_le)
            else:
                current_le = hash256(sibling_le + current_le)
            idx //= 2

        computed_root_be = reverse_hex(current_le.hex())
        return computed_root_be.lower() == merkle_root_be.lower()


def main():
    cmd = input().strip()
    if cmd == "root":
        n = int(input().strip())
        txids = [input().strip() for _ in range(n)]
        tree = MerkleTree(txids)
        print(tree.get_root())

    elif cmd == "path":
        index = int(input().strip())
        n = int(input().strip())
        txids = [input().strip() for _ in range(n)]
        tree = MerkleTree(txids)
        proof = tree.get_proof(index)
        for sib_be in proof:
            print(sib_be)           
        print(tree.get_root())

    elif cmd == "verify":
        index = int(input().strip())
        merkle_root_be = input().strip()
        p = int(input().strip())
        siblings_be = [input().strip() for _ in range(p)]
        n = int(input().strip())
        txids = [input().strip() for _ in range(n)]
        target_txid = txids[index]

        valid = MerkleTree.verify_proof(target_txid, index, siblings_be, merkle_root_be)
        print("valid" if valid else "invalid")

    else:
        print("Unknown command", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
