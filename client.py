import socket
import threading
from tkinter import ttk
import tkinter as tk
from datetime import datetime

# ! Protocolos
PORT = 5050
SERVER =   '192.168.1.15' # -> IME  '172.15.4.20'
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
ONLY_ONE_USER = '__001__'
READY_TO_GO = '__002__'

# ! variáveis globais
client = None
lines = 1
user_name = ""
friend_name = ""

def get_name() -> None:
    global user_name, lines
    if name_entry.get():
        now = datetime.now()
        chat_text.config(state=tk.NORMAL)
        user_name = name_entry.get()
        chat_text.insert(f'{lines}.0', f'User [{user_name} logged in at {now.hour}:{now.minute}:{now.second}]')
        lines += 1
        chat_text.config(state=tk.DISABLED)
        send_text.config(state=tk.NORMAL)
        name_entry.config(state=tk.DISABLED)
        
        

def send_messages() -> None:
    print('aqui')
    if send_text.get():
        now = datetime.now()
        msg = f'\n[You sent at {now.hour}:{now.minute}:{now.second}]: ' + send_text.get()
        put_messages_screen(msg)
    
        msg_len = get_send_len(msg)
        msg_send = msg.encode(FORMAT)
        client.send(msg_len)
        client.send(msg_send)

def get_messages() -> None:
    global friend_name
    while True:
        msg_len = client.recv(HEADER).decode(FORMAT)
        if msg_len:
            now = datetime.now()
            msg_len = int(msg_len)
            msg = client.recv(msg_len)
            msg = msg.decode(FORMAT)
            new_message = f'\n[{friend_name} at {now.hour}:{now.minute}:{now.second}]: ' + msg
            put_messages_screen(new_message)
            
def put_messages_screen(new_message: str) -> None:
    global lines
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(f'{lines}.0', new_message)
    chat_text.config(state=tk.DISABLED)
    lines += 1
    send_text.delete(0, 'end')
        
def get_send_len(msg: str) -> str:
    msg_len = len(msg)
    send_msg_len = str(msg_len).encode(FORMAT)
    send_msg_len += b' ' * (HEADER - len(send_msg_len))
    return send_msg_len

def server_coonect() -> None:
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    t = 0 
    while user_name == "":
        continue
    name = user_name.encode(FORMAT)
    send_name_len = get_send_len(name)
    client.send(send_name_len)
    client.send(name)
    print(user_name + " ue " + str(t))
    t += 1
    
    start_chat()

def start_chat() -> None:
    global lines, friend_name
    while True:
        msg: str = client.recv(2048)
        if msg:
            msg = msg.decode(FORMAT)
            if msg == ONLY_ONE_USER:
                chat_text.config(state=tk.NORMAL)
                chat_text.insert(f'{lines}.0', f'\n[WAITING FOR ANOTHER USER...]')
                chat_text.config(state=tk.DISABLED)
                lines += 1
                print(lines)
            if READY_TO_GO in msg:
                friend_name = msg[7:]
                print("PRONTOO")
                break
        
    messages_get = threading.Thread(target=get_messages, args=())    
    messages_get.start()

def show_gui() -> None:
    root.mainloop()
            
root = tk.Tk()
root.resizable(False, False)
root.geometry("800x600")
root.title("Simple Chat")

name_label = tk.Label(root, text="Your name: ")
name_label.place(x=10, y=20, anchor="w")

name_entry = tk.Entry(root, width=50)
name_entry.place(x=80, y=20, anchor="w")

get_name_button = ttk.Button(root, text="OK", command=get_name)
get_name_button.place(x=390, y=20, anchor="w")

chat_text = tk.Text(root, height=20, width=80)
chat_text.place(x=10, y=210, anchor="w")
# chat_text.config(state=tk.DISABLED)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=chat_text.yview)
scrollbar.place(x=670, y=210, anchor="w")
chat_text['yscrollcommand'] = scrollbar.set

send_text = tk.Entry(root, width=108)
send_text.place(x=10, y=425, anchor="w")
send_text.config(state=tk.DISABLED)

send_text_button = ttk.Button(root, text="SEND", command=send_messages)
send_text_button.place(x=670, y=425, anchor="w")

service_thread = threading.Thread(target=server_coonect, args=())
service_thread.start()

show_gui()


