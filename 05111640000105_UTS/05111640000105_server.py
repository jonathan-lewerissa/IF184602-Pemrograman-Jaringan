import socket
import select
import sys
import os
from thread import *

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

ip_address = '127.0.0.1'

port = 8081

server.bind((ip_address,port))

server.listen(100)

base_folder = 'server'

list_of_clients = []

def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048)
            # print message
            if message:
                split_message = str(message).split()
                # print split_message

                # Digunakan untuk upload file ke server
                if split_message[0] == 'UPLOAD':
                    with open(os.path.join(base_folder,split_message[1]),'wb') as f:
                        l = conn.recv(2048)
                        while l:
                            f.write(l)
                            l = conn.recv(2048)
                            if str(l) == 'ENDSEND':
                                break
                
                # Digunakan untuk download file dari server
                elif split_message[0] == 'DOWNLOAD':
                    with open(os.path.join(base_folder,split_message[1]),'wb') as f:
                        l = conn.send(2048)
                        while l:
                            f.write(l)
                            l = conn.send(2048)
                            if str(l) == 'ENDSEND':
                                break

                # Digunakan untuk melihat list folder
                elif split_message[0] == 'LIST':
                    file_list = [f for f in os.listdir(base_folder) if os.path.isfile(os.path.join(base_folder,f))]
                    print str(file_list)
                    conn.send(str(file_list))

                # Digunakan untuk menghapus file
                elif split_message[0] == 'REMOVE':
                    file_list = [f for f in os.listdir(base_folder) if os.path.isfile(os.path.join(base_folder,f))]
                    os.remove(os.path.join(base_folder,split_message[1]))
                    conn.send(str(split_message[1]) + ' removed')
                
                # Digunakan untuk mengirim chat
                else: 
                    message_to_send = "<" + str(addr) + "> " + message
                    # print message_to_send
                    broadcast(message_to_send,conn)
            else:
                removeConnection(conn) 
        except:
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                removeConnection(client)

def removeConnection(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

os.system('clear')

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print addr[0] + " connected"
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()