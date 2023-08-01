import tkinter as tk
from tkinter import ttk
import random

# Create the main window
root = tk.Tk()
root.title("Scrollable List of Images")

# Create a scrollbar
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, height=4)

# Create a frame to hold the list of canvas elements
frame = ttk.Frame(root)
frame.pack()

# Create a list to hold the canvas elements
canvas_list = []


def create_random_image():
    # Generate a random 2D array of pixels
    width = 100
    height = 100
    pixels = [[random.randint(0, 255) for _ in range(width)] for _ in range(height)]
    return pixels


for i in range(7):
    # Create a canvas to display the image
    canvas = tk.Canvas(frame, width=100, height=100)
    canvas.grid(row=i, column=0)

    # Generate a random image
    pixels = create_random_image()

    # Draw the pixels on the canvas
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            color = "#%02x%02x%02x" % (pixel, pixel, pixel)
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=color)

    canvas_list.append(canvas)

# Configure the scrollbar to work with the frame
#frame.config(yscrollcommand=scrollbar.set)
#scrollbar.config(command=frame.yview)

root.mainloop()
