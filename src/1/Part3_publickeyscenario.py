from Part2_RSA import RSA
def main():
    alice_rsa = RSA(128)
    bob_rsa = RSA(128)

#   alice want to send a message to bob
    message = 'hello bob'.encode('utf-8')
    """
    1- Confidentiality
    """
    print('Confidentiality')
    alice_cipher = bob_rsa.encrypt(message)
    print(alice_cipher.hex())
    # send the text to bob
    bob_plaintext = bob_rsa.decrypt(alice_cipher)
    print(bob_plaintext.decode('utf-8'))
    """
    2 - Authentication
    """
    print('Authentication')
    alice_cipher = alice_rsa.encrypt(message)
    print(alice_cipher.hex())
    # send to bob
    bob_plaintext = alice_rsa.decrypt(alice_cipher)
    print(bob_plaintext.decode('utf-8'))
    """
    3- Confidentiality + Authentication
    """
    print('Confidentiality + Authentication')
    alice_cipher = alice_rsa.encrypt(message)
    bob_alice_cipher = bob_rsa.encrypt(alice_cipher)
    print(bob_alice_cipher.hex())
    bob_alice_plaintext = bob_rsa.decrypt(bob_alice_cipher)
    bob_plaintext = alice_rsa.decrypt(bob_alice_plaintext)
    print(bob_plaintext.decode('utf-8'))


main()    