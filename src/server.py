import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received: {data}")
        
        if data == "ping":
            response = "pong"
            client_socket.send(response.encode('utf-8'))

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    host = "localhost"
    port = 8080

    start_server(host, port)
