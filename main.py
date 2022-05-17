from tkinter import *
from guestreserve import *
from report import *
from guestcheckout import *

#Hotel managment application main screen
#This is used by Hotel administrator or receptionist
#Hotel admin can perform the following operations
#1. Room reservation for guest(s)
#2. Room checkout
#3. View room booking report
root = Tk()
root.title('Hotel Management System')
l1 = Label(root, text='HOTEL MANAGEMENT SYSTEM - ADMIN TOOL')
l1.grid(row=0, column=0, columnspan=3, sticky='NSEW')
b1 = Button(root, text="Room reservation",border=5, padx=50, pady=20, command=reserve)
b1.grid(row=1, column=0)
b2 = Button(root, text="Guest Checkout", border=5, padx=50, pady=20, command=guestcheckout)
b2.grid(row=1, column=1)
b3 = Button(root, text="Report", border=5, padx=75, pady=20, command=report)
b3.grid(row=1, column=2)

root.mainloop()