import socket
import sys
import re
import select
import time
import pickle

server_address = ('localhost',8080)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
player_id = {}
player_address = {}
state = {}
turn = 'L'
started = False

def pickling(data):
    return pickle.dumps(data)

def unpickling(data):
    return pickle.loads(data)

def check_win(data):
    if data[1] == data[2] and data[2] == data[3] and data[3] != ' ': return data[1]
    elif data[4] == data[5] and data[5] == data[6] and data[6] != ' ': return data[4]
    elif data[7] == data[8] and data[8] == data[9] and data[9] != ' ': return data[7]
    elif data[1] == data[4] and data[4] == data[7] and data[7] != ' ': return data[1]
    elif data[2] == data[5] and data[5] == data[8] and data[8] != ' ': return data[2]
    elif data[3] == data[6] and data[6] == data[9] and data[9] != ' ': return data[3]
    elif data[1] == data[5] and data[5] == data[9] and data[9] != ' ': return data[1]
    elif data[3] == data[5] and data[5] == data[7] and data[7] != ' ': return data[3]
    else: return False


try:
    while True:
        read_ready,write_ready,exception = select.select(input_socket,[],[])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                if len(input_socket) == 1:
                    player_id[client_socket] = 'L'
                    player_address['L'] = client_socket
                    input_socket.append(client_socket)
                elif len(input_socket) == 2:
                    player_id[client_socket] = 'S'
                    player_address['S'] = client_socket
                    input_socket.append(client_socket)

                    started = True
                    for x in range(1,10):
                        state[x] = ' '

                    player_address['L'].send(pickling(state))
                    player_address['S'].send(pickling(state))
                    print 'already send state'

                print len(input_socket)
            
            else:
                data = sock.recv(1024)

                if len(input_socket) == 3 and started:
                    if player_address[turn] != sock:
                        sock.send('belum giliran')
                        sock.send(pickling(state))
                    else:
                        state = unpickling(data)
                        
                        for k,v in state.iteritems():
                            if k == v:
                                state[k] = turn

                        win  = check_win(state)

                        if(win):
                            player_address[win].send(pickling('win!'))
                            if win == 'L':
                                player_address['S'].send(pickling('loser'))
                            else:
                                player_address['L'].send(pickling('loser'))
                        
                        else:
                            player_address['L'].send(pickling(state))
                            player_address['S'].send(pickling(state))

                            if turn == 'L':
                                turn = 'S'
                            else:
                                turn = 'L'

                else:
                    sock.send('Not enough player')

except (KeyboardInterrupt, SystemExit):
    print 'Exiting...'
    server_socket.close()
    sys.exit(0)