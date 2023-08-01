import tkinter as tk
import random
class CanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('200x200')  # sets the size of the window to 200x200 pixels

        # Create and configure the frame that holds the main canvas
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill='both')

        #Create the main canvas, set its size and add it to the frame
        self.canvas = tk.Canvas(self.frame,width=200,height=200)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Create the frame that holds the sub-canvases
        self.widgets_frame = tk.Frame(self.canvas)
        self.widgets_frame.pack()

        # Create the scrollbar, set its orientation and bind it to the main canvas
        self.scrollbar = tk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.widgets_frame, anchor='nw')

        # Bind the <Configure> event to the main canvas, so that the scroll region is updated when the canvas is resized
        self.canvas.bind('<Configure>', self.on_configure)

        # Create a list to store the sub-canvases
        self.canvas_elements = []

        # Create the button that adds new sub-canvases to the main canvas
        self.add_button = tk.Button(self.root, text="Add Canvas", command=self.random_add)
        self.add_button.pack()

        # The size of each suqare  in the sub-canvases
        self.pixelCanvasSize = 10

    def on_configure(self, event):
        """ Update the scrollredion of the main canvas whenever it is resized """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_canvas(self, active_buttons):
        """ Create a new sub-canvas with the given x-y coordinates for the black squares """
        width = max(j for i, j in active_buttons) + 1
        height = max(i for i, j in active_buttons) + 1

        canvas = tk.Canvas(self.widgets_frame, width= self.pixelCanvasSize * width, height= self.pixelCanvasSize * height)
        container = tk.Frame(canvas)
        for i, j in active_buttons:
            canvas.create_rectangle(self.pixelCanvasSize * j, self.pixelCanvasSize * i, self.pixelCanvasSize * (j + 1),
                                    self.pixelCanvasSize * (i + 1), fill="black")
        return canvas

    def random_add(self):
        """ Generate a new List of x-y coordinates, create a new sub-canvas with these coordinates, and add it to the main canvas """
        active_buttons = [(random.randint(0,4),random.randint(0,4)) for _ in range(5)]
        self.canvas_elements.append(self.create_canvas(active_buttons))
        self.add_canvas_elements(self.canvas_elements)
        self.update_scrollbar()

    def add_canvas_elements(self, canvas_list):
        """ Add all sub-canvases in the given list to the main canvas """
        for canvas_element in canvas_list:
            canvas_element.pack()

    def update_scrollbar(self):
        """ Update the scroll region of the main canvas """
        self.widgets_frame.update()
        self.on_configure(None)


root = tk.Tk()
app = CanvasApp(root)
root.mainloop()
