import tkinter as tk
import random


def create_canvas(active_buttons):
    # Calculate the size of the canvas
    width = max(j for i, j in active_buttons) + 1
    height = max(i for i, j in active_buttons) + 1

    # Create the canvas and draw the active buttons
    canvas = tk.Canvas(self.canvas_frame, width=50 * width, height=50 * height)
    container = tk.Frame(canvas)
    for i, j in active_buttons:
        canvas.create_rectangle(50 * j, 50 * i, 50 * (j + 1), 50 * (i + 1), fill="black")
    return canvas


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()
        self.canvas_elements = []
        self.create_buttons_window()

    def create_buttons_window(self):
        add_button = tk.Button(self.root, text="Add canvas", command=self.add_canvas)
        add_button.pack()

    def add_canvas(self):
        active_buttons = [(random.randint(0, 5), random.randint(0, 5)) for _ in range(10)]
        canvas = create_canvas(active_buttons)
        self.canvas_elements.append(canvas)
        self.show_canvas_elements()

    def show_canvas_elements(self):
        frame = tk.Frame(self.canvas_frame)
        frame.pack(expand=True, fill='both')
        canvas = tk.Canvas(frame)
        canvas.pack(side='left', fill='both', expand=True)
        widgets_frame = tk.Frame(canvas)
        widgets_frame.pack()
        for canvas_element in self.canvas_elements:
            canvas_element.pack()

        scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=widgets_frame, anchor='nw')

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind('<Configure>', on_configure)

