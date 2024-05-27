import socket

def parse_request(data):
    lines = data.split('\r\n')
    start_line = lines[0]
    method, path, version = start_line.split(' ')
    return method, path, version

def get_response(path):
    if path == '/':
        return 'HTTP/1.1 200 OK\r\n\r\n'
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\n'

def handle_request(client_socket):
    data = client_socket.recv(1024)
    print(data)
    method, path, version = parse_request(data.decode())
    response = get_response(path)
    client_socket.sendall(response.encode())

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
