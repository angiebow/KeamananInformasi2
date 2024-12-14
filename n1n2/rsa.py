#rsa.py
class RSA:
    def __init__(self):
        self.p = 61
        self.q = 53
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 17  
        self.d = self.mod_inverse(self.e, self.phi) 
        
    def mod_inverse(self, a, m):
        """Compute the modular inverse of a under modulo m."""
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def encrypt(self, plaintext, public_key):
        e, n = public_key
        if isinstance(plaintext, int): 
            plaintext_int = plaintext
        else: 
            plaintext_int = int.from_bytes(plaintext.encode('utf-8'), 'big')
        ciphertext_int = pow(plaintext_int, e, n)
        return ciphertext_int

    def decrypt(self, ciphertext):
        plaintext_int = pow(ciphertext, self.d, self.n)
        try:
            plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big').decode('utf-8')
        except UnicodeDecodeError:
            plaintext = plaintext_int
        return plaintext

    def get_public_key(self):
        """Return the public key (e, n)."""
        return (self.e, self.n)
