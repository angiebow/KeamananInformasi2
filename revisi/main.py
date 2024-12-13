from rsa.key_generation import rsa_key_generation
from rsa.encryption import rsa_encrypt
from rsa.decryption import rsa_decrypt

def main():
    print("=== RSA Key Generation ===")
    public_key, private_key = rsa_key_generation()
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")

    message = "hello"
    print(f"\nOriginal Message: {message}")

    encrypted_message = rsa_encrypt(message, public_key)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = rsa_decrypt(encrypted_message, private_key)
    print(f"Decrypted Message: {decrypted_message}")

if __name__ == "__main__":
    main()
