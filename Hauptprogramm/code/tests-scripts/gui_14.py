import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Scrollable List")

# Create a list of items to display in the listbox
cities = ["Hamburg", "Stuttgart","Berlin", "Dortmund", "Duisburg", "Potsdam", "Meschede"]

canvas_list = []

canvas1 = tk.Canvas(root, width=200, height=100)
canvas1.pack()

canvas_list.append(canvas1)

canvas2 = tk.Canvas(root, width=200, height=100, bg='white', bd=2)
canvas2.pack()

canvas_list.append(canvas2)

# Create a scrollbar
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox to display the items
listbox = tk.Listbox(root, height=4, yscrollcommand=scrollbar.set)
for city in canvas_list:
    listbox.insert(tk.END, city)
listbox.pack()

# Configure the scrollbar to work with the listbox
scrollbar.config(command=listbox.yview)

# Run the main loop
root.mainloop()
