from audioop import add
import threading 
import socket
from typing import List
from time import sleep

# ! 1 - O usuário deverá tentar se conectar ao servidor

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
HEADER = 64 
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = '00!@!00'
ONLY_ONE_USER = '__001__'
READY_TO_GO = '__002__'
MAX_CONNECTED = 2


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class User:
    def __init__(self, conn, addr, name) -> None:
        self.conn = conn
        self.addr = addr
        self.name = name
        self.send_messages = []


users: List[User] = []


def start_server():
    print('[STARTING SERVER] starting...')
    server.listen()
    run()
    
def run():
    threads: List[threading.Thread] = []
    threads.append(threading.Thread(target=connect, args=()))
    threads[0].start()
    t = 0
    while threads[0].is_alive():
        if len(users) == 1:
            send_wait_message(users[0].conn, ONLY_ONE_USER)
            t += 1
        if len(users) == 2:
            break
        sleep(2)
        print(f'[WAITING] for {t} seconds')
        
    sleep(2)
    send_wait_message(users[0].conn, READY_TO_GO)
    send_wait_message(users[1].conn, READY_TO_GO)
    print('Chat Started...')
    threads.append(threading.Thread(target=messages, args=(users[0].conn, users[0].addr)))
    threads.append(threading.Thread(target=messages, args=(users[1].conn, users[1].addr)))
    threads[1].start()
    threads[2].start()
        
def user_is_connect(addr) -> bool:
    for user in users:
        if user.addr == addr:
            return True
    return False

def connect() -> None:
    while True:
        conn, addr = server.accept()
        if len(users) < 2:
            thread = threading.Thread(target=connect_user, args=(conn, addr))
            thread.start()
        if len(users) == 2:
            break

def connect_user(conn, addr):
    name_len = conn.recv(HEADER).decode(FORMAT)
    if name_len:
        name_len = int(name_len)
        name = conn.recv(name_len).decode(FORMAT)            
        new_user = User(conn, addr, name)
        users.append(new_user)
        print(f'[NEW USER ENTER THE CHAT! ({len(users)} acctive)] {name}')

def send_wait_message(conn, msg: str):
    conn.send(msg.encode(FORMAT))

def messages(conn, addr):
    while True:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(HEADER)
            if users[0].addr == addr:
                send_conn = users[1].conn
            else:
                send_conn = users[0].conn
            msg_len = str(msg_len).encode(FORMAT)
            send_conn.send(msg_len)
            send_conn.send(msg)
            
    
if __name__ == "__main__":
    start_server() 
    