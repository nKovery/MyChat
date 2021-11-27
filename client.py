import socket
from threading import Thread
from tkinter import *
from cryptography.fernet import Fernet


nickname = input('Enter your Username: ') 

stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
host = 'localhost'
port = 8080
 
server_address = ((host, port))
stream_socket.connect(server_address)
stream_socket.sendall(nickname.encode())
 

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def decrypt_message(message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(message)
    return decrypted_message



def receiveMessage():
    while True:
        data = stream_socket.recv(2048)
        try:
            print(decrypt_message(data).decode())
        except:
            if data.decode() != 'exit':
                print(data.decode()) 

t1 = Thread(target=receiveMessage)
t1.start()




while True:
    message = input()
    if message == 'exit':
        stream_socket.sendall(message.encode())
        stream_socket.close()
        break
    else:

        stream_socket.sendall(encrypt_message(message))


