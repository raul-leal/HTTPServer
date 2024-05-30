import socket
import threading
import os
import argparse

def get_directory():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='files', help='Directory to serve files from')
    args = parser.parse_args()
    return args

def parse_request(data):
    lines = data.split('\r\n')
    start_line = lines[0]
    method, path, version = start_line.split(' ')
    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        header, value = line.split(': ', 1)
        headers[header] = value
    return method, path, version, headers

def generate_response(status, content_type, body, encoding=None):
    if isinstance(body, bytes):
        body = body.decode()
    body_length = len(body)

    if encoding != None and 'gzip' in encoding:
        headers = [
            f'HTTP/1.1 {status}',
            f'Content-Encoding: gzip',
            f'Content-Type: {content_type}',
            f'Content-Length: {body_length}',
            '',
            body
        ]
    else:
        headers = [
            f'HTTP/1.1 {status}',
            f'Content-Type: {content_type}',
            f'Content-Length: {body_length}',
            '',
            body
    ]
    return '\r\n'.join(headers)

def files_get(path):
    args = get_directory()
    file_path = path.split("/files/")[1]
    full_file_path = os.path.join(args.directory, file_path)
    if os.path.isfile(full_file_path):
        try:
            with open(full_file_path, 'rb') as file:
                file_contents = file.read()
            response = generate_response('200 OK', 'application/octet-stream', file_contents)
        except PermissionError:
            print(f'Permission denied while reading {full_file_path}')
            response = generate_response('403 Forbidden', 'text/plain', 'Access Denied')
    else:
        print(f'File {full_file_path} not found')
        response = generate_response('404 Not Found', 'text/plain', 'File Not Found')
    return response

def files_post(path, data):
    args = get_directory()
    file_path = path.split("/files/")[1]
    full_file_path = os.path.join(args.directory, file_path)
    if os.path.isfile(full_file_path):
        print(f'File {full_file_path} already exists')
        response = generate_response('409 Conflict', 'text/plain', 'File Already Exists')
    else:
        try:
            with open(full_file_path, 'wb') as file:
                file.write(data.split('\r\n\r\n')[1].encode())
            response = generate_response('201 Created', 'text/plain', 'File Created')
        except PermissionError:
            print(f'Permission denied while writing {full_file_path}')
            response = generate_response('403 Forbidden', 'text/plain', 'Access Denied')
    return response

def handle_request(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return
        
        method, path, version, headers = parse_request(data)

        if path == '/':
            response = generate_response('200 OK', 'text/plain', '')
        elif path.startswith('/echo'):
            echo_str = path.split("/echo/")[1]
            if 'Accept-Encoding' in data:
                encoding = data.split('Accept-Encoding: ')[1].split('\r\n')[0]
            else:
                encoding = None
            response = generate_response('200 OK', 'text/plain', echo_str, encoding)
        elif path == '/user-agent':
            user_agent = headers.get('User-Agent', 'Unknown')
            response = generate_response('200 OK', 'text/plain', user_agent)
        elif path.startswith('/files/'):
            if method == 'GET':
                response = files_get(path)
            elif method == 'POST':
                response = files_post(path, data)
        else:
            response = generate_response('404 Not Found', 'text/plain', 'Not Found')
        client_socket.send(response.encode())
    finally:
        client_socket.close()

def client_thread(client_socket, addr):
    print(f"Connection from {addr} has been established.")
    handle_request(client_socket)
    print(f"Connection from {addr} has been closed.")

def main():
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()
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
