import socket

def handle_request(client_socket):
    client_socket.recv(1024)
    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.send(response.encode())

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")
    server_socket.accept()
    handle_request(server_socket)

if __name__ == "__main__":
    main()
