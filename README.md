# TCP-Based Ping and Pong Implementation with CVS Sensor Data
## Table of Contents

1. [How to Install and Run](#installation)
    1. [Pre-requisites](#prerequisites)
    3. [How to run](#how-to-run)
    4. [Configuration](#configuration)
    5. [Usage](#usage)
2. [Implementation Details](#implementation-details)
    1. [Server](#server)
    2. [Client](#client)

&nbsp;
## How to Install and Run <a name="installation"></a>
### Pre-requisites <a name="prerequisites"></a>
Make sure Python and pip are properly set up on the system. **Python 3.x** and **pip3** are required for this project. This can be checked by running `pip –-version` and `python --version` in the Command Prompt. 

Python can be downloaded from the [official Python website](https://www.python.org/downloads/). Make sure to check the box that says "Add Python X.X to PATH" during installation. pip3 is automatically installed with Python 3.4+.

A virtual environment keeps Python packages in a virtual environment localized to the project, instead of installing the packages system-wide. Familiarize yourself and use this option if neccessary.

### Steps to run the TCP Ping Pong Client <a name="how-to-run"></a>

**1. Clone the repository:**

   ```powershell
   git clone https://github.com/Anni-065/tcp-pingpong.git
   ```

**2. Navigate to the project directory:**

   ```powershell
   cd tcp-pingpong
   ```

**3. Create and activate a virtual environment if needed, and install the required Python packages:**
   
   ```powershell
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

   Then, install the required packages:
   
   ```powershell
   pip install -r requirements.txt
   ```

   Following external Python packages are required, and are part of the `requirements.txt` file:

   - [pandas](https://pandas.pydata.org/)
   - [keyboard](https://github.com/boppreh/keyboard)

**5. Naviagte to the `src` folder and run the server:**

   ```powershell
   python server.py
   ```
   
**6. In a different terminal window, navigate to the `src` folder and run the client:**

   ```powershell
   python client.py
   ```
   You can open more terminals and run more seperate clients in each one.

   The clients will start and connect to the server, and you can interact with them using the options provided.

## Configuration <a name="configuration"></a>

You can configure the server address and port by modifying the `host` and `port` variables in the `client.py` file.

```python
host = "localhost"
port = 8080
```

## Usage <a name="usage"></a>

- Enter *'Data'* or *'D'* into the client terminal(s) to send data from the CSV file.
- Enter *'Ping'* or *'P'* into the client terminal(s) to send 5 consecutive ping messages to the server, and receive a pong response including the Round-trip time (RTT) it took to send and receive the messages.
- Press the ESC key in the client terminal to quit the corresponding client.
- Press CTRL+C in the server terminal to quit the server, and disconnect all clients.

Follow the on-screen prompts and instructions. The input commands are <ins>**not** case-sensitive</ins>.

&nbsp;

## Implementation Details <a name="implementation-details"></a>

The TCP Client and Server were implemented using Python. Here's an overview of how their functionalities were implemented: 

### Server Implementation <a name="server"></a>

- The server uses standard Python socket programming to manage connections and data transmission, and continuously listens on a specified `host` and `port` to accept incoming connections from clients.

- When a client tries to connect, a new socket for the specific client and the client's address is created. For each client connection, a new thread is also created to handle communication with that client. The server is implemented using a multi-threaded approach to handle several client connections concurrently. Multiple clients can communicate with the server at the same time without blocking each other.

- Connected clients are stored in a list, and removed in case of an error or when the client disconnects.

- The server responds to client requests in the following ways:
  - If the client sends *'ping'*, the server responds with *'pong'*.
  - If the client sends a message starting with *'data;'*, the server echoes the received data back to the client.

- The global variable `server_running` is used to control whether the server should continue running. The user can stop the server by pressing Ctrl+C in the terminal. This functionality was implemented using the [`signal` module](https://docs.python.org/3/library/signal.html#signal.SIGINT), which registers the Ctr+C event, and sets `server_running` to False. As a result the server and client sockets are closed, and the process is terminated.

### Client Implementation <a name="client"></a>

- The client is designed to automatically conntect to the server. It can send data from a CSV file or five consecutive ping messages to measure the round-trip time (RTT) to the server, depending on the user input from the terminal.

- The [`pandas` module](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv) is used to read and process data from a CSV file. The function `def read_data_for_day(csv_file, target_date)` filters the data based on a date provided in the code and returns it as a string, excluding the index column. The main client function then receives the string and sends the result to the server.

- To measure the RTT of the ping-pong messages, the client records the time when a *'ping'* message is sent, and again when the respective *'pong'* response is received from the server. Based on these numbers the RRT is calculated.

- The input options for the user include sending pings, sending data, or quitting a client process by pressing ESC. The latter option is implemented using the [`keyboard` module](https://github.com/boppreh/keyboard#keyboardon_press_keykey-callback-suppressfalse) to detect the respective key event. When the user sends an exit signal to the client, the flag `is_quit` is set to True, which interupts the loop that keeps the client running. The client socket is then closed and the keyboard listener removed, before the system exit function is called to terminate the process.

- If no response is received within a specified timeframe (the default timeout value is 5 seconds), the client prints a message notifying the user that no response was received from the server, assuming that an error occured during the transmission of the data.
