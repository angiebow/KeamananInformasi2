import socket
from des.DES import DES

IP = "127.0.0.1"
PORT = 65432
DES_KEY = 12345678  

def main():
    des_instance = DES(DES_KEY)  

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print("Waiting for connection...")

        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            encrypted_message = conn.recv(1024).decode()
            print("Received encrypted message:", encrypted_message)

            decrypted_message = des_instance.decrypt(encrypted_message)
            print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()