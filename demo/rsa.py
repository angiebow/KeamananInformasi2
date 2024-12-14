#rsa.py
import random
from Crypto.Util import number

class RSA:
    def __init__(self, key_size=1024):
        self.key_size = key_size
        self.e, self.d, self.n = self.generate_keys()

    def generate_keys(self):
        p = number.getPrime(self.key_size // 2)
        q = number.getPrime(self.key_size // 2)
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537  
        d = pow(e, -1, phi)

        return e, d, n

    def encrypt(self, plaintext, public_key):
        e, n = public_key
        plaintext_int = int.from_bytes(plaintext.encode('utf-8'), 'big')
        ciphertext_int = pow(plaintext_int, e, n)
        return ciphertext_int

    def decrypt(self, ciphertext):
        plaintext_int = pow(ciphertext, self.d, self.n)  
        return plaintext_int  


    def get_public_key(self):
        return (self.e, self.n)