import socket
import random

server_address = ('127.0.0.1',5001)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(server_address)

while True:
    data, client_addresss = server_socket.recvfrom(1024)

    if random.randint(0,1):
        server_socket.sendto(data, client_addresss)
        print 'data: ',data, 'client address:', client_addresss
        print 'sock_name', server_socket.getsockname() 
    
    else:
        print 'server is down'