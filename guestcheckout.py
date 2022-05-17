from tkinter import *
from db import *
from guestreserve import*

def guestcheckout():
    #Open a new window
    t = Toplevel()

    ln = Label(t, text='Enter Guest Name')
    en = Entry(t, width = 20)

    lph = Label(t, text='Enter Guest phone number')
    eph = Entry(t, width = 20)

    ln.grid(row = 0, column = 0,sticky='W')
    en.grid(row = 0, column = 2)
    lph.grid(row = 1, column=0,sticky='W')
    eph.grid(row = 1, column = 2)
    
    b = Button(t, text='Enter', command=lambda:checkout(t, en, eph, b))
    b.grid(row=3, column = 1, columnspan=2)
    
    #Query Database
