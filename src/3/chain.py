import hashlib
import time
import hashlib
from merkel import Merkel_tree

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

    def get_proof(self,txids:list, index:int, path:list):
        if len(txids) == 1:
            path.append(txids[0])
            return 
        flag = index % 2
        new_index = 0

        new_level = []
        for i in range(0, len(txids), 2):
            one = txids[i]
            two = txids[i + 1] if i + 1 < len(txids) else txids[i]
            
            
            concat = one + two
            hashed = hash256(concat)
            new_level.append(hashed)

            if i == index - flag:
                t = [one,two]
                path.append(t[not flag])
                new_index = len(new_level) - 1

        return self.get_proof(new_level,new_index,path)
    
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
    

def calculate_sha256(data_string:str)->str:
    """
    Calculates the SHA256 hash of a given string.
    Ensures the input is encoded to bytes before hashing.
    """
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

class Block:
    def __init__(self, index, transactions, previous_hash):
        """
        Initializes a new Block.

        Args:
            index (int): The position of the block in the chain.
            transactions (list of str): A list of transaction strings for this block.
            previous_hash (str): The SHA256 hash of the previous block.
        """
        self.ind = index
        self.trs = transactions
        self.prev = previous_hash
        self.transactions = transactions
        transactions_ids = [calculate_sha256(transaction) for transaction in transactions]
        self.merkel_tree = Merkel_tree(transactions_ids)
        self.nonce = 0
        self.time = time.time()
        self.hash = None

    def calculate_merkle_root(self):
        """
        Calculates the Merkle root of the block's transactions for any number of transactions.
        If there are no transactions, returns an empty string.
        If there's only one transaction, its hash is the Merkle root.
        Otherwise, builds the Merkle tree iteratively.
        """      
        return self.merkel_tree.find_root()

    def calculate_hash(self):
        """
        Calculates the SHA256 hash of the entire block.
        Combines all block attributes into a single string for hashing.
        The nonce is included as it's modified during Proof-of-Work.
        """
        hash_str = str(self.ind) + str(self.prev) + str(self.calculate_merkle_root()) + str(self.nonce) + str(self.time)
        return calculate_sha256(hash_str)

class Blockchain:

    def __init__(self):
        """
        Initializes the Blockchain.
        Sets the difficulty for Proof-of-Work and creates the genesis block.
        """
        self.difficulty = 1
        self.chain:list[Block] = []
        self.target = 2**(256 - self.difficulty)
        self.chain.append(self.create_genesis_block())

    def create_genesis_block(self):
        """
        Creates the very first block in the blockchain (the genesis block).
        It has index 0, a "0" previous hash, and initial transactions.
        The genesis block must also be mined.
        """
        gen_block = Block(0,["TX-000: Initial Coin Generation (50 BTC to GenesisMiner)","TX-000: Network Protocol Version 1.0 Activated","TX-000: Initial Block Reward Set to 50 BTC"],'0')
        self.mine_block(gen_block)
        return gen_block

    def get_latest_block(self):
        """
        Returns the most recently added block in the chain.
        """
        return self.chain[-1]

    def mine_block(self, block:Block):
        """
        Performs the Proof-of-Work (mining) for a given block.
        It increments the block's nonce until a hash meeting the difficulty
        requirement (starting with 'difficulty' number of zeros) is found.

        Args:
            block (Block): The Block object to be mined.
        """
        block.nonce = 0
        while True:
            block_hash = int(block.calculate_hash(),16)
            if block_hash <= self.target:
                block.hash = block.calculate_hash()
                break
            block.nonce += 1

    def add_block(self, transactions):
        """
        Adds a new block to the blockchain.
        The new block is mined before being added to the chain.

        Args:
            transactions (list of str): A list of transaction strings for the new block.
        """
        block = Block(len(self.chain),transactions,self.chain[-1].hash)
        self.mine_block(block)
        self.chain.append(block)

    def is_chain_valid(self):
        """
        Checks the integrity of the entire blockchain.
        Verifies previous hash links, re-calculates each block's hash,
        and checks if the block's hash meets the Proof-of-Work difficulty.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            current_hash = int(current_block.calculate_hash(), 16)
            if current_hash > self.target:
                print(f"Block {current_block.ind} has invalid Proof-of-Work.")
                return False


            if current_block.prev != previous_block.hash:
                print(f"Block {current_block.ind} has invalid previous_hash link.")
                return False


            recalculated_hash = current_block.calculate_hash()
            if recalculated_hash != current_block.hash:
                print(f"Block {current_block.ind} has been tampered with.")
                return False

            merkle_root = current_block.calculate_merkle_root()
            transactions_ids = [calculate_sha256(tx) for tx in current_block.transactions]
            if len(transactions_ids) == 0:
                expected_merkle = ''
            else:
                mt = Merkel_tree(transactions_ids)
                expected_merkle = mt.find_root()

            if merkle_root != expected_merkle:
                print(f"Block {current_block.ind} has an invalid Merkle root.")
                return False
        print("Blockchain is valid.")
        return True

# testing the blockchain
if __name__ == "__main__":

    print("Initializing new blockchain...")
    bc = Blockchain()

    # Add some blocks
    print("\nAdding Block 1...")
    bc.add_block(["TX-001: Alice sends 1 BTC to Bob", 
                  "TX-002: Bob sends 0.5 BTC to Charlie"])

    print("\nAdding Block 2...")
    bc.add_block(["TX-003: Charlie sends 0.2 BTC to Dan",
                  "TX-004: Miner reward of 50 BTC issued"])

    print("\nAdding Block 3...")
    bc.add_block(["TX-005: Dan buys coffee with 0.01 BTC",
                  "TX-006: Network fee collected: 0.001 BTC"])

    print("\nBlockchain built successfully.")
    

    print("\n=== Blockchain Details ===")
    for block in bc.chain:
        print(f"\nBlock {block.ind}")
        print(f"Timestamp: {block.time}")
        print(f"Previous Hash: {block.prev}")
        print(f"Merkle Root: {block.calculate_merkle_root()}")
        print(f"Nonce: {block.nonce}")
        print(f"Hash: {block.hash}")
        print("Transactions:")
        for tx in block.transactions:
            print(f" - {tx}")


    print("\nValidating blockchain...")
    bc.is_chain_valid()  


    print("\nTampering with Block 1...")
    bc.chain[1].transactions[0] = "TX-001: Alice steals 100 BTC from Bob"

    print("\nRevalidating tampered blockchain...")
    bc.is_chain_valid() 