#broadcaster.py
import socket
import threading
from ..cryptolib import RSA  
from des.DES import DES
from des.utils import pad_string, bin_to_text
import os
import random

IP = "127.0.0.1"
PORT = 65431

clients = {}
DES_KEY = 123123 

def encrypt_des(message):
    des_instance = DES(int(DES_KEY))
    message_bin = pad_string(message)
    encrypted_chunks = [
        des_instance.encrypt(message_bin[i:i+64]) for i in range(0, len(message_bin), 64)
    ]
    encrypted_message = ''.join(encrypted_chunks)
    return encrypted_message

def decrypt_des(encrypted_message):
    des_instance = DES(int(DES_KEY))
    decrypted_chunks = [
        des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
    ]
    decrypted_binary = ''.join(decrypted_chunks)
    decrypted_message = bin_to_text(decrypted_binary)
    return decrypted_message

def broadcast(message, current_username):
    print(f"Broadcasting: {message}")
    for username in clients:
        # print(f"Broareceive_messagesdcasting to {username} | {client_info}")
        if username != current_username:
            try:
                clients[username]['conn'].sendall(message.encode())
            except Exception as e:
                print(f"Error broadcasting to {username}: {e}")
                del clients[username]

def handle_client(conn, addr, private_key, public_key):
    global DES_KEY, clients

    try:
        msg = conn.recv(1024).decode()
        n1 = msg
        n2 = str(random.randint(100000, 999999))
    except Exception as e:
        print(f"Error receiving n1: {e}")
        conn.close()
        return
    
    try:
        message = f"{n1}|{n2}"
        conn.sendall(message.encode())
    except Exception as e:
        print(f"Error sending n1 and n2 to {addr}: {e}")
        conn.close()
        return
    
    try: 
        msg = conn.recv(1024).decode()
        client_n1, client_n2 = msg.split("|")
        if client_n1 == n1 and client_n2 == n2:
            conn.sendall("OK".encode())
            print("Client authenticated.")
        else:
            conn.sendall("Invalid authentication.".encode())
            conn.close()
            return
    except Exception as e:
        print(f"Error authenticating client: {e}")
        conn.close()
        return

    try:
        public_key_msg = "<KEY START>" + str(public_key) + "<KEY END>"
        # print(f"Public Key {public_key_msg}")
        conn.sendall(public_key_msg.encode())
        print(f"Successfully sent the server's public key.")
    except Exception as e:
        print(f"Error sending server's public key")
        conn.close()
        return

    # Receive client username
    while True:
        msg = conn.recv(1024).decode()
        if msg in clients:
            print(f"Username '{msg}' already exists.")
            conn.sendall("Username already exists. Please choose another one.".encode())
        else:
            conn.sendall("OK".encode())
            username = msg
            
            # Initialize the client's dictionary entry
            clients[username] = {'conn': conn}
            print(f"Received username: {username} | client : {len(clients)}")
            break

    # Receive client's public key
    try:
        msg = conn.recv(1024).decode()
        print(f"Received client's public key: {msg}")
        clients[username]['public_key'] = str(msg)
        # print(f"Received client's public key: {client_public_key}")
    except Exception as e:
        print(f"Error receiving client's public key: {e}")
        conn.close()
        return

    # Send the new client's public key to all previously connected clients
    for user in clients:
        if user != username:
            clients[user]['conn'].sendall(f"NEW_CLIENT|{username}|{clients[username]['public_key']}".encode())
    print(f"Sent new client's public key to all existing clients.")
    
    # Send all previously connected clients' public keys to the new client
    for user in clients:
        if user != username:
            conn.sendall(f"EXISTING_CLIENT|{user}|{clients[user]['public_key']}".encode())
    print(f"Sent all existing clients' public keys to the new client.")

    print("========================================")

    while True:
        try:
            message = conn.recv(2048).decode()
            if not message:
                break
            print(f"Message from {username}: {message}")

            # Broadcast decrypted message to all clients
            broadcast(message, username)
            print("========================================")
        except ConnectionResetError:
            break

    del clients[username]
    conn.close()
    print(f"Client {username} disconnected.")

def main():
    rsa = RSA()
    public_key, private_key = rsa.generate_keys()
    print("public key: ", public_key)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print("Server listening for connections...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, private_key, public_key)).start()

if __name__ == "__main__":
    main()
