import socket

server_address = ('localhost',5001)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(server_address)

while True:
    ops = raw_input()
    client_socket.send(ops)

client_socket.close()
