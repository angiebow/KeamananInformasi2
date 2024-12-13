#encryption.py
def rsa_encrypt(message, public_key):
    """Encrypt a message using RSA public key."""
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]