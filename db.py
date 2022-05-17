import sqlite3
from tkinter import *
from datetime import date

roomnumberallocated = 0
roomtypeallocated = ''
roompriceallocated = 0

def resetroomdetails():
    global roomnumberallocated
    global roomtypeallocated
    global roompriceallocated

    roomnumberallocated = 0
    roomtypeallocated = ''
    roompriceallocated = 0    

def calcnumdays(co, ci):
    d0 = date(co[2], co[1], co[0])
    d1 = date(ci[2], ci[1], ci[0])
    delta = d0 - d1
    return delta.days


def allocateroom(rt, rp, ecin, eco):
    global roomnumberallocated
    global roomtypeallocated
    global roompriceallocated

    #Calculate room price based on number of days considering 10% advance payment
    co = eco.get().split('/')
    co[0] = int(co[0])
    co[1] = int(co[1])
    co[2] = int(co[2])

    ci = ecin.get().split('/')
    ci[0] = int(ci[0])
    ci[1] = int(ci[1])
    ci[2] = int(ci[2])

    delta = calcnumdays(co, ci)
    price = roompriceallocated * delta * 0.9
    return roomnumberallocated, roomtypeallocated, price

def roomselected(v, rt, rp, b):
    global roomnumberallocated
    global roomtypeallocated
    global roompriceallocated

    b['state'] = DISABLED
    #Update room status
    # conn = sqlite3.connect('hms.db')
    # c = conn.cursor()

    # c.execute('UPDATE roomdetails SET roomstatus=? WHERE roomnumber=?', ('BUSY', v))
    roomnumberallocated = v
    roomtypeallocated = rt
    roompriceallocated = rp

    # conn.commit()
    # conn.close()
    return

#Query Database for available rooms of type=Type
def showavailablerooms(t, rt, rp, r):
    conn = sqlite3.connect('hms.db')
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM roomdetails WHERE roomtype=? AND roomstatus=?', (rt, 'FREE'))
    except:
        print('No rooms matching Roomtype ' + rt)
        return r
    
    results = c.fetchall()

    if(len(results) > 0):
        v = IntVar()
        c = 1
        l = Label(t, text='Available rooms for ' + rt, justify=LEFT)
        l.grid(row=r, column=0,sticky='W')
        #r += 1
        for result in results:
            rb = Radiobutton(t, text=str(result[0]), variable=v, value=result[0], width=10)
            rb.grid(row=r, column=c)
            c += 1

        r += 1    
        b = Button(t, text='Confirm', command=lambda:roomselected(v.get(), rt, rp, b))
        b.grid(row=r, column=1)
        r += 1
    else:
        print('Query returned no results')

    conn.commit()
    conn.close()
    return r


