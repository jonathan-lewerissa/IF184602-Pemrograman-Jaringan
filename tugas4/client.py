import socket
import select
import sys

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
            message = message.split(":")
            name = str(message[1]).strip()

            with open(base_folder+'/'+name,'wb') as f:
                message = socks.recv(2048)
                print message
                f.write(message)
                # if str(message) != 'ENDSEND':
                    # f.write(message)
        else:
            message = raw_input()
            message = message.split()

            server.send(str('SEND:'+message[1]+'\n'))

            with open(message[1],'rb') as f:
                for line in f:
                    server.send(str(line))
            server.send(str('\n'))

            sys.stdout.write("<You>")
            sys.stdout.write(str(message))
            sys.stdout.flush()

server.close()