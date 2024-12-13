def pka_key_generation():
    """Generate PKA public and private keys."""
    p = 47
    q = 59

    n = p * q                 
    phi = (p - 1) * (q - 1)   

    e = 17
    if gcd(e, phi) != 1:
        raise ValueError("e and phi(n) are not coprime")

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key