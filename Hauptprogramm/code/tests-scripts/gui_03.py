import tkinter as tk

root = tk.Tk()

root.geometry("500x500")
root.title("My First GUI")

label = tk.Label(root, text="Hello World", font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10, pady=10)

myEntry = tk.Entry(root)
myEntry.pack(padx=10, pady=10)

button = tk.Button(root, text="Click me!", font=("Arial", 18))
button.pack(padx=10, pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

but1 = tk.Button(buttonframe, text="1", font=('Arial', 18))
but1.grid(row=0, column=0)


but2 = tk.Button(buttonframe, text="2", font=('Arial', 18))
but2.grid(row=0, column=1)

but3 = tk.Button(buttonframe, text="3", font=('Arial', 18))
but3.grid(row=0, column=2)

but4 = tk.Button(buttonframe, text="4", font=('Arial', 18))
but4.grid(row=1, column=0)

but5 = tk.Button(buttonframe, text="5", font=('Arial', 18))
but5.grid(row=1, column=1)

but6 = tk.Button(buttonframe, text="6", font=('Arial', 18))
but6.grid(row=1, column=2)

buttonframe.pack()

anotherbtn = tk.Button(root, text="Test")
anotherbtn.place(x=100, y=400, height=100, width=300)


root.mainloop()