import base64
import json
from .cryptolib import RSA, PKA, DES

def main():
    rsa = RSA()
    pka = PKA()

    message = "12345"
    public_key, private_key = rsa.generate_keys()
    test_pub, test_priv = rsa.generate_keys()

    encrypted_message = rsa.encrypt2(message, private_key)
    print("encrypted message: ", encrypted_message)

    second_encrypt = rsa.encrypt2(str(encrypted_message), test_pub)
    print("2nd encrypted message: ", second_encrypt)

    decrypted_message = rsa.decrypt2(encrypted_message, test_priv)
    print("decryptred message: ", decrypted_message)

    second_decrypted_message = rsa.decrypt2(int(decrypted_message), public_key)
    print("decryptred message: ", second_decrypted_message)
    print("==========================================")

    # # Test dengan kunci baru
    # print("Test public key: ", test_pub)

    # # Konversi public key ke string JSON agar dapat dienkripsi
    # message = json.dumps(test_pub)  

    # # Enkripsi public key dari pasangan test_pub menggunakan public_key
    # encrypted_message = rsa.encrypt(message, public_key)
    # print("encrypted message: ", encrypted_message)

    # # Dekripsi kembali menggunakan private_key
    # decrypted_message = rsa.decrypt(encrypted_message, private_key)

    # # Parse kembali ke bentuk tuple menggunakan json.loads
    # decrypted_public_key = json.loads(decrypted_message)
    # print("decrypted public key: ", decrypted_public_key)

    # # Encode hasil dekripsi ke Base64 untuk tujuan representasi aman
    # base64_message = base64.b64encode(decrypted_message.encode('utf-8')).decode('utf-8')
    # print("Base64 message:", base64_message)


if __name__ == '__main__':
    main()