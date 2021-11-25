import socket, time
from threading import Thread
from tkinter import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
host = '192.168.137.75'

port = 8080
 
sock.bind((host, port))
sock.listen(1)
 

connection, client = sock.accept()
 
print(client, 'connected')
 
 
def receiveMessage():
    while True:
        data = connection.recv(2048).decode('utf-8')
        print("\n"+ data) 

t1 = Thread(target=receiveMessage)
t1.start()

while True:
    
    message = input().encode()
    connection.sendall(message)

 
 
