import tkinter as tk
from tkinter import *
import socket, sys
from threading import Thread
from tkinter import *
from tkinter import font
import tkinter
from cryptography.fernet import Fernet
from tkinter import messagebox
from tkinter.simpledialog import askstring
root = tk.Tk()
root.withdraw()

valid = False
while valid == False:
    name = askstring('Nickname', 'Enter your Nickname \t\t\t\t\t')
    if name != None:

        for letter in name:
            if letter != ' ':
                valid = True
    else:
        sys.exit()
nickname = name
root.quit()
#test

chat = tk.Tk()
chat.title("My Chat")
chat.geometry("1000x460")
chat.resizable(width=False, height=False)


stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.135.184'
port = 8084
 
server_address = ((host, port))
stream_socket.connect(server_address)
stream_socket.sendall(nickname.encode())
def load_key():
    return open("secret.key", "rb").read()
def decrypt_message(message):
    key = load_key()
    f = Fernet(key)
    try:
        decrypted_message = f.decrypt(message)
        return decrypted_message.decode()
    except:
        nachricht = message.decode()
        return nachricht
nachrichten = []
def receiveMessage():
    while True:
        data = stream_socket.recv(2048)
        try:
            print(decrypt_message(data).decode())
        except:
            if data.decode() != 'exit':
                nachricht = Label(chat, text = decrypt_message(data)) 
                nachricht.pack(anchor='w')
                nachrichten.append(nachricht)
                chat.update()
                ycor = nachricht.winfo_rooty()
                print(ycor)
                if int(ycor) > 510:
                    nachrichten[0].destroy()
                    nachrichten.pop(0)


t1 = Thread(target=receiveMessage)
t1.start()


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message



message = Entry(chat, bg="white", font='Helvatica 16')
message.place(x=10, y=410, height=40, width=800)
message.focus()
mychat = Label(chat, text="MyChat", font='Helvatica 18', bg='lightblue', width=1000)
mychat.place(x=0, y=10, width=1000, height=30)
mychat.pack()
sc = Scrollbar(chat, orient="vertical")
sc.pack(side=RIGHT, fill=Y)
def sendMsg(arg=None):
    msg = message.get()
    print('????', msg, '????')
    ismsg = False
    for letter in msg:
        if letter != ' ':
            ismsg = True
    if len(msg) > 510:
        messagebox.showerror(title='Message is too long.', message="Your message can't be longer than 250 Characters. Current length: " + str(len(msg)))
    
    

    elif msg == 'exit':
        stream_socket.sendall(msg.encode())
        stream_socket.close()
        chat.quit()
    
    else:
        if msg != '' and ismsg == True:
            completedMsg = nickname + ': ' + msg
            nachricht = Label(chat, text=completedMsg)
            nachricht.pack(anchor='w')
            nachrichten.append(nachricht)
            chat.update()
            ycor = nachricht.winfo_rooty()
            print(ycor)
            if int(ycor) > 490:
                nachrichten[0].destroy()
                nachrichten.pop(0)
            stream_socket.sendall(encrypt_message(completedMsg))
            message.delete(0,END)


senden = Button(chat, text="Senden", bg="lightblue", command=sendMsg)
senden.place(x=850, y=410, height=40, width=100)
chat.bind("<Return>", sendMsg)


def on_closing():
    stream_socket.sendall(b'exit')
    stream_socket.close()
    chat.quit()


chat.protocol("WM_DELETE_WINDOW", on_closing)
chat.mainloop()
