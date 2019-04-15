import socket
import select
import sys
import os
from functools import partial
from time import sleep

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address,port))

base_folder = 'base'

if sys.argv:
    base_folder = sys.argv[1]

os.system('clear')

while True:
    socket_list = [sys.stdin, server]

    read_socket, write_socket, error_socket = select.select(socket_list,[],[])

    for socks in read_socket:
        if socks == server:
            message = socks.recv(2048)
            print str(message)

        else:
            message = raw_input()
            message_parse = message.split()

            # Digunakan untuk upload file ke server dan/atau semua client
            if message_parse[0] == 'UPLOAD' or  message_parse[0] == 'SENDALL':
                server.send(message)
                sleep(0.5)
                with open(message_parse[1],'rb') as f:
                    for chunk in iter(partial(f.read,2048),b''):
                        server.send(chunk)
                sleep(0.5)
                server.send('ENDSEND')

            # Digunakan untuk download file dari server
            elif message_parse[0] == 'DOWNLOAD':
                server.send(message)

                with open(os.path.join(base_folder,message_parse[1]),'wb') as f:
                        l = server.recv(2048)
                        while l:
                            f.write(l)
                            l = server.recv(2048)
                            if str(l) == 'ENDSEND':
                                break
            
            # Digunakan untuk message lain seperti LIST, REMOVE, atau menerima pesan
            else:
                server.send(message)

server.close()