import socket
import sys
import threading
import time

exit_signal = threading.Event()


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    connected_clients = []
    try:
        while not exit_signal.is_set():

            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            connected_clients.append(client_socket)

            client_thread = threading.Thread(target=handle_client, args=(
                client_socket, client_address, connected_clients))
            client_thread.start()

            # This allows the child threads to exit the main thread and to register the keyboard interrupt
            try:
                while not exit_signal.is_set():
                    time.sleep(0.1)
                    client_thread.join()
            except KeyboardInterrupt:
                exit_signal.set()
                print("Server shutting down.")
                server_socket.close()
                break
    except Exception as e:
        print(e)
    finally:
        server_socket.close()
        sys.exit()


def handle_client(client_socket, client_address, connected_clients):
    try:
        while not exit_signal.is_set():
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from {client_address}: {data}")
            if not exit_signal.is_set():
                if data == "ping":
                    response = "pong"
                    client_socket.send(response.encode('utf-8'))
                elif data.startswith("Data for"):
                    response = data
                    client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        connected_clients.remove(client_socket)
        client_socket.close()


if __name__ == "__main__":
    host = "localhost"
    port = 8080

    try:
        start_server(host, port)
    except KeyboardInterrupt:
        print("Server start interrupted by user.")
    except Exception as e:
        print(e)
