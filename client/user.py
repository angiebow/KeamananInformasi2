import os
import socket
import random

import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from des.DES import DES
from des.utils import pad_string, bin_to_text

IP = "127.0.0.1"
PORT = 65432
DES_KEY = None  

def encrypt_rsa(message, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher_rsa.encrypt(message.encode())
    return encrypted_message

def decrypt_rsa(encrypted_message, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypt_message = cipher_rsa.decrypt(encrypted_message)
    return decrypt_message

def encrypt_des(message):
    global DES_KEY
    des_instance = DES(int(DES_KEY))
    message_bin = pad_string(message)
    encrypted_chunks = [
        des_instance.encrypt(message_bin[i:i+64]) for i in range(0, len(message_bin), 64)
    ]
    encrypted_message = ''.join(encrypted_chunks)
    return encrypted_message

def decrypt_des(encrypted_message):
    global DES_KEY
    try:
        des_instance = DES(int(DES_KEY))
        decrypted_chunks = [
            des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
        ]
        decrypted_binary = ''.join(decrypted_chunks)
        decrypted_message = bin_to_text(decrypted_binary)
    except Exception as e:
        print("Error decrypting message: ", e)
        return ""
    return decrypted_message

def receive_messages(sock, once=False):
    """Listen for messages from the server and print them."""
    while True:
        try:
            message = sock.recv(1024).decode()
            message = decrypt_des(message)
            # print("Received message: ", message)
            if "<KEY START>" in message:
                message = message.replace("<KEY START>", "")
                print("\033[K", end="")  
                while True:
                    buffer = sock.recv(1024).decode()
                    message += decrypt_des(buffer)
                    if "<KEY END>" in message:
                        message = message.replace("<KEY END>", "")
                        break
                if once:
                    print("Received private key: ", message)
                    return message
                print("\r" + f"other key: {message}")
                print("You: ", end="", flush=True)
            elif message:
                print("\033[K", end="")  
                print("\r" + f"msg: {message}") 
                print("You: ", end="", flush=True)
            else:
                print("exit receive message")
                break
        except Exception as e:
            print("Error receiving message: ", e)
            break

def main():
    
    global DES_KEY
    DES_KEY = random.randint(100000, 999999)
    print(f"Created DES key: {DES_KEY}")
    des_instance = DES(int(DES_KEY))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))

        while True:
            # Send username to the server
            username = input("Enter your username: ")
            s.sendall(username.encode())
            msg = s.recv(1024).decode()
            if msg == "OK":
                break
            else:
                print(msg)

        # Receive public key from the server
        public_key_pem = s.recv(1024)
        if not public_key_pem:
            print("Error: Failed to receive public key from server.")
            return

        server_key = RSA.import_key(public_key_pem)

        # Encrypt DES key using the received public key
        encrypted_des_key = encrypt_rsa(str(DES_KEY), server_key)
        s.sendall(encrypted_des_key)

        # Receive private key from the server
        user_private_key = receive_messages(s, True)

        print("Connected to the server.")

        # Start a thread to receive messages
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            message = input("You: ")
            padded_message = pad_string(message)
            encrypted_chunks = [
                des_instance.encrypt(padded_message[i:i+64]) for i in range(0, len(padded_message), 64)
            ]
            encrypted_message = ''.join(encrypted_chunks)
            s.sendall(encrypted_message.encode())
            # print("Encrypted message sent:", encrypted_message)

if __name__ == "__main__":
    main()
