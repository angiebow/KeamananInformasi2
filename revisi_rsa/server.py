import asyncio
import logging
from .cryptolib import RSA, PKA, DES  # Updated import statement
# import utils


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


async def handle_client(reader, writer):
    rsa = RSA()
    pka = PKA()
    pka.register("server", rsa.get_public_key())

    logging.info("Waiting for client message...")

    # Send RSA public key to client
    public_key = rsa.get_public_key()
    writer.write(str(public_key).encode())
    await writer.drain()

    # Receive encrypted DES key
    encrypted_des_key = await reader.read(1024)
    print("encrypted des: ", encrypted_des_key)
    des_key = rsa.decrypt(int(encrypted_des_key.decode()))
    logging.info(f"Received DES key: {des_key}")

    # DES encryption object
    des = DES(des_key)

    while True:
        encrypted_message = await reader.read(1024)
        if not encrypted_message:
            logging.info("No more data from client.")
            break

        decrypted_message = des.decrypt(encrypted_message.decode())
        logging.info(f"Received message: {decrypted_message}")

        response = input("Enter your response: ")
        encrypted_response = des.encrypt(response)
        writer.write(encrypted_response.encode())
        await writer.drain()

    logging.info("Closing connection.")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 5002)
    logging.info("Server started on 127.0.0.1:5002")
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
