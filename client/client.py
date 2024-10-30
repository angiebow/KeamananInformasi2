# client/sender.py
import socket
import threading
import os
import sys

sys.path.append(os.path.abspath('../'))
from des.DES import DES
from des.utils import pad_string

IP = "127.0.0.1"
PORT = 65432
DES_KEY = 12345678

def receive_messages(sock, des_instance):
    """Receive and decrypt messages from the server."""
    while True:
        try:
            encrypted_message = sock.recv(1024).decode()
            if not encrypted_message:
                break

            # Display received message (already decrypted by the server)
            print(f"\n{encrypted_message}")
        except:
            print("Disconnected from server.")
            break

def send_messages(sock, des_instance):
    """Send encrypted messages to the server."""
    while True:
        message = input()  # Take input from the user
        padded_message = pad_string(message)

        encrypted_chunks = [
            des_instance.encrypt(padded_message[i:i+64]) for i in range(0, len(padded_message), 64)
        ]
        encrypted_message = ''.join(encrypted_chunks)
        sock.sendall(encrypted_message.encode())

def main():
    des_instance = DES(DES_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        print("Connected to the server.")
        print("Write a message and press Enter to send it to another client.")

        # Start threads for sending and receiving messages
        threading.Thread(target=receive_messages, args=(s, des_instance), daemon=True).start()
        send_messages(s, des_instance)  # Main thread handles sending

if __name__ == "__main__":
    main()
