from tkinter import *
from tkinter import ttk

root = Tk()

def orig():
    print('orig function called')
    but.configure(command=new) 

def new():
    print('new function called')

but = ttk.Button(command=orig)
but.grid()


root.mainloop()

