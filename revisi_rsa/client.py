import asyncio
import logging
from .cryptolib import RSA, PKA, DES  # Updated import statement
# import utils


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


async def communicate_with_server():
    reader, writer = await asyncio.open_connection('127.0.0.1', 5002)
    rsa = RSA()
    pka = PKA()

    # Receive server's public key
    server_public_key = await reader.read(1024)
    logging.info(f"Received server public key: {server_public_key.decode()}")

    # Encrypt DES key and send it to the server
    des_key = "1001100111"
    print("des key: ", des_key)
    encrypted_des_key = rsa.encrypt(des_key, eval(server_public_key.decode()))
    writer.write(str(encrypted_des_key).encode())
    await writer.drain()

    # DES encryption object
    des = DES(des_key)

    while True:
        message = input("Enter your message: ")
        encrypted_message = des.encrypt(message)
        writer.write(encrypted_message.encode())
        await writer.drain()

        logging.info(f"Sent encrypted message: {encrypted_message}")

        # Receive and decrypt server response
        encrypted_response = await reader.read(1024)
        decrypted_response = des.decrypt(encrypted_response.decode())
        logging.info(f"Received decrypted message: {decrypted_response}")


if __name__ == '__main__':
    asyncio.run(communicate_with_server())
