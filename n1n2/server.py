import socket
import random
import json
from rsa import RSA

def Main():
    host = '127.0.0.1'
    port = 12345

    # Initialize server RSA
    server_rsa = RSA()

    # Create and bind the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server is listening...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from: {addr}")

        # Send public key to the client
        public_key = server_rsa.get_public_key()
        conn.send(json.dumps(public_key).encode())  # Send public key in JSON format

        # Receive client's public key
        client_public_key = json.loads(conn.recv(1024).decode())  # Use JSON to parse the public key
        print(f"Client's public key: {client_public_key}")

        # Receive n1 (client's nonce)
        n1 = int(conn.recv(1024).decode())
        print(f"Received n1 (client's nonce): {n1}")

        # Sign n1 with server's private key (correcting the signing process)
        signed_n1 = server_rsa.encrypt(str(n1), server_rsa.get_public_key())  # Use encrypt with the public key
        print(f"Signed n1: {signed_n1}")

        # Send signed n1 to the client
        conn.send(f"{signed_n1}".encode())

        # Generate and send n2 (server's nonce)
        n2 = random.randint(100000, 999999)
        print(f"Generated n2 (server's nonce): {n2}")
        conn.send(f"{n2}".encode())

        # Receive signed n2 from the client
        signed_n2 = conn.recv(1024).decode()

        if signed_n2:
            signed_n2 = int(signed_n2)
            print(f"Received signed n2: {signed_n2}")

            # Decrypt the signed n2 using the server's private key
            decrypted_n2 = server_rsa.decrypt(signed_n2)
            print(f"Decrypted n2: {decrypted_n2}")

            # Verify n2
            if decrypted_n2 == str(n2):
                print("Verification succeeded!")
            else:
                print("Verification failed!")

        else:
            print("No signed n2 received!")

        conn.close()

if __name__ == "__main__":
    Main()
