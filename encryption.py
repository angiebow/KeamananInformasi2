from Crypto.Cipher import AES
import base64

key = b'Sixteen byte key'
iv = b'Sixteen byte IV '

def encrypt_string(plain_text):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_bytes = cipher.encrypt(plain_text.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_string(encrypted_text):
    encrypted_bytes = base64.b64decode(encrypted_text)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    return decrypted_bytes.decode('utf-8')