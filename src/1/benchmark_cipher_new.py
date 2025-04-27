import time
import secrets
from Part1_DES import DES
from Part1_AES import AES
from Part2_RSA import RSA
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import ceil

def bench(name,cipher_tuple,tests):
    cipher = cipher_tuple[0](*cipher_tuple[1])
    enc_times = []
    dec_times = []
    for test in tests:
        start = time.time()
        cipher_text = cipher.encrypt(test)
        end = time.time()
        enc_times.append(end-start)
        start = time.time()
        plain = cipher.decrypt(cipher_text)
        end = time.time()
        dec_times.append(end-start)
    return name,(sum(enc_times)/len(enc_times),sum(dec_times)/len(dec_times))

def main():
    n_tests = 15
    tests = []
    for _ in range(n_tests):
        tests.append(secrets.token_bytes(1024))


    results = {}


    des_key = secrets.token_bytes(8)   
    aes128_key = secrets.token_bytes(16) 
    aes192_key = secrets.token_bytes(24)  
    aes256_key = secrets.token_bytes(32)  

    ciphers = {
        "DES": (DES,(des_key, "standard")),
        "DES_Xor_based": (DES,(des_key, "xor_based")),
        "AES-128": (AES,(aes128_key,)),
        "AES-192": (AES,(aes192_key,)),
        "AES-256": (AES,(aes256_key,)),
        "RSA-1024": (RSA,(2024,)),
        "RSA-3072": (RSA,(3072,)),
        # "RSA-7680": (RSA,(7680,)),
        # "RSA-15360": (RSA,(15360,)),
    }

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(bench, cipher_name, obj, tests): cipher_name
            for cipher_name, obj in ciphers.items()
        }


        results = {}
        for future in as_completed(futures):
            cipher_name, result = future.result()  
            results[cipher_name] = result 
    
    print(f"{'Algo':<15} {'Enc(ms)':>8} {'Dec(ms)':>8}")
    print("-"*60)
    for name, vals in results.items():
        e,d = vals
        print(f"{name:<15} {e*1000:8.3f} {d*1000:8.3f}")

if __name__=="__main__":
    main()

# | RSA Key Size | Equivalent AES Key Size |
# |--------------|-------------------------|
# | 1024 bits    | 80 bits (no longer secure) |
# | 2048 bits    | 112 bits                |
# | 3072 bits    | 128 bits                |
# | 7680 bits    | 192 bits                |
# | 15360 bits   | 256 bits                |
    
# Algo             Enc(ms)  Dec(ms)
# ------------------------------------------------------------
# DES_Xor_based     74.687   73.592
# AES-128           22.763  162.454
# AES-192           33.628  230.193
# AES-256           32.483  233.037
# DES              143.949  143.478
# RSA-1024           1.817  596.200
# RSA-3072           2.829 1250.222