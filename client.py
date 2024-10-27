import socket
from encryption import encrypt_string

def start_client(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    encrypted_message = encrypt_string(message)
    client_socket.send(encrypted_message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    message = "This is a test message longer than 8 characters"
    start_client(message)