import tkinter as tk

root = tk.Tk()
root.geometry('200x200')  # sets the size of the window to 200x200 pixels

# Create a frame that will hold the canvas and the scrollbar
frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

# Create a canvas that will act as a container
canvas = tk.Canvas(frame, width=200, height=200)
canvas.pack(side='left', fill='both', expand=True)

# Create a frame that will hold the widgets, and attach it to the canvas
widgets_frame = tk.Frame(canvas)
widgets_frame.pack()

# Create a scrollbar and attach it to the frame
scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)
canvas.create_window((0, 0), window=widgets_frame, anchor='nw')


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


canvas.bind('<Configure>', on_configure)


def add_canvas_elements(canvas_list):
    for canvas_element in canvas_list:
        canvas_element.pack()


colors = ["white", "red", "blue", "green", "purple", "gray"]
canvas_elements = [tk.Canvas(widgets_frame, bg=color, width=200, height=200) for color in colors]
add_canvas_elements(canvas_elements)

root.mainloop()
