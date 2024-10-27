import socket
from encryption import decrypt_string

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    print("Server listening on port 12345")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    encrypted_message = conn.recv(1024).decode('utf-8')
    decrypted_message = decrypt_string(encrypted_message)
    print(f"Decrypted message: {decrypted_message}")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()