import socket
import random
import threading
from ..rsa.key_generation import generate_rsa_keys
from ..rsa.encryption import rsa_encrypt
from ..rsa.decryption import rsa_decrypt
from ..des.DES import DES

clients = {}
public_keys = {}

def handle_server_messages(client_socket, client_private_key, client_public_key):
    while True:
        try:
            response = client_socket.recv(1024).decode()
            print("response: ", response)
            if not response:
                break
            if response.startswith("NEW_CLIENT_USERNAME|"):
                new_client_username = response.split('|')[1]
                print(f"New client connected: {new_client_username}")
            elif response.startswith("EXISTING_CLIENT_USERNAME|"):
                existing_client_username = response.split('|')[1]
                print(f"Existing client: {existing_client_username}")
            elif response.startswith("NEW_CLIENT_PUB_KEY|"):
                new_client_public_key = eval(response.split('|')[1])
                # print(f"Received new client's public key: {new_client_public_key}")
            elif response.startswith("EXISTING_CLIENT_PUB_KEY|"):
                existing_client_public_key = eval(response.split('|')[1])
                # print(f"Received existing client's public key: {existing_client_public_key}")
            elif response.startswith("DES_KEY|"):
                sender_public_key_str, encrypted_des_key = response.split('|')[1:]
                sender_public_key = eval(sender_public_key_str)
                des_key = rsa_decrypt(rsa_decrypt(encrypted_des_key, client_private_key), sender_public_key)
                des_instance = DES(int(des_key))
                print(f"Received DES key: {des_key}")
            else:
                n1_received, n2, server_public_key_str = response.split('|')
                n1_received = int(n1_received)
                n2 = int(n2)
                server_public_key = eval(server_public_key_str)
                # print(f"Separated n1: {n1_received}, n2: {n2}, Server Public Key: {server_public_key}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12346))
        print("Connected to the server.")

        while True:
            # Send username to the server
            username = input("Enter your username: ")
            client_socket.sendall(username.encode())
            msg = client_socket.recv(1024).decode()
            if msg == "OK":
                break
            else:
                print(msg)

        client_public_key, client_private_key = generate_rsa_keys()
        # print(f"Client Public Key: {client_public_key}")
        # print(f"Client Private Key: {client_private_key}")

        n1 = random.randint(100000, 999999)
        # print(f"Generated n1: {n1}")

        message = f"{n1}|{client_public_key}"
        # print(f"Sending message: {message}")  # Debugging statement
        client_socket.send(message.encode())
        # print(f"Sent n1 and client public key to server: {message}")

        server_thread = threading.Thread(target=handle_server_messages, args=(client_socket, client_private_key, client_public_key), daemon=True)
        server_thread.start()

        while True:
            recipient = input("Enter recipient username: ")
            if recipient not in clients:
                print("Recipient not found.")
                continue

            des_key = random.randint(100000, 999999)
            encrypted_des_key = rsa_encrypt(rsa_encrypt(str(des_key), client_private_key), public_keys[recipient])
            clients[recipient]['conn'].send(f"DES_KEY|{client_public_key}|{encrypted_des_key}".encode())
            print(f"Sent DES key to {recipient}: {des_key}")

            message = input("Enter message: ")
            des_instance = DES(des_key)
            encrypted_message = des_instance.encrypt(message)
            clients[recipient]['conn'].send(encrypted_message.encode())
            print(f"Sent encrypted message to {recipient}: {encrypted_message}")

        server_thread.join()
        client_socket.close()

if __name__ == "__main__":
    start_client()
