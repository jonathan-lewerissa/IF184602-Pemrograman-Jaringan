import socket
import sys
import re
import select

server_address = ('localhost',5000)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket,]

try:
    while True:
        input_ready,output_ready,except_ready = select.select(input,[],[])

        for s in input_ready:
            if s == server_socket:
                client_socket, client_address = server_socket.accept()
                input.append(client_socket)
                print client_socket, client_address

            else:
                data = s.recv(1024)
        
                if data:
                    if re.match(r'^\d+[-+*/]\d+$',data):
                        res = eval(data)
                        print res
                        s.send(res)
                    else:
                        print 'invalid'
                else:
                    client_socket.close()

except (KeyboardInterrupt, SystemExit):
    print 'Exiting...'
    server_socket.close()
    sys.exit(0)