import socket

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        for i in range(5):
            message = "ping"
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received: {response}")

        input("Press Enter to send 5 more pings")

if __name__ == "__main__":
    host = "localhost"
    port = 8080

    start_client(host, port)
