#key_generation.py
import random
from .math_utils import gcd, mod_inverse

def rsa_key_generation():
    """Generate RSA public and private keys."""
    p = 61
    q = 53

    n = p * q                 
    phi = (p - 1) * (q - 1)   

    e = 17
    if gcd(e, phi) != 1:
        raise ValueError("e and phi(n) are not coprime")

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def generate_rsa_keys():
    """Generate PKA public and private keys."""
    p = random.choice([47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
    q = random.choice([101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151])

    n = p * q                 
    phi = (p - 1) * (q - 1)   

    e = random.choice([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
    while gcd(e, phi) != 1:
        e = random.choice([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key