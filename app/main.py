import socket
import threading

def parse_request(data):
    lines = data.split('\r\n')
    start_line = lines[0]
    user_agent_line = lines[2]
    method, path, version = start_line.split(' ')
    return method, path, version, user_agent_line

def get_response(path, user_agent):
    if path.startswith('/echo'):
        path_message = path.split('/')[2]
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path_message)}\r\n\r\n{path_message}'
    elif path.startswith('/user-agent'):
        path_user_agent = user_agent.split(': ')[1]
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path_user_agent)}\r\n\r\n{path_user_agent}'
    elif path == '/':
        return 'HTTP/1.1 200 OK\r\n\r\n'
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\n'

def handle_request(client_socket):
    data = client_socket.recv(1024)
    print(data)
    method, path, version, user_agent = parse_request(data.decode())
    print(f'Method: {method}, path: {path}, version: {version}, user-agent: {user_agent}')
    response = get_response(path, user_agent)
    client_socket.sendall(response.encode())

def client_thread(client_socket, addr):
    print(f"Connection from {addr} has been established.")
    handle_request(client_socket)
    client_socket.close()
    print(f"Connection from {addr} has been closed.")

def main():
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket = socket.create_server(("localhost", 4221))
    print("Server is listening on port 4221...")
    try:
        while True:
            print("Waiting for a new connection...")
            client_socket, addr = server_socket.accept()
            threading.Thread(target=client_thread, args=(client_socket, addr)).start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    main()
