import socket

def handle_request(client_socket):
    data = client_socket.recv(1024)
    print(data)
    client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")
    try:
        while True:
            print("Waiting for a new connection...")
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr} has been established.")
            handle_request(client_socket)
            client_socket.close()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    main()
