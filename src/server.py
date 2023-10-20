import signal
import socket
import sys
import threading

server_running = True


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    connected_clients = []

    while server_running:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            connected_clients.append(client_socket)

            client_thread = threading.Thread(target=handle_client, args=(
                client_socket, client_address, connected_clients))
            client_thread.start()
        except KeyboardInterrupt:
            break

    server_socket.close()
    for client_socket in connected_clients:
        client_socket.close()
    sys.exit()


def handle_client(client_socket, client_address, connected_clients):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from {client_address}: {data}")

            if data == "ping":
                response = "pong"
                client_socket.send(response.encode('utf-8'))
            elif data.startswith("data;"):
                response = data
                client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        connected_clients.remove(client_socket)
        client_socket.close()


def on_quit(sig, frame):
    global server_running
    print("Server is shutting down. Disconnecting all clients...")
    server_running = False


if __name__ == "__main__":
    host = "localhost"
    port = 8080
    signal.signal(signal.SIGINT, on_quit)

    start_server(host, port)
