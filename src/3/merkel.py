import hashlib

def hash256(hex_str: str) -> str:
    binary = bytes.fromhex(hex_str)
    hash1 = hashlib.sha256(binary).digest()
    hash2 = hashlib.sha256(hash1).digest()
    return hash2.hex()

def reverse_hex(hex_str: str) -> str:
    return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))

class Merkel_tree():
    def __init__(self,txids) -> None:
        self.txids = [reverse_hex(txid) for txid in txids]

        self.root = self.build_tree(self.txids)

    def build_tree(self, txids):
        if len(txids) == 1:
            return txids[0]

        new_level = []
        for i in range(0, len(txids), 2):
            one = txids[i]
            two = txids[i + 1] if i + 1 < len(txids) else txids[i]
            concat = one + two
            hashed = hash256(concat)
            new_level.append(hashed)

        return self.build_tree(new_level)
    
    def find_root(self):
        return reverse_hex(self.root)

    def get_proof(self,txids:list, target_tx:str, path:list,level=0):

        if len(txids) == 1:
            path.append(txids[0])
            return 

        new_level = []
        for i in range(0, len(txids), 2):
            one = txids[i]
            two = txids[i + 1] if i + 1 < len(txids) else txids[i]
            
            
            concat = one + two
            hashed = hash256(concat)
            new_level.append(hashed)
            if one == target_tx:
                path.append(two)
            elif two == target_tx:
                path.append(one)
            if one ==target_tx or two==target_tx:
                target_tx = hashed


        return self.get_proof(new_level,target_tx,path,level+1)
    
    def verify_proof(self,ind,current,proof:list):
        if len(proof) == 1:
            return current == proof[0]
        
        if ind % 2 == 0:
            one = current
            two = proof.pop()
        else:
            one = proof.pop()
            two = current

        concat = one + two
        current = hash256(concat)
        new_ind =  ind//2
        return self.verify_proof(new_ind,current,proof)

    

def main():
    command = input()
    if command == 'root':
        n = int(input())
        tx = []
        for i in range(n):
            tx.append(input())
        mtree = Merkel_tree(tx)
        print(mtree.find_root())

    elif command == 'path':
        ind = int(input())
        n = int(input())
        tx = []
        for i in range(n):
            tx.append(input())
        mtree = Merkel_tree(tx)
        path = []
        mtree.get_proof(mtree.txids,mtree.txids[ind],path)
        print('\n\n\n')
        for tx in path:
            print(tx)

    else:
        ind = int(input())
        merkel_root = input()
        p = int(input())
        siblings = []
        for i in range(p):
            siblings.append(input())
        n = int(input())
        tx = []
        for i in range(n):
            tx.append(input())
        mtree = Merkel_tree(tx)
        siblings.reverse()
        res = mtree.verify_proof(ind,mtree.txids[ind],siblings)
        print('verify' if res else 'invalid')

if __name__ == "__main__":
    # main()
    import json
    with open('src/3/hash.json', 'r') as f:
        hashes = json.load(f)
    merkel_root = "f8ea455b494fd54255bb495e53f4bc4e6e15ff9985a3df7712b627cca862ead5"
    merkel_tree = Merkel_tree(hashes)
    print(merkel_tree.find_root())
    print(merkel_root==merkel_tree.find_root())
    path = []
    merkel_tree.get_proof(merkel_tree.txids,merkel_tree.txids[5],path)
    print(path)
    path.reverse()
    print(merkel_tree.verify_proof(5,merkel_tree.txids[5],path))