from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_keys(private_key, public_key):
    with open("private.pem", "wb") as priv_file:
        priv_file.write(private_key)
    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key)

def load_public_key():
    with open("public.pem", "rb") as pub_file:
        return pub_file.read()

if __name__ == "__main__":
    priv_key, pub_key = generate_key_pair()
    save_keys(priv_key, pub_key)
    print("Public and private keys generated and saved.")