def initroomdb(roomtype, roomprice, roomdesc):
    conn = sqlite3.connect('hms.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS roomdetails
                (
                    roomnumber int not null,
                    roomtype text not null,
                    roomprice int not null,
                    roomstatus text not null,
                    roomdesc text not null,
                    unique(roomnumber)
                )''')
    
    c.execute('SELECT * FROM roomdetails')
    results = c.fetchall()
    if len(results) == 0:
        #We have 5 rooms for each type
        for i in range(100,105):
            try:
                c.execute("INSERT INTO roomdetails VALUES (:n,:t,:p,:s,:d)",
                        {
                            'n': i,
                            't': roomtype[0],
                            'p': roomprice[0],
                            's': 'FREE',
                            'd': roomdesc[0]
                        })
            except:
                print('Room details already exists')

        for i in range(200,205):
            try:
                c.execute("INSERT INTO roomdetails VALUES (:n,:t,:p,:s,:d)",
                        {
                            'n': i,
                            't': roomtype[1],
                            'p': roomprice[1],
                            's': 'FREE',
                            'd': roomdesc[1]
                        })
            except:
                print('Room details already exists')

        for i in range(300,305):
            try:
                c.execute("INSERT INTO roomdetails VALUES (:n,:t,:p,:s,:d)",
                        {
                            'n': i,
                            't': roomtype[2],
                            'p': roomprice[2],
                            's': 'FREE',
                            'd': roomdesc[2]
                        })
            except:
                print('Room details already exists')

        for i in range(400,405):
            try:
                c.execute("INSERT INTO roomdetails VALUES (:n,:t,:p,:s,:d)",
                        {
                            'n': i,
                            't': roomtype[3],
                            'p': roomprice[3],
                            's': 'FREE',
                            'd': roomdesc[3]
                        })
            except:
                print('Room details already exists')

        conn.commit()
    else:
        print('Room details already created')

    conn.close()
    return


def confirmcheckout(t, b, records, r):
    b['state'] = DISABLED
    conn = sqlite3.connect('hms.db')
    c = conn.cursor()

    for record in records:
        l = Label(t, text='Checking out guest: ' + record[0])
        l.grid(row=r, column=0)
        r += 1
        try:
            c.execute('UPDATE roomdetails SET roomstatus=? WHERE roomnumber=?', ('FREE', record[5]))
        except:
            print('Cannot update Status for Room number: ' + str(record[5]))
        try:
            c.execute("DELETE FROM guestdetails WHERE guestname=? AND guestphone=? AND oid=?", 
                    (str(record[0]), str(record[1]), record[8]))
        except:
            print('Cannot Delete Guest details for Guestname: ' + str(record[0]) + ' Guestphone: ' + str(record[1]))

    conn.commit()
    conn.close()

def checkout(t, en, eph, b):
    guestname = en.get()
    guestph = eph.get()

    conn = sqlite3.connect('hms.db')
    c = conn.cursor()
    c.execute('SELECT *, oid FROM guestdetails WHERE guestname=? AND guestphone=?', (guestname, guestph))

    records = c.fetchall()
    numrecords = len(records)

    if(numrecords > 0):
        b['state'] = DISABLED
        l = Label(t, text = 'Guest: ' + guestname + ' and Phone number: ' + guestph + ' current reservation(s)')
        l.grid(row=3, column=0)

        r = 4
        for record in records:
            l2 = Label(t, text='Room number: ' + str(record[5]))
            l3 = Label(t, text='Room charges: ' + str(record[7]))

            l2.grid(row = r, column = 0)
            l3.grid(row = r, column = 1)
            r += 1

        #Payment method
        def show():
            label.config( text = clicked.get() )
            
        # Dropdown menu options
        options =["Credit/ Debit", "Paytm/ PhonePe", "UPI", "Cash"]
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set( "UPI" )
        
        # Create Dropdown menu
        drop = OptionMenu( t , clicked , *options )
        drop.grid(row=r+1,column=0)
    

        # Create button, it will change label text
        button = Button( t , text = "Pay" , command = show )
        button.grid(row=r+1,column=2)
        
        # Create Label
        label = Label( t , text = " " )
        label.grid()
        b2 = Button(t, text='Confirm', command=lambda:confirmcheckout(t, b2, records, r+1))
        b2.grid(row=r+2, column=1)

    else:
        l = Label(t, text='Enter Valid Name and Phone number')
        l.grid(row=4, column=0)
    conn.commit()
    conn.close()
    return

def queryguestdetails(t):
    conn = sqlite3.connect('hms.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guestdetails")

    records = c.fetchall()
    numrecords = len(records)
    columns = []

    if(numrecords > 0):
        for col in c.description:
            columns.append(col[0])
        
        numcols = len(columns)

        #Print column names
        for i in range(numcols):
            e = Entry(t, width = 20)
            e.grid(row = 0, column = i)
            e.insert(END, columns[i])

        #Print rows
        r = 1
        for record in records:
            for i in range(len(record)):
                e = Entry(t, width = 20)
                e.grid(row = r, column = i)
                e.insert(END, record[i])
            r += 1
    else:
        print('Query returned no results')

    conn.commit()
    conn.close()

def createguestdetails(ename,eph,eaddr,ecin,eco,roomtype, roomprice, b):
    b['state'] = DISABLED

    #Validate and store in DB
    conn = sqlite3.connect('hms.db')
    c = conn.cursor()

    #Check if our table exists, if not create one - table is created only once
    c.execute('''CREATE TABLE IF NOT EXISTS guestdetails
                (
                    guestname text,
                    guestphone text,
                    guestaddr text,
                    guestcin text,
                    guestco text,
                    guestroomno int,
                    guestroomtype text,
                    guestcharges int
                )''')
    conn.commit()

    #Insert Guest details post validation
    (rmno, rt, rp) = allocateroom(roomtype, roomprice, ecin, eco)

    #Update Room status to busy
    c.execute('UPDATE roomdetails SET roomstatus=? WHERE roomnumber=?', ('BUSY', rmno))

    c.execute("INSERT INTO guestdetails VALUES (:n,:p,:a,:ci,:co,:rn,:rt,:rc)",
                {
                    'n': ename.get(),
                    'p': eph.get(),
                    'a': eaddr.get(),
                    'ci': ecin.get(),
                    'co': eco.get(),
                    'rn': rmno,
                    'rt': rt,
                    'rc': rp
                })
    resetroomdetails()

    conn.commit()

    #Clear the text fields
    ename.delete(0, END)
    eph.delete(0, END)
    eaddr.delete(0, END)
    ecin.delete(0, END)
    eco.delete(0, END)

    conn.close()
