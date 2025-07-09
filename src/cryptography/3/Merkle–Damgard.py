import random

p = 23
q = (p - 1) // 2
A = 5
b_secret = random.randint(1, q - 1)
B = pow(A, b_secret, p)


def round_hash(x1, x2):
    a_term = pow(A, x1, p)
    b_term = pow(B, x2, p)
    return (a_term * b_term) % p


def bytes_to_blocks(data, block_size=2):
    blocks = []
    for i in range(0, len(data), block_size):
        x1 = data[i] if i < len(data) else 0
        x2 = data[i+1] if i+1 < len(data) else 0
        blocks.append((x1 % q, x2 % q))  # map to Z_q
    return blocks

def merkle_damgard_hash(data: bytes):
    # Initial hash value (IV)
    h = 1  # or use a random q-sized value
    blocks = bytes_to_blocks(data)

    for x1, x2 in blocks:

        x1 = (x1 ^ h) % q
        h = round_hash(x1, x2)

    return h

msg = b"hello world"
digest = merkle_damgard_hash(msg)
print(f"Hash of '{msg.decode()}': {digest}")