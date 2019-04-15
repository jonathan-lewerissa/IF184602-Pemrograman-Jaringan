import socket
import select
import sys
import os

base_folder = 'base'

def navigate(path):
    entries = os.listdir(base_folder + path)
    response = '<ul>'
    for files in entries:
        print files
        response += '<li><a href=/'+path+'/'+files+'></li>'
    response += '</ul>'

    print response

    return response

server_address = ('127.0.0.1',80)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket,[],[])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                print 'check'

            else:
                # receive data from client, break when null received
                data = sock.recv(4096)
                print data

                request_header = data.split('\r\n')
                print request_header
                request_file = request_header[0].split()[1]
                print request_file

                if request_file == 'index.html' or request_file == '/':
                    response_data = navigate('/')
                    print response_data

                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(content_length) + '\r\n'
                    print response_header

                print 'before'
                sock.sendall(response_header + '\r\n' +response_data)
                print 'after'
                
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)

