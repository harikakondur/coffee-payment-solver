# MySQL Connectivity
import mysql.connector as sqltor
mycon = sqltor.connect(
    host='localhost',
    user='root',
    passwd='harikakondur',
    database='coffee')
csr = mycon.cursor()

from coffee import *
from tkinter import *
from coffee import calculateMaxDebt

def addvalues():
    r1 = (214, 219, 173)
    h1 = "#{:02x}{:02x}{:02x}".format(*r1)
    c.create_rectangle(15, 120, 400, 390, fill=h1, outline="olive", width=2)
    
    # Assuming the SQL query fetches all rows from the 'coworkers' table
    csr.execute("SELECT coworkers.name, coworkers.drink_preference, coworkers.price, coworkers.debt, sub.transaction_count FROM coworkers JOIN (SELECT payer, COUNT(tid) AS transaction_count FROM transactions GROUP BY payer) AS sub ON coworkers.cid = sub.payer;")
    values = csr.fetchall()
    # Display the values
    for j, row in enumerate(values):
        for i, value in enumerate(row):
            rgb_color = (98, 54, 28)
            hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
            c.create_text(w[i], h[j], text=str(value), font=('PT Mono', 13), anchor="nw", fill=hex_color, tags="values")


def displayValues():
    newTransaction()
    addvalues()

# Create the main window
root = Tk()
root.geometry('425x740')
root.title("Coffee Payment Solver")
root.resizable(False, False)

#canvas
bg = PhotoImage(file='bg.png')
c = Canvas(root, width=400, height=600)
c.pack(fill="both", expand=True)
c.create_image(0, 0, image=bg, anchor='nw')

def displayNextPayer():
    c.delete("name")

    d, nextPayerId = calculateMaxDebt()
    coworkers = getAllCoworkers()
    name = [coworker[0] for coworker in coworkers if coworker[1] == nextPayerId]

    if name:
        payer = name[0]
        # Create and display the new widget with the tag "name"
        name_widget = Label(c, text=payer, font=('PT Mono', 15))
        name_widget.pack()
        c.create_window(200, 14, window=name_widget, anchor="nw", tags="name")
    else:
        print("No next payer found.")

# buttons
button1 = Button(root, text="Who's turn?", font=('PT Mono', 15), command=displayNextPayer)
button2 = Button(root, text="Pay", font=('PT Mono', 15), bg='#2E8B57', relief='flat', command=displayValues)
button1_canvas = c.create_window(20, 10, anchor="nw", window=button1)

button2_canvas = c.create_window(320, 10,
                                 anchor="nw",
                                 window=button2)

# Table
widget = Label(c, text='Name', font=('PT Mono', 15))
widget.pack()
c.create_window(20, 80, window=widget, anchor="nw")
widget = Label(c, text='Drink', font=('PT Mono', 15))
widget.pack()
c.create_window(90, 80, window=widget, anchor="nw")
widget = Label(c, text='Price', font=('PT Mono', 15))
widget.pack()
c.create_window(220, 80, window=widget, anchor="nw")
widget = Label(c, text='Debt', font=('PT Mono', 15))
widget.pack()
c.create_window(290, 80, window=widget, anchor="nw")
widget = Label(c, text='Count', font=('PT Mono', 15))
widget.pack()
c.create_window(350, 80, window=widget, anchor="nw")
w = [20, 90, 220, 290, 360]
h = [130, 170, 210, 250, 290, 330, 370]

addvalues()

root.mainloop()
