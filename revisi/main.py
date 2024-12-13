from rsa.key_generation import rsa_key_generation, pka_key_generation
from rsa.encryption import rsa_encrypt
from rsa.decryption import rsa_decrypt

def main():
    print("=== PKA Key Generation ===")
    pka_public_key, pka_private_key = pka_key_generation()
    print(f"PKA Public Key (e, n): {pka_public_key}")
    print(f"PKA Private Key (d, n): {pka_private_key}\n")

    print("=== User Key Generation ===")
    user1_public_key, user1_private_key = rsa_key_generation()
    print(f"User1 Public Key (e, n): {user1_public_key}")
    print(f"User1 Private Key (d, n): {user1_private_key}\n")

    print("=== PKA Sends User1's Public Key ===")
    user1_key_encrypted = rsa_encrypt(str(user1_public_key), pka_private_key)
    print(f"Encrypted Public Key sent by PKA: {user1_key_encrypted}")

    print("\n=== User2 Decrypts the Public Key ===")
    user1_key_decrypted = rsa_decrypt(user1_key_encrypted, pka_public_key)
    print(f"Decrypted User1 Public Key: {user1_key_decrypted}")
