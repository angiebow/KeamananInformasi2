#decryption.py
def rsa_decrypt(ciphertext, private_key):
    """Decrypt a message using RSA private key."""
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])