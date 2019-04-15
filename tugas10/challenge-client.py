import socket
import sys
import select
import pickle

server_address = ('localhost',8080)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(server_address)

input_socket = [client_socket,sys.stdin]
state = {}

def pickling(data):
    return pickle.dumps(data)

def unpickling(data):
    return pickle.loads(data)

try:
    while True:
        read_ready,write_ready,exception = select.select(input_socket,[],[])

        for sock in read_ready:
            if sock == client_socket:
                data = unpickling(sock.recv(2014))
                print data
                print type(data)

                if type(data) is str:
                    print data
                elif type(data) is dict:
                    state = data
                
                    print state[1] + "|" + state[2] + "|" + state[3]
                    print state[4] + "|" + state[5] + "|" + state[6]
                    print state[7] + "|" + state[8] + "|" + state[9]
            else:
                message = sys.stdin.readline()
                message = message.strip()
                message = int(message)
                state[message] = message
                client_socket.send(pickling(state))

except (KeyboardInterrupt, SystemExit):
    print 'Exiting...'
    client_socket.close()
    sys.exit(0)