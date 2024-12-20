import random
from Crypto.Util import number
import binascii


class RSA:
    def __init__(self, key_size=1024):
        self.key_size = key_size
        # self.e, self.d, self.n = self.generate_keys()

    def generate_keys(self):
        p = number.getPrime(self.key_size // 2)
        q = number.getPrime(self.key_size // 2)
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537  # Commonly used public exponent
        d = pow(e, -1, phi)

        public_key = (e, n)
        private_key = (d, n)
        return public_key, private_key

    def encrypt(self, plaintext, public_key):
        e, n = public_key
        plaintext_int = int.from_bytes(plaintext.encode('latin-1'), 'big')
        ciphertext_int = pow(plaintext_int, e, n)
        return ciphertext_int

    def decrypt(self, ciphertext, key):
        d, n = key
        plaintext_int = pow(ciphertext, d, n)
        plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
        return plaintext
    
    def encrypt2(self, plaintext, public_key):
        e, n = public_key
        chunk_size = (n.bit_length() - 1) // 8  # Limit based on RSA key size
        chunks = [plaintext[i:i+chunk_size] for i in range(0, len(plaintext), chunk_size)]
        encrypted_chunks = [pow(int.from_bytes(chunk.encode('utf-8'), 'big'), e, n) for chunk in chunks]
        return encrypted_chunks

    def decrypt2(self, encrypted_chunks, key):
        d, n = key
        decrypted_chunks = [
            pow(chunk, d, n).to_bytes((chunk.bit_length() + 7) // 8, 'big').decode('utf-8')
            for chunk in encrypted_chunks
        ]
        return ''.join(decrypted_chunks)

class DES:
    def __init__(self, key="1001100111"):
        self.key = key
        # Define the S-boxes and other DES operations here

    def encrypt(self, message):
        if not message:
            return None

        # Simple placeholder encryption logic, adjust as necessary
        encrypted_message = ''.join(format(ord(c), '08b') for c in message)
        return encrypted_message

    def decrypt(self, encrypted_message):
        if not encrypted_message:
            return None

        # Simple placeholder decryption logic
        decrypted_message = ''.join(chr(int(encrypted_message[i:i+8], 2)) for i in range(0, len(encrypted_message), 8))
        return decrypted_message


class PKA:
    def __init__(self):
        self.keys = {}

    def register(self, device_id, public_key):
        self.keys[device_id] = public_key

    def get_public_key(self, device_id):
        return self.keys.get(device_id)