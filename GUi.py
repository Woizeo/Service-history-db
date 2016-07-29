import tkinter
import tkinter.messagebox as msgbox
import sqlite3 as lite
import sys
import time



top = tkinter.Tk()

w = 200 # width for the Tk root
h = 150 # height for the Tk root

# get screen width and height
ws = top.winfo_screenwidth() # width of the screen
hs = top.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
top.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Database test
con = None

# http://www.tutorialspoint.com/python/python_gui_programming.htm

try:
	con = lite.connect('test.db')
    
	cur = con.cursor()    
	cur.execute('SELECT SQLITE_VERSION()')
    
	data = cur.fetchone()
    
	msgbox.showinfo ("SQLite","SQLite version: %s" % data)

	cur.execute('CREATE TABLE IF NOT EXISTS Service(operation CHAR(255), mileage INT, cost INT, doneBy CHAR(255));')
	cur.execute('CREATE TABLE IF NOT EXISTS Repair(operation CHAR(255), mileage INT, cost INT, doneBy CHAR(255));')
	cur.execute('CREATE TABLE IF NOT EXISTS Note(operation CHAR(255), mileage INT, cost INT, doneBy CHAR(255));')
	
	
except lite.Error:
	msgbox.showinfo ("Database error","Error: %s" % e.args[0])
	time.sleep(2)
	sys.exit(1)
    
finally:
    
	if con:
		con.close()

# GUI test

def saveButtonCallBack(E1, E2, E3, E4, var):
	msgbox.showinfo ("Save pressed!")
	print(var.get())
	print(E1.get())
	print(E2.get())
	print(E3.get())
	print(E4.get())
	# CHECK FOR INTEGERS!
	print("Variables read: %s, %d, %d, %s" % (E1.get(), int(E2.get()), int(E3.get()), E4.get()))
	if var.get() == 1:
		insertCommand = "INSERT INTO Service (operation, mileage, cost, doneBy) VALUES "
	elif var.get() == 2:
		insertCommand = "INSERT INTO Repair VALUES "
	elif var.get() == 3:
		insertCommand = "INSERT INTO Note VALUES "
	else:
		msgbox.showinfo ("Var is zero!")
	op = E1.get()
	mil = E2.get()
	cost = E3.get()
	done = E4.get()
	msgbox.showinfo ("Info","Variables read: %s, %d, %d, %s" % (op, int(mil), int(cost), done))

	if not var.get() == 0:
		values = "('%s', %d, %d, '%s');" % (op, int(mil), int(cost), done)
		insertCommand = insertCommand+values
		print(insertCommand)
		con = lite.connect('test.db')
		print("Connected to db")
		cur = con.cursor()    
		cur.execute(insertCommand)
		print("Executed insert")
		con.commit()
		print("Committed")
		con.close()

	
def addButtonCallBack():
	#	msgbox.showinfo("Info", "Nothing has been added yet.")
	add = tkinter.Tk()
	var = tkinter.IntVar(add)
	w = 300 # width for the Tk root
	h = 180 # height for the Tk root
	ws = add.winfo_screenwidth() # width of the screen
	hs = add.winfo_screenheight() # height of the screen
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2) - 100
	add.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	upperFrame = tkinter.Frame(add)
	lowerFrame = tkinter.Frame(add)
	upperFrame.pack()
	lowerFrame.pack(side=tkinter.BOTTOM)
	R1 = tkinter.Radiobutton(upperFrame, text="Normal Service", variable=var, value=1) 
	R1.pack()
	R2 = tkinter.Radiobutton(upperFrame, text="Repair", variable=var, value=2)
	R2.pack()
	R3 = tkinter.Radiobutton(upperFrame, text="Note", variable=var, value=3)
	R3.pack()
	L1 = tkinter.Label(lowerFrame, text="Operation")
	L2 = tkinter.Label(lowerFrame, text="Mileage (km)")
	L3 = tkinter.Label(lowerFrame, text="Cost (€)")
	L4 = tkinter.Label(lowerFrame, text="Done by")
	E1 = tkinter.Entry(lowerFrame)
	E2 = tkinter.Entry(lowerFrame)
	E3 = tkinter.Entry(lowerFrame)
	E4 = tkinter.Entry(lowerFrame)
	L1.grid(column=0, row=0);
	L2.grid(column=0, row=1);
	L3.grid(column=0, row=2);
	L4.grid(column=0, row=3);
	E1.grid(column=1, row=0);
	E2.grid(column=1, row=1);
	E3.grid(column=1, row=2);
	E4.grid(column=1, row=3);
	saveButton = tkinter.Button(lowerFrame, text ="Save", command=lambda: saveButtonCallBack(E1, E2, E3, E4, var))
	saveButton.grid(column=0, row=4)
	
	
def getButtonCallBack():
	con = lite.connect('test.db')
	print("Connected to db")
	cur = con.cursor()
	data = ""
	tables = ["Service", "Repair", "Note"]
	data = [[],[],[]]
	for i in range(3):
		cur.execute("SELECT * FROM " + tables[i] + " ORDER BY Mileage;")
		data[i] = cur.fetchall()
	print("Executed select")
	print(data)
	con.close()
	resultStr = "Services:\n"
	for tuple in data[0]:
		resultStr += str(tuple)
		resultStr += "\n"
	resultStr += "Repairs:\n"
	for tuple in data[1]:
		resultStr += str(tuple)
		resultStr += "\n"
	resultStr += "Notes:\n"
	for tuple in data[2]:
		resultStr += str(tuple)
		resultStr += "\n"
		
	msgbox.showinfo("Service history",resultStr)
	
addButton = tkinter.Button(top, text ="Add information", command = addButtonCallBack)
getButton = tkinter.Button(top, text ="Get information", command = getButtonCallBack)

addButton.pack()
getButton.pack()
top.mainloop()
