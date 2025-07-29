import time
import timeit
from Crypto.Random import get_random_bytes
from Part1_AES import AES
from Part1_DES import DES
from Part2_RSA import RSA
import random
import string

def generate_random_string(length=1024):  # Smaller for RSA compatibility
    """Generate a random string of given length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length)).encode('utf-8')

def main():
    # Generate random keys
    des_key = get_random_bytes(8)   # DES key (8 bytes)
    aes128_key = get_random_bytes(16)  # AES-128 key (16 bytes)
    aes192_key = get_random_bytes(24)  # AES-192 key (24 bytes)
    aes256_key = get_random_bytes(32)  # AES-256 key (32 bytes)

    # Generate test data (smaller for RSA)
    data = generate_random_string(4096)

    print("Running benchmarks... (this may take a while)")

    # Benchmark each algorithm
    ciphers = {
        "DES": (DES,(des_key, "standard")),
        "AES-128": (AES,(aes128_key,)),
        "AES-192": (AES,(aes192_key,)),
        "AES-256": (AES,(aes256_key,)),
        "RSA-1024": (RSA,(1024,)),
        "RSA-2048": (RSA,(2048,)),
    }
    results = {}
    for cipher in ciphers:
        tupl = ciphers[cipher]
        start = time.time()
        algo = tupl[0](*tupl[1])
        algo.encrypt(data)
        end = time.time()
        results[cipher] = end-start

    # Print results
    print("\nBenchmark Results (seconds per operation):")
    print("-----------------------------------------")
    for algo, time_taken in sorted(results.items(), key=lambda x: x[1]):
        print(f"{algo:<8}: {time_taken:.6f} sec")

if __name__ == "__main__":
    main()