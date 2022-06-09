import socket
import threading
import pickle

import resources as r
from .controllers import (
    camper_controller,
    staff_controller,
    inventory_controller,
    history_controller,
    bank_controller
)

HEADER = 64

PORT = r.settings.port
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
RUNNING = True

FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
SUCCESS_MSG = "!SUCCESS!"
FAIL_MSG = "!FAILED!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

# Command Format
# ("route1/route2/...", object1, object2, ...)

# ----------| Send and Receive data to threaded clients | ----------
def handle_client(conn, address ):
    print(f"[NEW CONNECTION] {address} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            cmd = conn.recv(msg_length)
            cmd = pickle.loads( cmd )
            
            if cmd == DISCONNECT_MSG:
                print(f"[{address}] | {cmd}")
                connected = False
            else:
                handle_command( conn, cmd )

def send_to_client( conn, res ):
    # Pickling the command object being sent
    response = pickle.dumps(res)
    # Calculating length of byte response to include in header
    msg_length = len(response)
    
    # Building the header and encoding to send to server.
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    # Sending header
    conn.send(send_length)
    # Sending response
    conn.send(response)

def handle_command( conn, data ):
    command = data[0].split('/')
    res = None
    
    if command[1] == "campers":
        res = camper_controller.handle_campers_command( data )
    if command[1] == "staff":
        res = staff_controller.handle_staff_command( data )
    if command[1] == "inventory":
        res = inventory_controller.handle_inventory_command( data )
    if command[1] == "history":
        res = history_controller.handle_history_command( data )
    if command[1] == "bank":
        res = bank_controller.handle_bank_command( data )
    
    if res is not None:
        send_to_client( conn, res )

# ----------| Starts running the server | ----------
def start():
    global RUNNING
    print("[STARTING] | Server is starting...")
    server.listen()
    print(f"[LISTENING] | Server is listening on IP: {SERVER}, PORT: {PORT}")
    while RUNNING:
        conn, address = server.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.daemon = True
        thread.start()
        
        print(f"[ACTIVE CONNECTIONS] | {threading.active_count() - 2}")
    close()
    server.close()

# ----------| Closes the server | ----------
def close():
    global RUNNING
    RUNNING = False
    
    print(f"[DEACTIVATING] | Server is closing...")

if __name__ == '__main__':
    start()