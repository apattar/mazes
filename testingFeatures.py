from tkinter import *
from tkinter import ttk

root = Tk()
canvas = Canvas(root, width=300, height=300)
canvas.grid(sticky='nsew')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

def displayWidthHeight(canvas):
    canvas.update_idletasks()
    canvas.delete(ALL)
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    canvas['width'] = w - 4
    canvas['height'] = h - 4
    canvas.create_text(w//2, h//2, text='Width: %d\nHeight: %d' % (w,h),
                       anchor='center')

root.bind('<Configure>', lambda e: displayWidthHeight(canvas))
root.mainloop()