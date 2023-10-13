import socket
import time

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = "ping"

        client_socket.send(message.encode('utf-8'))
        
        response = client_socket.recv(1024).decode('utf-8')
        if not response:
            break
        print(f"Received: {response}")

        time.sleep(2)

    client_socket.close()

if __name__ == "__main__":
    host = "localhost"
    port = 8080

    start_client(host, port)
