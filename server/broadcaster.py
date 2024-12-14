#broadcaster.py
import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from des.DES import DES
from des.utils import bin_to_text, pad_string
import os

IP = "127.0.0.1"
PORT = 65432

clients = {}
DES_KEY = 123123 

def encrypt_des(message, des_key):
    des_instance = des_key
    message_bin = pad_string(message)
    encrypted_chunks = [
        des_instance.encrypt(message_bin[i:i+64]) for i in range(0, len(message_bin), 64)
    ]
    encrypted_message = ''.join(encrypted_chunks)
    return encrypted_message

def decrypt_des(encrypted_message, des_key):
    des_instance = des_key
    decrypted_chunks = [
        des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
    ]
    decrypted_binary = ''.join(decrypted_chunks)
    decrypted_message = bin_to_text(decrypted_binary)
    return decrypted_message

def encrypt_rsa(message, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher_rsa.encrypt(message.encode())
    return encrypted_message

def decrypt_rsa(encrypted_message, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa.decrypt(encrypted_message)
    return decrypted_message

def delete_key_pair(name):
    private_key_path = os.path.join("server/private", f"{name}.pem")
    public_key_path = os.path.join("server/public", f"{name}.pem")

    try:
        if os.path.exists(private_key_path):
            os.remove(private_key_path)
            print(f"Deleted private key for {name}")
        if os.path.exists(public_key_path):
            os.remove(public_key_path)
            print(f"Deleted public key for {name}")
    except Exception as e:
        print(f"Error deleting keys for {name}: {e}")

def broadcast(message, current_username):
    print(f"Broadcasting: {message}")
    for username, client_info in clients.items():
        # print(f"Broadcasting to {username} | {client_info}")
        if username != current_username:
            try:
                encrypted_message = encrypt_des(message, client_info['des'])
                client_info['conn'].sendall(encrypted_message.encode())
            except Exception as e:
                print(f"Error broadcasting to {username}: {e}")
                del clients[username]

def handle_client(conn, addr):
    global DES_KEY
    print(f"Client {addr} connected.")

    # Receive username
    while True:
        msg = conn.recv(1024).decode()
        if msg in clients:
            print(f"Username {msg} already exists.")
            conn.sendall("Username already exists. Please choose another one.".encode())
            msg = ""
        else:
            conn.sendall("OK".encode())
            username = msg
            # Initialize the client's dictionary entry
            clients[username] = {'conn': conn}
            print(f"Received username: {username} | client : {len(clients)}")
            break

    generate_key_pair(f"{username}")

    # Send server's public key to the client
    public_key_path = "server/public/server.pem"

    try:
        with open(public_key_path, "rb") as pub_file:
            public_key = pub_file.read()
            conn.sendall(public_key)
        print(f"Server's public key sent to {username}.")
    except FileNotFoundError:
        print("Server public key not found.")
        delete_key_pair(username)
        del clients[username]
        conn.close()
        return

    # Receive DES key from the client
    encrypted_key = conn.recv(256)  
    private_key_path = "server/private/server.pem"
    try:
        with open(private_key_path, "rb") as priv_file:
            private_key = RSA.import_key(priv_file.read())
            DES_KEY = decrypt_rsa(encrypted_key, private_key)
        des_instance = DES(int(DES_KEY.decode()))
        clients[username]['des'] = des_instance
        print(f"Received DES key {username}: {DES_KEY.decode()}")
    except FileNotFoundError:
        print("Server private key not found.")
        delete_key_pair(username)
        del clients[username]
        conn.close()
        return

    # Send user's private key after encrypt it with the DES key
    user_private_key_path = f"server/private/{username}.pem"
    try:
        with open(user_private_key_path, "rb") as priv_file:
            user_private_key = priv_file.read()
        
        encrypted_private_key = encrypt_des(("<KEY START>" + user_private_key.decode() + "<KEY END>"), des_instance)
        conn.sendall(encrypted_private_key.encode())
        print(f"Sent {username}'s private key to the client.")

        if len(clients) > 1:
            broadcast("<KEY START>" + user_private_key.decode() + "<KEY END>", username)
    except FileNotFoundError:
        print("User private key not found.")
        delete_key_pair(username)
        del clients[username]
        conn.close()
        return

    while True:
        try:
            encrypted_message = conn.recv(1024).decode()
            if not encrypted_message:
                break
            print(f"Encrypted message from {username}: {encrypted_message}")

            # Decrypt message
            decrypted_chunks = [
                des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
            ]
            decrypted_binary = ''.join(decrypted_chunks)
            decrypted_message = bin_to_text(decrypted_binary)
            print(f"Message from {addr}: {decrypted_message}")

            # Broadcast decrypted message to all clients
            broadcast(f"{username}: {decrypted_message}", username)
        except ConnectionResetError:
            break

    delete_key_pair(username)
    del clients[username]
    conn.close()
    print(f"Client {username} disconnected.")

def generate_key_pair(name):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Tentukan folder untuk penyimpanan
    public_folder = "server/public"
    private_folder = "server/private"

    # Buat folder jika belum ada
    os.makedirs(public_folder, exist_ok=True)
    os.makedirs(private_folder, exist_ok=True)

    # Simpan private key di folder private
    private_key_path = os.path.join(private_folder, f"{name}.pem")
    with open(private_key_path, "wb") as priv_file:
        priv_file.write(private_key)

    # Simpan public key di folder public
    public_key_path = os.path.join(public_folder, f"{name}.pem")
    with open(public_key_path, "wb") as pub_file:
        pub_file.write(public_key)

    print(f"Key for {name} created successfully")

def main():
    generate_key_pair("server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print("Server listening for connections...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
