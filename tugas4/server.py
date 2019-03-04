import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

ip_address = '127.0.0.1'

port = 8081

server.bind((ip_address,port))

server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print "<" + addr[0] + "> " + message

                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message,conn)
            else:
                remove(conn) 
        except:
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print addr[0] + " connected"
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()