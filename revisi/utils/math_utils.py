def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_euclidean(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0

def mod_inverse(e, phi):
    inv = extended_euclidean(e, phi)
    return inv % phi  
