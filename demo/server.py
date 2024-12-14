#server.py
import random
from rsa import RSA
import socket

def Main():
    host = "127.0.0.1"
    port = 5002

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Waiting for connection...")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    rsa = RSA()

    n1 = int(conn.recv(1024).decode()) 
    print(f"Received n1: {n1}")

    n2 = random.randint(10000, 99999)  
    print(f"Generated n2: {n2}")
    encrypted_n1 = pow(n1, public_key[0], public_key[1])  

    response = (encrypted_n1, rsa.get_public_key(), n2)
    conn.send(str(response).encode())

    encrypted_n2 = int(conn.recv(2048).decode())  
    decrypted_n2 = rsa.decrypt(encrypted_n2)  
    if int(decrypted_n2) != n2:
        print("Error: n2 verification failed!")
        return
    print("n2 verified successfully!")

    encrypted_des_key = int(conn.recv(2048).decode())  
    des_key = rsa.decrypt(encrypted_des_key)  
    print(f"DES key securely received: {des_key}")

if __name__ == "__main__":
    Main()