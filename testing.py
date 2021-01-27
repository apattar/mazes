from tkinter import *
from tkinter import ttk

class Thing(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __eq__(self, other):
        return self.a == other.a
    
    def __hash__(self):
        return hash(self.a) # have to hash the things
                            # that make up identity of
                            # the object
    
    def __repr__(self):
        return f'a{self.a} b{self.b}'
    
t1 = Thing(1, 2)
t2 = Thing(1, 3)
t3 = Thing(2, 5)

things = set([t2, t3])
print(t1 in things)     # prints True

print(list(things))
newthing = things.remove(t1)
print(list(things))
print(newthing)


# root = Tk()

# def orig():
#     print('orig function called')
#     but.configure(command=new) 

# def new():
#     print('new function called')

# but = ttk.Button(command=orig)
# but.grid()


# root.mainloop()