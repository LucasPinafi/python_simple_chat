import tkinter as tk


root = tk.Tk()
text = tk.Text(root, width=40, height=80)
text.place(x=0,y=0)


text.insert('0.0', 'teste\n')
text.insert('0.0', 'teste2\n')
text.insert('0.0', 'teste3\n')

root.mainloop()