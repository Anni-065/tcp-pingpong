import socket
import time
import keyboard
import os

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    is_quit = False

    def on_esc_event(e):
        nonlocal is_quit
        if e.event_type == keyboard.KEY_DOWN:
            is_quit = True

    keyboard.on_press_key("esc", on_esc_event)

    while not is_quit:
        for i in range(5):
            message = "ping"
            start_time = time.time()
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            end_time = time.time()
            round_trip_time = (end_time - start_time) * 1000
            print(f"Received: {response} (RRT: {round_trip_time:.3f}ms)")

        input("Press Enter to send 5 more pings or ESC to quit the client")

    keyboard.unhook_all()
    client_socket.close()
    os._exit(0)

if __name__ == "__main__":
    host = "localhost"
    port = 8080

    start_client(host, port)
