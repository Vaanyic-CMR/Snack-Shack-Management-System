from http import client
import socket
import pickle

from . import var_const as vc

HEADER = 64

PORT = vc.settings.port
SERVER = socket.gethostbyname(vc.settings.host_name)
ADDRESS = (SERVER, PORT)

def reload_address():
    global SERVER, PORT, ADDRESS
    PORT = vc.settings.port
    SERVER = socket.gethostbyname(vc.settings.host_name)
    ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"
DISCONNECT_CMD = "!DISCONNECT"
SUCCESS_MSG = "!SUCCESS!"

client = None

# Command Format
# ("route1/route2/...", object1, object2, ...)

def connect_to_host():
    global client, ADDRESS
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDRESS)
    except Exception as e:
        client = None
        raise e

def send( cmd ):
    global client
    
    # Pickling the command object being sent
    command = pickle.dumps(cmd)
    # Calculating length of byte command to include in header
    msg_length = len(command)
    
    # Building the header and encoding to send to server.
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    # Sending header
    client.send(send_length)
    # Sending command
    client.send(command)

def response_from_server():
    global client
    
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        res = client.recv(msg_length)
        res = pickle.loads( res )
        return res

if __name__ == '__main__':
    # send( "Hello World" )
    # cmd = ("api/campers/create", "Hello World")
    # send( cmd )
    # send( DISCONNECT_CMD )
    pass