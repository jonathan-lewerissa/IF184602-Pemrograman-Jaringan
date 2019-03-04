import socket
import select
import sys

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address,port))

while True:
    socket_list = [sys.stdin, server]

    read_socket, write_socket, error_socket = select.select(socket_list,[],[])

    for socks in read_socket:
        if socks == server:
            message = socks.recv(2048)
            print message
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()