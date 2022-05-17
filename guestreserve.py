from tkinter import *
from db import *
from utils import *

#Room configuration. This will be stored in Database
roomtype = ["Type1", "Type2", "Type3", "Type4"]
roomprice = [1000, 2000, 3000, 4000]
roomdesc = [
    "Single bed, AC, Microwave, TV",
    "Double bed, AC, Microwave, TV, Coffeemaker",
    "Apartment, AC, Kitchen, TV",
    "Suite, AC, Kitchen, TV, Jacuzzi"]

#This function is invoked by reserve() function
#The user collects user inputs to make the reservation
#Based on the user inputs and the selected room type, room is allocated
#The allocated room details are stored in the database
def confirm(t,lrt,lrp,lrf,ladv,choice, b):
    #Discard any content in the label from previous operation
    lrt.grid_forget()
    lrp.grid_forget()
    lrf.grid_forget()

    #User should not click again
    b['state'] = DISABLED
    
    #Index into roomprice and roomfeatures we need 0 based
    rt = choice.get()
    if(rt == 'Type1'):
        c = 0
    elif(rt == 'Type2'):
        c = 1
    elif(rt == 'Type3'):
        c = 2
    elif(rt == 'Type4'):
        c = 3
 
    #Display user the Room details and Room type availability and advance payment
    #10% advance is mandated
    lrt['text'] = "Your Room type: " + rt
    lrt.grid(row=2,column=0, columnspan=2,sticky='W')

    r = showavailablerooms(t, rt, roomprice[c], 3)

    lrp['text'] = "Room price per day: " + str(roomprice[c])
    lrp.grid(row=r,column=0, columnspan=2,sticky='W')

    lrf['text'] = "Room features: " + str(roomdesc[c])
    lrf.grid(row=r+1,column=0, columnspan=2,sticky='W')

    ladv['text'] = "Advance Payment (10%/day): " + str((10/100) * roomprice[c])
    ladv.grid(row=r+2,column=0,columnspan=2,sticky='W')

    guestnameentry(t, r+3, 0)
    guestphoneentry(t, r+5, 0)
    guestaddrentry(t, r+7, 0)
    guestcinentry(t, r+9, 0)
    guestcotentry(t, r+11, 0)

  
    button_entry = Button(t,text="Enter",command=lambda:printsummary(t, roomtype[c], roomprice[c], button_entry))
    button_entry.grid(row=r+12,column=2,sticky="EW")
    #Deactivate Enter button

#This function is executed when user clicks the Reserve button on main screen
#We open a new application window and perform the guest reservation function
def reserve():
    choice = StringVar()
    choice.set(roomtype[0])

    #Initiatize Room database
    initroomdb(roomtype, roomprice, roomdesc)

    #Open a new Window
    t = Toplevel()
    t.geometry("800x600")

    #Allow user to select Roomtype
    l = Label(t, text="Room Type")
    l.grid(row=0, column=0,sticky='W')
    rt = OptionMenu(t, choice, *roomtype)
    rt.grid(row=0,column=1)

    lrt = Label(t)
    lrp = Label(t)
    lrf = Label(t)
    ladv = Label(t)
   
    b = Button(t, text="Confirm", command=lambda:confirm(t,lrt,lrp,lrf,ladv,choice,b))
    b.grid(row=0,column=2)
