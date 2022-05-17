from tkinter import *
import re
from db import *

def validatename(name):
    tmp = name.split(" ")
    tmp1 = ""
    for i in range(len(tmp)):
        tmp1 += tmp[i]
     #Check if the name is a alphabet string
    if tmp1.isalpha():
        return True
    else:
        return False

def submitname(t, ename, r, l, b):
    l.grid_forget()
    result = validatename(ename.get())
    

    if(result is True):
        print('ValidName')
        #Deactivate Enter button
        b['state'] = DISABLED
    else:
        print('Invalidname')
        ename.delete(0, END)
        l['text'] = 'Invalid name please retry'
        l.grid(row=r, column=0)

def guestnameentry(t,r, c):
    l = Label(t, text="Guest Name")
    l.grid(row=r, column=c,sticky='W')
    global ename
    ename = Entry(t)
    ename.grid(row=r,column=c+1,columnspan=2)

    l2 = Label(t)
    b = Button(t, text='Enter', command=lambda:submitname(t, ename, r+1, l2, b))
    b.grid(row=r, column=c+3)

    return

def validatephone(s):
    
    # 1) Begins with 0 or 91
    # 2) Then contains 6 or 7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)

def submitphno(t, eph, r, l, b):
    l.grid_forget()
    ph_length = len(eph.get())
    result = validatephone(str(eph.get()))

    if(result and ph_length < 12 ):
        print('Valid Phone number')
        #Deactivate Enter button
        b['state'] = DISABLED
    else:
        print('Invalid phone number')
        eph.delete(0, END)
        l['text'] = 'Invalid phone number please retry'
        l.grid(row=r, column=0)
    return

def guestphoneentry(t, r, c):
    l = Label(t, text="Guest Phone")
    l.grid(row=r, column=c,sticky='W')
    global eph
    eph = Entry(t)
    eph.grid(row=r,column=c+1,columnspan=2)

    l2 = Label(t)
    b = Button(t, text='Enter', command=lambda:submitphno(t, eph, r+1, l2, b))
    b.grid(row=r, column=c+3)
    return

def submitaddr(t, eaddr, b):
    #Deactivate Enter button and there is no address validation
    b['state'] = DISABLED
    return

def guestaddrentry(t, r, c):
    l = Label(t, text="Guest Address")
    l.grid(row=r, column=0,sticky='W')
    global eaddr
    eaddr = Entry(t)
    eaddr.grid(row=r,column=c+1,columnspan=2)

    b = Button(t, text='Enter', command=lambda:submitaddr(t,eaddr, b))
    b.grid(row=r, column=c+3)
    return

def validate_date(d):
    if d[2] < 2021 or d[2] > 2022:
        print("Invalid Year. Please select 2021 or 2022")
        return False
    if d[1] < 1 or d[1] > 12:
        print("Invalid Month. Please select between 1 and 12")
        return False
    if d[1] == 2:
        if d[2] % 4 == 0 and d[0] < 1 or d[0] > 29:
            print("Leap year and Feb can have dates only till 29")
            return False
    elif d[1] == 1 or d[1] == 3 or d[1] == 5 or d[1] == 7 or d[1] == 8 or d[1] == 10 or d[1] == 12:
        if d[0] < 1 or d[0] > 31:
            print("Jan, March, May, July, Aug, Oct, Dec can have 31 days only")
            return False
    elif d[0] == 4 or d[1] == 6 or d[1] == 9 or d[1] == 11:
        if d[0] < 1 or d[0] > 30:
            print("Apr, Jun, Sep, Nov can have 30 days only")
            return False
    return True

def submitcheckin(t, cin, r, l, b):
    l.grid_forget()
    ci = cin.get().split('/')
    ci[0] = int(ci[0])
    ci[1] = int(ci[1])
    ci[2] = int(ci[2])
    result = validate_date(ci)
    
    if(result is True):
        print('Valid checkin date')
        #Deactivate Enter button
        b['state'] = DISABLED
    else:
        print('Invalid checkin date')
        cin.delete(0, END)
        l['text'] = 'Invalid checkin date please retry'
        l.grid(row=r, column=0)
    return


def guestcinentry(t, r, c):

    l = Label(t, text="Guest Checkin")
    l.grid(row=r, column=0,sticky='W')
    global ecin
    ecin = Entry(t)
    ecin.grid(row=r,column=c+1,columnspan=2)
   
    l2 = Label(t)
    b = Button(t, text='Enter', command=lambda:submitcheckin(t, ecin, r+1, l2, b))
    b.grid(row=r, column=c+3)
    return

def submitcheckout(t, cout, r, l, b):
    l.grid_forget()
    co = cout.get().split('/')
    co[0] = int(co[0])
    co[1] = int(co[1])
    co[2] = int(co[2])
    result = validate_date(co)
    
    ci = ecin.get().split('/')
    ci[0] = int(ci[0])
    ci[1] = int(ci[1])
    ci[2] = int(ci[2])

    #Calculate number of days
    noofdays = calcnumdays(co, ci)
    print(noofdays)
    result2 = False

    if(noofdays > 0):
        result2 = True

    if(result is True and result2 is True):
        print('Valid checkout date')
        #Deactivate Enter button
        b['state'] = DISABLED
    else:
        print('Invalid checkout date')
        cout.delete(0, END)
        l['text'] = 'Invalid checkout date please retry'
        l.grid(row=r, column=0)
    return

def guestcotentry(t, r, c):
    l = Label(t, text="Guest Checkout")
    l.grid(row=r, column=0,sticky='W')
    global eco
    eco = Entry(t)
    eco.grid(row=r,column=c+1,columnspan=2)
   
    l2 = Label(t)
    b = Button(t, text='Enter', command=lambda:submitcheckout(t, eco, r+1, l2, b))
    b.grid(row=r, column=c+3)
    return

def printsummary(t, roomtype, roomprice, b):
    l = Label(t, text = 'Dear Guest here is your booking summary')
    l1 = Label(t, text ="Name :" + ename.get())
    l2 = Label(t, text ="Phone Number :"+" "+eph.get())
    l3 = Label(t, text ="Address: "+" "+ eaddr.get())
    l4 = Label(t, text ="Check In date:"+" "+ecin.get())
    l5 = Label(t, text="Check Out date"+" "+eco.get())
    l6 = Label(t, text = 'Do you Confirm')

    b2 = Button(t, text='Confirm Booking', command=lambda:createguestdetails(ename,eph,eaddr,ecin,eco, roomtype, roomprice, b2))
    
    l.grid(row=18,column=0,padx=10,pady=5,sticky="W")
    l1.grid(row=19,column=0,padx=10,pady=5,sticky="W")
    l2.grid(row=20,column=0,padx=10,pady=5,sticky="W")
    l3.grid(row=21,column=0,padx=10,pady=5,sticky="W")
    l4.grid(row=22,column=0,padx=10,pady=5,sticky="W")
    l5.grid(row=23,column=0,padx=10,pady=5,sticky="W")
    l6.grid(row=24,column=0,columnspan=2,padx=10,pady=10,sticky="W")
    b2.grid(row=25,column=0,columnspan=2,padx=10,pady=10,sticky="EW")

    exit_button = Button(t, text="Exit", command=t.destroy)
    exit_button.grid(row=27,column=0,columnspan=2,padx=20,pady=20)

    #Deactivate Confirm booking button
    b['state'] = DISABLED
    