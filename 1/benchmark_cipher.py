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

def benchmark_symmetric(cipher, data, iterations=1000):
    """Benchmark symmetric encryption."""
    def _encrypt():
        cipher.encrypt(data)
    return timeit.timeit(_encrypt, number=iterations)/iterations

def benchmark_rsa(cipher, data, iterations=100):
    """Benchmark RSA encryption (fewer iterations due to slowness)."""
    def _encrypt():
        cipher.encrypt(data[:cipher.n.bit_length()//8-11])  # RSA block size
    return timeit.timeit(_encrypt, number=iterations)/iterations

def main():
    # Generate random keys
    des_key = get_random_bytes(8)   # DES key (8 bytes)
    aes128_key = get_random_bytes(16)  # AES-128 key (16 bytes)
    aes192_key = get_random_bytes(24)  # AES-192 key (24 bytes)
    aes256_key = get_random_bytes(32)  # AES-256 key (32 bytes)

    # Initialize ciphers
    des_cipher = DES(des_key, "standard")
    aes128_cipher = AES(aes128_key)
    aes192_cipher = AES(aes192_key)
    aes256_cipher = AES(aes256_key)
    rsa_1024 = RSA(1024)
    rsa_2048 = RSA(2048)

    # Generate test data (smaller for RSA)
    sym_data = generate_random_string(1024)  # 1KB for symmetric
    rsa_data = generate_random_string(100)   # 100B for RSA (max 117B for 1024-bit)

    # Benchmark parameters
    sym_iterations = 1000
    rsa_iterations = 100

    print("Running benchmarks... (this may take a while)")

    # Benchmark each algorithm
    results = {
        "DES": benchmark_symmetric(des_cipher, sym_data, sym_iterations),
        "AES-128": benchmark_symmetric(aes128_cipher, sym_data, sym_iterations),
        "AES-192": benchmark_symmetric(aes192_cipher, sym_data, sym_iterations),
        "AES-256": benchmark_symmetric(aes256_cipher, sym_data, sym_iterations),
        "RSA-1024": benchmark_rsa(rsa_1024, rsa_data, rsa_iterations),
        "RSA-2048": benchmark_rsa(rsa_2048, rsa_data, rsa_iterations),
    }

    # Print results
    print("\nBenchmark Results (seconds per operation):")
    print("-----------------------------------------")
    for algo, time_taken in sorted(results.items(), key=lambda x: x[1]):
        print(f"{algo:<8}: {time_taken:.6f} sec")

if __name__ == "__main__":
    main()