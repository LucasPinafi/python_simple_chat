from cgitb import text
import tkinter as tk
from tkinter import ttk
import datetime
import threading

class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.geometry("800x600")
        self.root.title("Simple Chat")

        self.name_label = tk.Label(self.root, text="Your name: ")
        self.name_label.place(x=10, y=20, anchor="w")

        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.place(x=80, y=20, anchor="w")

        self.get_name_button = ttk.Button(self.root, text="OK", command=self.get_name)
        self.get_name_button.place(x=390, y=20, anchor="w")

        self.chat_text = tk.Text(self.root, height=20, width=80)
        self.chat_text.place(x=10, y=210, anchor="w")    
        self.chat_text.config(state=tk.DISABLED)
        
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.chat_text.yview)
        self.scrollbar.place(x=670, y=210, anchor="w")
        self.chat_text['yscrollcommand'] = self.scrollbar.set

        self.send_text = tk.Entry(self.root, width=108)
        self.send_text.place(x=10, y=425, anchor="w")
        self.send_text.config(state=tk.DISABLED)

        self.send_text_button = ttk.Button(self.root, text="SEND", command=self.send_message)
        self.send_text_button.place(x=670, y = 425, anchor="w")
        
        self.line: int = 1
        self.name: str = ""
    
    def show_gui(self) -> None:
        self.root.mainloop()

    def get_name(self) -> None:    
        if self.name_entry.get():
            now = datetime.datetime.now()
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.insert(f'{self.line}.0', f'[{self.name_entry.get()} at {now.hour}:{now.minute}:{now.second} entered the room]')
            self.line += 1
            self.chat_text.config(state=tk.DISABLED)
            self.send_text.config(state=tk.NORMAL)
            self.name_entry.config(state=tk.DISABLED)
            self.name = self.name_entry.get()

    def send_message(self) -> str:
        if self.send_text.get():
            print('ola')
            now = datetime.datetime.now()
            new_message = f'\n[{self.name} at {now.hour}:{now.minute}:{now.second}]: ' + self.send_text.get()
            self.put_messages(new_message)
            return new_message
    
    def put_messages(self, new_message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(f'{self.line}.0', new_message)
        self.chat_text.config(state=tk.DISABLED)
        self.line += 1
        self.send_text.delete(0, 'end')

if __name__ == "__main__":
    gui = Gui()
    gui_thread = threading.Thread(target=gui.show_gui, args=())
    gui_thread.start()

    print('por aqui vai?')

