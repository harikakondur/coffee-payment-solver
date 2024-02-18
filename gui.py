# MySQL Connectivity
import mysql.connector as sqltor
from config import MYSQL_CONFIG  # Import the configuration
mycon = sqltor.connect(**MYSQL_CONFIG)
csr = mycon.cursor()

from coffee import *
from tkinter import *
from coffee import calculateMaxDebt

def addvalues():
    updateDebts()
    r1 = (214, 219, 173)
    h1 = "#{:02x}{:02x}{:02x}".format(*r1)
    c.create_rectangle(15, 120, 400, 390, fill=h1, outline="olive", width=2)

    csr.execute("SELECT name, drink_preference, price, debt,count FROM coworkers")
    coworker_values = csr.fetchall()
    print('values',coworker_values)
    for j, coworker_row in enumerate(coworker_values):
        # Display coworker attributes
        for i, value in enumerate(coworker_row):
            rgb_color = (98, 54, 28)
            hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
            c.create_text(w[i], h[j], text=str(value), font=('PT Mono', 13), anchor="nw", fill=hex_color, tags="values")

def displayValues():
    newTransaction()
    addvalues()

# Main window
root = Tk()
root.geometry('425x740')
root.title("Coffee Payment Solver")
root.resizable(False, False)

#canvas
bg = PhotoImage(file='bg.png')
c = Canvas(root, width=400, height=600)
c.pack(fill="both", expand=True)
c.create_image(0, 0, image=bg, anchor='nw')

#button command: Who's turn?
def displayNextPayer():
    c.delete("name")
    d, nextPayerId,nextPayerName = calculateMaxDebt()
    
    # Create and display the new widget with the tag "name"
    name_widget = Label(c, text=nextPayerName, font=('PT Mono', 15))
    name_widget.pack()
    c.create_window(200, 14, window=name_widget, anchor="nw", tags="name")
  

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
