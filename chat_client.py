import socket
import threading
from typing import List

PORT = 5050
SERVER = '192.168.1.15' # -> casa
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
NAME = input('Digite seu nome: ')
ONLY_ONE_USER = '__001__'

client = None
messages_sent: List[str] = []
messages_obt: List[str] = []

def get_send_lens(msg: str):
    msg_len = len(msg)
    send_msg_len = str(msg_len).encode(FORMAT)
    send_msg_len += b' ' * (HEADER - len(send_msg_len))
    return send_msg_len

def server_connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    name = NAME.encode(FORMAT)
    send_name_len = get_send_lens(name)
    
    client.send(send_name_len)
    client.send(name)
    
    start_chat()
    
def start_chat():
    global client
    while True:
        msg: str = client.recv(2048).decode(FORMAT)
        if msg == ONLY_ONE_USER:
            print('Waiting for another user...')
        else:
            break
    
    send = threading.Thread(target=send_messages, args=())
    get = threading.Thread(target=get_messages, args=())
    
    send.start()
    get.start()      
    
def send_messages():
    while True:
        msg = input('[Write Here]: ')
        msg_len = get_send_lens(msg)
        msg_send = msg.encode(FORMAT)
        
        client.send(msg_len)
        client.send(msg_send)
        
        messages_sent.append(msg)
    
def get_messages():
    while True:
        msg_len = client.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = client.recv(msg_len)
            msg = msg.decode(FORMAT)
            print(f'\n[you get it...] {msg}')
            messages_obt.append(msg)
           
service_thread = threading.Thread(target=server_connect, args=())  
service_thread.start()
   
    
