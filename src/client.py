import socket
import sys
import time
import keyboard
import os
import pandas as pd
from datetime import datetime

# Sorry I know this is ugly but I swear I couldn't find any other way to access the file :///
script_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(os.path.dirname(
    script_dir), 'data', 'wr_sensor_data.csv')

timeout = 5


def read_data_for_day(csv_file, target_date):
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    filtered_data = df[df['Timestamp'].dt.date ==
                       target_date].to_string(index=False)

    return filtered_data


def send_ping(client_socket):
    message = "ping"

    for i in range(5):
        try:
            start_time = time.time()
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            end_time = time.time()
            round_trip_time = (end_time - start_time) * 1000
            print(f"Received: {response} (RTT: {round_trip_time:.6f}ms)")
        except socket.timeout:
            print(f"Timeout: No response from server after {timeout}s")


def start_client(host, port, target_date):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.settimeout(timeout)

    is_quit = False

    def on_esc_event(e):
        nonlocal is_quit
        if e.event_type == keyboard.KEY_DOWN:
            is_quit = True

    keyboard.on_press_key("esc", on_esc_event)

    while not is_quit:
        choice = input(
            "Enter 'Data' for data, 'Ping' for ping, or ESC to quit: ").lower()

        if choice == 'data' or choice == 'd':
            data = read_data_for_day(csv_file_path, target_date)
            message = f"data;{target_date};{data}"
            try:
                start_time = time.time()
                client_socket.send(message.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                end_time = time.time()
                round_trip_time = (end_time - start_time) * 1000
                print(f"Received: {response} (RTT: {round_trip_time:.6f}ms)")
            except socket.timeout:
                print(f"Timeout: No response from server after {timeout}s")
        elif choice == 'ping' or 'p':
            send_ping(client_socket)
        else:
            print(
                "Invalid choice. Please enter 'Data', 'D', 'Ping', 'P', or ESC to quit the client.")

    keyboard.unhook_all()
    client_socket.close()
    sys.exit()


if __name__ == "__main__":
    host = "localhost"
    port = 8080
    target_date = datetime(2023, 10, 13).date()

    start_client(host, port, target_date)
