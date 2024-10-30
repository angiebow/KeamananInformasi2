# server/receiver.py
import socket
import threading
import os
import sys

sys.path.append(os.path.abspath('../'))
from des.DES import DES
from des.utils import bin_to_text

IP = "127.0.0.1"
PORT = 65432
DES_KEY = 12345678

clients = []  # Store active client connections

def broadcast(message, sender_conn):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)

def handle_client(conn, addr):
    """Handle communication with a client."""
    des_instance = DES(DES_KEY)
    print(f"Client {addr} connected.")
    while True:
        try:
            encrypted_message = conn.recv(1024).decode()
            if not encrypted_message:
                break  # Client disconnected

            print(f"Received encrypted message from {addr}: {encrypted_message}")
            decrypted_chunks = [
                des_instance.decrypt(encrypted_message[i:i+64]) for i in range(0, len(encrypted_message), 64)
            ]
            decrypted_binary = ''.join(decrypted_chunks)
            decrypted_message = bin_to_text(decrypted_binary)
            print(f"Message from {addr}: {decrypted_message}")

            broadcast(f"{addr}: {decrypted_message}", conn)  # Send message to other clients

        except ConnectionResetError:
            break  # Handle client disconnect

    print(f"Client {addr} disconnected.")
    clients.remove(conn)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print("Server listening for connections...")

        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
