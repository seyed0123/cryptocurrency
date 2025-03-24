import time
from Crypto.Random import get_random_bytes
from Part1_AES import AES
from Part1_DES import DES
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import string

def benchmark_encryption(algo_name, cipher, data, iterations=1000):
    """Benchmark encryption time for a given cipher."""
    start_time = time.time()
    for _ in range(iterations):
        cipher.encrypt(data[_])
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    return avg_time * 1000  # Convert to milliseconds
def generate_random_string(length=50):
    """Generate a random string of given length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length)).encode('utf-8')

def main():
    # Sample text to encrypt
    

    # Generate random keys
    des_key = get_random_bytes(8)  # DES key (8 bytes)
    aes128_key = get_random_bytes(16)  # AES-128 key (16 bytes)
    aes192_key = get_random_bytes(24)  # AES-192 key (24 bytes)
    aes256_key = get_random_bytes(32)  # AES-256 key (32 bytes)

    # Initialize ciphers
    des_cipher = DES(des_key,"standard")
    aes128_cipher = AES(aes128_key)
    aes192_cipher = AES(aes192_key)
    aes256_cipher = AES(aes256_key)

    # Benchmark each algorithm (1000 iterations)
    iterations = 1000
    plaintexts = [generate_random_string() for i in range(iterations)]
    tasks = [
            ("DES", des_cipher, plaintexts, iterations),
            ("AES-128", aes128_cipher, plaintexts, iterations),
            ("AES-192", aes192_cipher, plaintexts, iterations),
            ("AES-256", aes256_cipher, plaintexts, iterations),
        ]
    results = {}
    with ThreadPoolExecutor() as executor:
        future_to_algorithm = {
            executor.submit(benchmark_encryption, algorithm, cipher, plaintext, iterations): algorithm
            for algorithm, cipher, plaintext, iterations in tasks
        }
        for future in as_completed(future_to_algorithm):
            algorithm = future_to_algorithm[future]
            try:
                results[algorithm] = future.result()
            except Exception as e:
                print(f"Error during {algorithm} benchmark: {e}")

    # Print results
                
    print("\nBenchmark Results:\n-----------------------------")
    for algorithm, time_taken in results.items():
        print(f"{algorithm}: {time_taken:.4f} seconds")

if __name__ == "__main__":
    main()