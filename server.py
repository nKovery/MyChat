import socket
from _thread import *
from tkinter import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
host = 'localhost'
port = 8080
 
sock.bind((host, port))
sock.listen(5)
 
connections = []
send = []



 
def sendMessage(msg):
    for con in connections:
        if con == send[0]:
            pass
        else:
            try:
                con.sendall(msg.encode())
            except:
                pass
        
 
 
def receiveMessage(c, addr, nname):
    while True:
        
        data = c.recv(2048).decode('utf-8')
        print(data)
        send.append(c)
        if len(connections) == 1:
            try:
                c.sendall(b'No other users are currently online, so your message wasnt sent')
            except:
                pass
        else:
            sendMessage(data)
        send.remove(c)
        if data == 'exit':
            
            disconnected_message = str(nname) + ' left the Chat.'
            print(addr, 'disconnected.')
            for con in connections:
                try:
                    con.sendall(disconnected_message.encode())
                except:
                    pass
            connections.remove(c)
            c.close()
            break
            
        



while True:
    connection, client = sock.accept()
    username = connection.recv(2048).decode('utf-8')
    entered_message = str(username) + ' entered the Chat.'
    connections.append(connection)
    for con in connections:
        con.sendall(entered_message.encode())


    start_new_thread(receiveMessage, (connection, client, username))
