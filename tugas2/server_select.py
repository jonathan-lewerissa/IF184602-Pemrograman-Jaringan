import socket
import sys
import re
import select
import time

server_address = ('localhost',5000)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(server_address)
server_socket.listen(5)

file_name = 'select_input.log'

input_socket = [server_socket]

file_cache = {}
file_name_cache = {}

try:
    while True:
        read_ready,write_ready,exception = select.select(input_socket,[],[])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                print client_socket, client_address
            
            else:
                data = sock.recv(1024)

                flag_start = re.match('(^F_START_)(.*)',str(data))
                flag_end = re.match('^F_EOF$',str(data))

                if flag_start:
                    print flag_start.groups()
                    file_name_cache[sock.getpeername()] = flag_start.group(0)
                    file_cache[sock.getpeername()] = ''
                elif flag_end:
                    print flag_end.groups()
                    print file_cache[sock.getpeername()]
                    # with open("server_"+str(file_name_cache[sock.getpeername()]),'w') as f:
                    #     f.write(file_cache[sock.getpeername()])
                    sock.close()
                    input_socket.remove(sock)
                else:
                    file_cache[sock.getpeername()] += str(data)

except (KeyboardInterrupt, SystemExit):
    print 'Exiting...'
    server_socket.close()
    sys.exit(0)