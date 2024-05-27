import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")
    client_socket.sendall(b"HTTP/1.1 200 OK \r\n\r\n")
    client_socket.close()


if __name__ == "__main__":
    main()
