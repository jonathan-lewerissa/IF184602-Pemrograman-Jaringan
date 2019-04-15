import socket

server_address = ('127.0.0.1',5000)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect(server_address)
print client_socket.getsockname()

send_address = ('127.0.0.1',5010)
send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
send_socket.connect(send_address)
send_info = send_socket.getsockname()

message = "DOWNLOAD ashiap.txt "+ str(send_info[0]) + " " + str(send_info[1])
client_socket.send(message)

recv_message = send_socket.recv(1024)
print 'message2'
f = open('asiap_client.txt','wb')
f.write(recv_message)
f.close()