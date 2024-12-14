#client.py
import socket
import random
from rsa import RSA

def Main():
    host = "127.0.0.1"
    port = 5002

    client_socket = socket.socket()
    client_socket.connect((host, port))

    rsa = RSA()

    n1 = random.randint(10000, 99999)  
    print(f"Generated n1: {n1}")
    client_socket.send(str(n1).encode())

    response = eval(client_socket.recv(2048).decode())
    encrypted_n1, server_public_key, n2 = response
    print(f"Received encrypted n1: {encrypted_n1}")
    print(f"Received server's public key: {server_public_key}")
    print(f"Received n2: {n2}")

    decrypted_n1 = pow(encrypted_n1, private_key[0], private_key[1]) 
    assert decrypted_n1 == n1, "Decrypted n1 does not match original!"
    if decrypted_n1 != n1: 
        print("Error: n1 verification failed!")
        return
    print("n1 verified successfully!")

    encrypted_n2 = rsa.encrypt(str(n2), server_public_key) 
    client_socket.send(str(encrypted_n2).encode())
    print("n2 sent successfully!")

    des_key = "1001100111" 
    encrypted_des_key = rsa.encrypt(des_key, server_public_key)
    client_socket.send(str(encrypted_des_key).encode())
    print("DES key securely sent!")

if __name__ == "__main__":
    Main()