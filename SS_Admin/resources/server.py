import socket
import threading
import pickle

import resources as r
from .controllers import (
    camper_controller,
    staff_controller,
    inventory_controller
)

HEADER = 64

PORT = r.settings.port
SERVER = socket.gethostbyname(r.settings.host_name)
ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

# Command Format
# ("route1/route2/...", object1, object2, ...)

# ----------| Send and Receive data to threaded clients | ----------
def handle_client(conn, address):
    print(f"[NEW CONNECTION] {address} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            cmd = conn.recv(msg_length)
            cmd = pickle.loads( cmd )
            
            if cmd == DISCONNECT_MSG:
                connected = False
            else:
                handle_command( cmd )
            
            print(f"[{address}] | {cmd}")

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

def handle_command( data ):
    command = data[0].split('/')
    res = None
    
    if command[1] == "campers":
        res = camper_controller.handle_campers_command( data )
    if command[1] == "staff":
        res = staff_controller.handle_staff_command( data )
    if command[1] == "inventory":
        res = inventory_controller.handle_inventory_command( data )
    
    if res is not None:
        send_to_client( res )

# ----------| Starts running the server | ----------
def start():
    print("[STARTING] | Server is starting...")
    server.listen()
    print(f"[LISTENING] | Server is listening on IP: {SERVER}, PORT: {PORT}")
    while r.running:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] | {threading.active_count() - 2}")
    print(f"[DEACTIVATING] | Server is closing...")
    server.close()

if __name__ == '__main__':
    start()