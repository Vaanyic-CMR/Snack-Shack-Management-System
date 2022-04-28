import socket
import pickle

HEADER = 64

PORT = 9000
SERVER = socket.gethostbyname("Caleb-Gaming-Desktop")
ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"
DISCONNECT_CMD = "!DISCONNECT"
SUCCESS_MSG = "!SUCCESS!"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# Command Format
# ("route1/route2/...", object1, object2, ...)

def send( cmd ):
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