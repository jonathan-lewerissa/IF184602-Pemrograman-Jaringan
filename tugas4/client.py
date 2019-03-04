import socket
import select
import sys
from functools import partial
from time import sleep

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address,port))

base_folder = 'base'

if sys.argv:
    base_folder = sys.argv[1]

while True:
    socket_list = [sys.stdin, server]

    read_socket, write_socket, error_socket = select.select(socket_list,[],[])

    for socks in read_socket:
        if socks == server:
            message = socks.recv(2048)
            print 'Header: ' + str(message)
            name = str(message)

            with open(base_folder+'/'+name,'wb') as f:
                l = socks.recv(2048)
                while l:
                    f.write(l)
                    l = socks.recv(2048)
                    if str(l) == 'ENDSEND':
                        break
        else:
            message = raw_input()

            server.send(str(message))
            sleep(0.5)

            with open(message,'rb') as f:
                for chunk in iter(partial(f.read,2048),b''):
                    server.send(chunk)
            server.send('ENDSEND')
            sleep(0.5)

            sys.stdout.write("<You>")
            sys.stdout.write(str(message))
            sys.stdout.flush()

server.close()