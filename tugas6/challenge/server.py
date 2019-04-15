import socket
import sys

command_address = ('127.0.0.1',5000)
command_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
command_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
command_socket.bind(command_address)
print command_socket.getsockname()

send_address = ('127.0.0.1',5010)
send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
send_socket.bind(send_address)

while True:
    data, client_address = command_socket.recvfrom(1024)
    data = data.split()
    print data
    if data[0] == 'DOWNLOAD':
        with open(data[1],'rb') as f:
            send_data = f.read()
            f.close()
        send_socket.sendto(send_data, (data[2],int(data[3])))
        print send_data
        print client_address