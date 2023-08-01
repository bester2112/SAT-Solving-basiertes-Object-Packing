import tkinter as tk

# Create the main window
root = tk.Tk()

# Create the canvas widget
canvas = tk.Canvas(root, width=200, height=100)
canvas.pack()

# Create a rectangle on the canvas
new_rectangle = canvas.create_rectangle(25, 25, 150, 75, fill="blue")

# Create vertical lines on the canvas
canvas.create_line(50, 25, 50, 75)
canvas.create_line(100, 25, 100, 75)

# Create horizontal lines on the canvas
canvas.create_line(25, 50, 150, 50)
canvas.create_line(25, 75, 150, 75)

# Run the tkinter event loop
root.mainloop()
