import socket
import random
import json
from rsa import RSA

def Main():
    host = '127.0.0.1'
    port = 12345

    # Initialize client RSA
    client_rsa = RSA()

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive server's public key
    server_public_key = json.loads(client_socket.recv(1024).decode())  # Use JSON to parse the public key
    print(f"Server's public key: {server_public_key}")

    # Send client's public key
    client_socket.send(json.dumps(client_rsa.get_public_key()).encode())  # Send public key in JSON format

    # Generate and send n1 (client's nonce)
    n1 = random.randint(100000, 999999)
    print(f"Generated n1 (client's nonce): {n1}")
    client_socket.send(f"{n1}".encode())

    # Receive signed n1 from the server
    signed_n1 = client_socket.recv(1024).decode()
    print(f"Received signed n1: {signed_n1}")

    if signed_n1:  # Ensure the signed_n1 is not empty
        signed_n1 = int(signed_n1)
        # Decrypt signed n1 using client's private key
        decrypted_n1 = client_rsa.decrypt(signed_n1)
        print(f"Decrypted n1: {decrypted_n1}")

        # Verify n1
        if decrypted_n1 != str(n1):
            print("Server verification failed!")
            client_socket.close()
            return

        # Receive n2 from the server
        n2 = int(client_socket.recv(1024).decode())
        print(f"Received n2 (server's nonce): {n2}")

        # Sign n2 and send it back to the server
        signed_n2 = client_rsa.encrypt(str(n2), client_rsa.get_public_key())
        print(f"Sending signed n2: {signed_n2}")
        client_socket.send(f"{signed_n2}".encode())

    else:
        print("Received empty signed_n1 from server!")

    client_socket.close()

if __name__ == "__main__":
    Main()
