import tkinter as tk
import openpyxl

email = ""

def runInterface():
    window = tk.Tk()
    greeting = tk.Label(text = "JoinThe.Mail", foreground = "white", background = "black")
    greeting.pack()

    button = tk.Button(text = "Click here", width = 25, height = 5, bg = "blue", fg = "yellow")
    button.pack() 

    label = tk.Label(text="Name")
    label.pack()
    entry = tk.Entry(fg="yellow", bg="blue", width=50)
    entry.pack()

    email = entry.get()

    label2 = tk.Label(text=email)
    label2.pack()
    
    window.mainloop()

runInterface()