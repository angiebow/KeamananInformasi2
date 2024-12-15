import base64
import os
import socket
import random

import threading
import time
from des.DES import DES
from des.utils import pad_string, bin_to_text
from ..cryptolib import RSA

IP = "127.0.0.1"
PORT = 65431
DES_KEY = None
RECIPIENT = None
online_users = {}

def encrypt_des(message):
    global DES_KEY
    des_instance = DES(int(DES_KEY))
    message_bin = pad_string(message)
    encrypted_chunks = [
        des_instance.encrypt(message_bin[i:i+64]) for i in range(0, len(message_bin), 64)
    ]
    encrypted_message = ''.join(encrypted_chunks)
    return encrypted_message

def decrypt_des(encrypted_message, key):
    try:
        des_instance = DES(int(key))
        decrypted_chunks = [
            des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
        ]
        decrypted_binary = ''.join(decrypted_chunks)
        decrypted_message = bin_to_text(decrypted_binary)
    except Exception as e:
        print("Error decrypting message: ", e)
        return ""
    return decrypted_message

def receive_messages(sock, rsa, client_private_key, once=False):
    """Listen for messages from the server and print them."""
    global online_users, RECIPIENT
    while True:
        try:
            message = sock.recv(2048).decode()
            # print("\033[F\033[K", end="")
            # print("Received message: ", message)
            if "<KEY START>" in message:
                message = message.replace("<KEY START>", "")
                if "<KEY END>" in message:
                    message = message.replace("<KEY END>", "")
                if once:
                    # print("Received private key: ", message)
                    return message
                print("\r" + f"other key: {message}")
            elif message.startswith("NEW_CLIENT"):
                _, username,  public_key = message.split('|')
                online_users[username] = {'key': str(public_key)}
                # print(f"New client online: {username}")
            elif message.startswith("EXISTING_CLIENT"):
                _, username,  public_key = message.split('|')
                online_users[username] = {'key': str(public_key)}
                # print(f"Existing client online: {username}")
            elif message.startswith("MESSAGE"):
                print("\033[F\033[K", end="")   
                # print("message: ", message)
                try:
                    _, sender,  key, encrypted_message = message.split('|')
                    # first_decrypt = rsa.decrypt(int(key), client_private_key)
                    second_decrypt = rsa.decrypt(int(key), eval(online_users[sender]['key']))
                    # print(f"Received DES key: {second_decrypt}")
                    decrypted_message = decrypt_des(encrypted_message, second_decrypt)
                    print(f"{sender}: {decrypted_message}")
                    print("====================================")
                except Exception as e:
                    print("Error decrypting message: ", e)
            elif message == "":
                print("Received empty message.")
                break
            
            if RECIPIENT:
                print("\nYou: ", end="", flush=True)
            else:
                usernames = list(online_users.keys())
                print("\r"+f"Online users: {' | '.join(usernames)}")
                print("Enter recipient username up: ", end="", flush=True)
        except Exception as e:
            print("Error receiving message: ", e)
            break

def main():
    global DES_KEY, online_users, RECIPIENT
    DES_KEY = random.randint(100000, 999999)
    print(f"Created DES key: {DES_KEY}")
    des_instance = DES(int(DES_KEY))

    rsa = RSA()
    client_private_key, client_public_key = rsa.generate_keys()
    # print("RSA key has been created.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((IP, PORT))

        n1 = random.randint(100000, 999999)
        conn.sendall(str(n1).encode())

        msg = conn.recv(1024).decode()
        server_n1, n2 = msg.split('|')
        if int(server_n1) != n1:
            print("Error: n1 mismatch.")
            return
        
        message = f"{n1}|{n2}"
        conn.sendall(message.encode())
        
        msg = conn.recv(1024).decode()
        if msg == "OK":
            print("Connection verified.")
        else:
            print(f"Error: {msg}.")
            return

        # Receive private key from the server
        server_key = receive_messages(conn, rsa, client_private_key, True)
        print("server key: ", server_key)

        while True:
            # Send username to the server
            username = input("Enter your username: ")
            conn.sendall(username.encode())
            msg = conn.recv(1024).decode()
            if msg == "OK":
                break
            else:
                print(msg)

        # Send public key to the server after encrypt it with server's public key
        conn.sendall(str(client_public_key).encode())

        print("Connected to the server.")

        # Start a thread to receive messages
        threading.Thread(target=receive_messages, args=(conn, rsa, client_private_key,), daemon=True).start()

        while True:
            
            while len(online_users) < 1:
                print("Waiting for other users to come online...")
                time.sleep(5)

            usernames = list(online_users.keys())
            # print("\033[F\033[K", end="")
            print(f"Online users: {' | '.join(usernames)}")            
            RECIPIENT = input("Enter recipient username up down: ")
            if RECIPIENT not in online_users:
                print(f"Error: {RECIPIENT} not online.")
                continue
        

            recipient_public_key = online_users[RECIPIENT]['key']
            first_encription = rsa.encrypt(str(DES_KEY), client_private_key)
            # second_encription = rsa.encrypt(str(first_encription), eval(recipient_public_key))
            # print(f"Encrypted DES key: {base64.b64encode(encrypted_key).decode()}   ")

            message = input("You: ")
            print("===============================")
            padded_message = pad_string(message)
            encrypted_chunks = [
                des_instance.encrypt(padded_message[i:i+64]) for i in range(0, len(padded_message), 64)
            ]

            encrypted_message = ''.join(encrypted_chunks)
            formatted_message = f"MESSAGE|{username}|{first_encription}|{encrypted_message}"
            conn.sendall(formatted_message.encode())
            RECIPIENT = None

if __name__ == "__main__":
    main()
