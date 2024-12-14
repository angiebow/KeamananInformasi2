import socket
import random
import threading
from ..rsa.key_generation import generate_rsa_keys
from ..rsa.encryption import rsa_encrypt
from ..rsa.decryption import rsa_decrypt

clients = {}
public_keys = {}

def handle_client(client_socket, addr):
    global clients, public_keys

    print(f"Connection from {addr} has been established.")

    while True:
        msg = client_socket.recv(1024).decode()
        if msg in clients:
            print(f"Username {msg} already exists.")
            client_socket.sendall("Username already exists. Please choose another one.".encode())
            msg = ""
        else:
            client_socket.sendall("OK".encode())
            username = msg
            # Initialize the client's dictionary entry
            clients[username] = {'conn': client_socket}
            print(f"Received username: {username} | client : {len(clients)}")
            break

    # Notify all existing clients about the new client
    for user, client_info in clients.items():
        if user != username:
            client_info['conn'].send(f"NEW_CLIENT_USERNAME|{username}".encode())

    # Send all existing clients' usernames to the new client
    for user in clients:
        if user != username:
            client_socket.send(f"EXISTING_CLIENT_USERNAME|{user}|".encode())

    server_public_key, server_private_key = generate_rsa_keys()
    print(f"Server Public Key: {server_public_key}")
    print(f"Server Private Key: {server_private_key}")

    try:
        data = client_socket.recv(1024).decode()
        print(f"Received data: {data}")  # Debugging statement
        n1, client_public_key_str = data.split('|')
        n1 = int(n1)
        client_public_key = eval(client_public_key_str)
        print(f"Received n1 and client's public key: n1={n1}, client_public_key={client_public_key}")
    except Exception as e:
        print(f"Error parsing data: {e}")
        client_socket.close()
        return

    try:
        n2 = random.randint(100000, 999999)
        print(f"Generated n2: {n2}")

        message = f"{n1}|{n2}|{server_public_key}"
        client_socket.send(message.encode())
        print(f"Sent n1, n2, and server public key to client: {message}")

        # Send the new client's public key to all previously connected clients
        for user, client_info in clients.items():
            if user != username:
                client_info['conn'].send(f"NEW_CLIENT_PUB_KEY|{client_public_key}".encode())

        # Send all previously connected clients' public keys to the new client
        for pk in public_keys.values():
            client_socket.send(f"EXISTING_CLIENT_PUB_KEY|{pk}|".encode())

        # Add the new client and its public key to the lists
        clients[username]['public_key'] = client_public_key
        public_keys[username] = client_public_key

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Handle other communication if needed
            except Exception as e:
                print(f"Error during communication: {e}")
                break
    except Exception as e:
        print(f"Error during initial communication: {e}")

    client_socket.close()
    del clients[username]
    del public_keys[username]
    print(f"Connection from {addr} has been closed.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))
    server_socket.listen(5)
    print("Server listening on port 12346...")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
