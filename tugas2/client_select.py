import socket
import sys

server_address = ('localhost',5000)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('Enter the file name: ')
file_name = sys.stdin.readline()
file_name = file_name.rstrip()
sys.stdout.write('Trying to send...\n')

with open(file_name,'r') as file_input:
    client_socket.send('F_START_'+file_name)
    client_socket.send(str(file_input.read()))
    client_socket.send('F_EOF')
print 'Exiting...'
client_socket.close()
sys.exit(0)