import tkinter as tk
from tkinter import messagebox

def on_submit():
    print(var.get())
    messagebox.showinfo("Eingegebene Zahl", "die eingegebene Zahl ist: " + var.get())

def on_check():
    state = var2.get()
    if state == 1:
        print("Checkbox aktiv")
    else:
        print("Checkbox nicht aktiv")

root = tk.Tk()
root.title("Number Input")

var = tk.StringVar()

entry = tk.Entry(root, textvariable=var, validate="key")
entry.config(validatecommand=(entry.register(lambda x: x.isdigit()), "%P"))
entry.pack()

var2 = tk.IntVar()
check = tk.Checkbutton(root, variable=var2, command=on_check)
check.pack()

submit = tk.Button(root, text="Submit", command=on_submit)
submit.pack()

root.mainloop()