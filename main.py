import sys
import re
from tkinter import *
import mysql.connector
idnum = 0
results = []
#Database Credentials
db = mysql.connector.connect(
  host="epsilon1.duckdns.org",
  user="cosc457user",
  password="ERDSaresofun",
  database="cosc457"
)

class findStudentIDWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter a student ID number")
        self.l.pack()
        #self idnum refers to a text entry you can multiple ones inside a window.
        self.idnum=Entry(top)
        self.idnum.pack()
        #the command self.cleanup causes the window to close and performs some action prior to closing in this case it's writing our results to an array to print
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.idnum.get()
        print(self.value)
        global results
        cursor = db.cursor()
        #the execute on the cusror runs the MySQL command be careful not to forget parathanseeses where needed this will cause the query to fail.
        cursor.execute("SELECT first_name, last_name FROM issued_id WHERE id=\""+str(self.value)+"\" AND status='Student';")
        results = []
        for x in cursor:
            results.append(x)
        #appends results to end of array and destroys the window
        self.top.destroy()

class findNamesOfCoursesOfferedByProgram(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter an Program Name")
        self.l.pack()
        #self program refers to a text entry you can multiple ones inside a window.
        self.program=Entry(top)
        self.program.pack()
        #the command self.cleanup causes the window to close and performs some action prior to closing in this case it's writing our results to an array to print
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.program.get()
        print(self.value)
        global results
        cursor = db.cursor()
        #the execute on the cusror runs the MySQL command be careful not to forget parathanseeses where needed this will cause the query to fail.
        cursor.execute("SELECT first_name, last_name FROM issued_id WHERE id=\""+str(self.program.get())+"\" AND status='Student';")
        results = []
        for x in cursor:
            results.append(x)
        #appends results to end of array and destroys the window
        self.top.destroy()

class resultsWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Results of query")
        self.l.pack()
        global results
        #Calls global results and creates a list of labels inside of the results window.
        for result in results:
            self.l2=Label(top)
            self.l2.config(text=result)
            self.l2.pack()
            
class mainWindow(object):
    def __init__(self,master):
        self.master=master
        #Calls each button corresponds to a window to be opened.
        self.b=Button(master,text="Find Student by ID",command=self.findStudentIDWindow)
        self.b.pack()
        #A function inside of this has to be created along with an object for each associated window in the program
        self.b2=Button(master,text="Find names of courses offered by program",command=self.findNamesOfCoursesOfferedByProgram)
        self.b2.pack()

        self.r=Button(master,text="Print results",command=self.results)
        self.r.pack()

        self.master.winfo_toplevel().title("Baltimore City Community College CMS")

    def findStudentIDWindow(self):
        self.w=findStudentIDWindow(self.master)
        self.b["state"] = "disabled" 

        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"


    def findNamesOfCoursesOfferedByProgram(self):
        self.w=findNamesOfCoursesOfferedByProgram(self.master)
        self.b["state"] = "disabled" 

        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"

    def results(self):
        self.w=resultsWindow(self.master)
        self.r["state"] = "disabled" 

        self.master.wait_window(self.w.top)
        self.r["state"] = "normal"


    def entryValue(self):
        return self.w.value


if __name__ == "__main__":
    root=Tk()
    db.connect
    root.geometry("640x480")
    m=mainWindow(root)
    root.mainloop()