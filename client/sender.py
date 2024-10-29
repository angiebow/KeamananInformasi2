import socket
from des.DES import DES  
from des.utils import pad_string 

IP = "127.0.0.1"
PORT = 65432
DES_KEY = 12345678 

def main():
    des_instance = DES(DES_KEY) 
    message = "This is a longer message that needs to be encrypted."

    padded_message = pad_string(message)
    encrypted_message = des_instance.encrypt(padded_message)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        s.sendall(encrypted_message.encode())
        print("Encrypted message sent:", encrypted_message)

if __name__ == "__main__":
    main()