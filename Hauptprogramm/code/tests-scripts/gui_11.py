import tkinter as tk
import tkinter.scrolledtext


class App:
    def __init__(self, master):
        self.master = master
        master.title("Grid")

        # Create a frame for the input fields and the submit button
        self.input_frame = tk.Frame(master)
        self.input_frame.pack()

        # Create the input fields and the submit button
        self.height_label = tk.Label(self.input_frame, text="Height:")
        self.height_label.pack(side=tk.LEFT)
        self.height_entry = tk.Entry(self.input_frame, width=5)
        self.height_entry.pack(side=tk.LEFT)
        self.width_label = tk.Label(self.input_frame, text="Width:")
        self.width_label.pack(side=tk.LEFT)
        self.width_entry = tk.Entry(self.input_frame, width=5)
        self.width_entry.pack(side=tk.LEFT)
        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.create_grid)
        self.submit_button.pack(side=tk.LEFT)

        # Create the canvas window and the scrollable area
        self.canvas_window = tk.Toplevel(master)
        self.canvas_window.title("Canvases")
        #self.canvas_area = tk.Canvas(self.canvas_window)
        #self.canvas_scroll = tk.Scrollbar(self.canvas_window, orient=tk.VERTICAL, command=self.canvas_area.yview)
        #self.canvas_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        #self.canvas_area.config(yscrollcommand=self.canvas_scroll.set)
        #self.canvas_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #self.canvas_area.pack_propagate(False)
        self.canvas_y = 0
        self.canvas_frame = None
        self.text_window = tk.Toplevel(master)
        self.text_window.title("Text")
        self.text_frame = None
        self.testCounter = 0
        self.canvas_elements = []


    def create_grid(self):
        # Get the values from the fields
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())

        # Create a new window for the grid of buttons
        self.grid_window = tk.Toplevel()
        self.grid_window.title("Grid")

        # Create the grid of buttons
        self.grid_buttons = []
        for i in range(height):
            row = []
            for j in range(width):
                button = tk.Button(self.grid_window, text=f"{i},{j}", command=lambda i=i, j=j: self.button_clicked(i, j))
                button.grid(row=i, column=j, sticky=tk.W+tk.E)
                row.append(button)
            self.grid_buttons.append(row)

        # Create a text label
        self.label = tk.Label(self.grid_window, text="HERE TEXT")
        self.label.grid(row=height, column=0, columnspan=width, sticky=tk.W+tk.E)

        # Create an input field
        self.input_field = tk.Entry(self.grid_window)
        self.input_field.grid(row=height + 1, column=0, columnspan=width, sticky=tk.W+tk.E)

        # Create the submit button for printing the list of active buttons
        self.list_button = tk.Button(self.grid_window, text="List Active Buttons", command=self.list_active_buttons)
        self.list_button.grid(row=height+2, column=0, columnspan=width, sticky=tk.W+tk.E)


        # Create the submit button for printing the input field value
       # self.submit_button.grid(row=height + 2, column=0)

    def button_clicked(self, i, j):
        button = self.grid_buttons[i][j]
        if button["relief"] == tk.SUNKEN:
            button.config(relief=tk.RAISED)
        else:
            button.config(relief=tk.SUNKEN)
            # Print the coordinates of the button that was clicked
            print(f"Button at position {i},{j} was clicked")

    def create_canvas(self, active_buttons):
        # Calculate the size of the canvas
        width = max(j for i, j in active_buttons) + 1
        height = max(i for i, j in active_buttons) + 1

        # Create the canvas and draw the active buttons
        canvas = tk.Canvas(self.canvas_frame, width=50 * width, height=50 * height)
        container = tk.Frame(canvas)
        for i, j in active_buttons:
            canvas.create_rectangle(50 * j, 50 * i, 50 * (j + 1), 50 * (i + 1), fill="black")
        #canvas.pack(side=tk.LEFT)
        return canvas

    def create_input_fields(self):
        # Create a text field for the amount and a text field for the name
        amount_label = tk.Label(self.canvas_frame, text="Amount:")
        amount_label.pack(side=tk.TOP)
        self.amount_entry = tk.Entry(self.canvas_frame)
        self.amount_entry.pack(side=tk.TOP)
        self.amount_entry.bind("<FocusOut>", self.validate_amount)
        name_label = tk.Label(self.canvas_frame, text="Name:")
        name_label.pack(side=tk.TOP)
        self.name_entry = tk.Entry(self.canvas_frame)
        self.name_entry.pack(side=tk.TOP)

    def create_save_button(self, active_buttons):
        # Create the save button
        self.save_button = tk.Button(self.canvas_frame, text="Save", command=self.save_values)
        self.save_button.pack(side=tk.TOP)

    def display_canvas2(self, active_buttons):
        # Create a new frame for the input fields and the button
        # Destroy the previous canvas frame if it exists
        #if hasattr(self, "canvas_frame"):
            # Destroy the previous canvas frame if it exists
        #    if self.canvas_frame is not None:
        #        self.canvas_frame.destroy()


        self.canvas_frame = tk.Frame(self.canvas_window)
        self.canvas_frame.pack()

        # Create a frame for the inner frame and the canvas
        outer_frame = tk.Frame(self.canvas_frame)
        outer_frame.pack(side=tk.LEFT)

        # Create a frame for the canvas and the input fields and save button
        inner_frame = tk.Frame(outer_frame)
        inner_frame.pack(side=tk.LEFT)

        # Create the canvas
        canvas = self.create_canvas(active_buttons)
        canvas.pack(side=tk.LEFT)

        # Create the input fields
        #self.create_input_fields()

        # Create the save button
        #self.create_save_button(active_buttons)

        # Add the frame to the canvas area and set the scroll region
        x1, y1, x2, y2 = canvas.bbox("all")
        #root.winfo_width() root.winfo_height()
        print(y2, y1)
        self.canvas_y += y2 - y1
        print(self.canvas_y)
        self.canvas_area.create_window((0, 0), window=self.canvas_frame, anchor=tk.NW)
        #self.canvas_area.create_window((0, self.canvas_y), window=self.canvas_frame, anchor=tk.NW)
        self.canvas_area.config(scrollregion=self.canvas_area.bbox("all"))

    def display_canvas(self, active_buttons):
        # Destroy the previous canvas frame if it exists
        #if hasattr(self, "canvas_frame"):
        # Destroy the previous canvas frame if it exists
        #    if self.canvas_frame is not None:
        #        self.canvas_frame.destroy()

        self.canvas_frame = tk.Frame(self.canvas_window)
        self.canvas_frame.pack(expand=True, fill='both')

        # Create a canvas that will act as a container
        self.canvas = tk.Canvas(self.canvas_frame, width=200, height=200)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Create a frame that will hold the widgets, and attach it to the canvas
        self.widgets_frame = tk.Frame(self.canvas)
        self.widgets_frame.pack()

        # Create a scrollbar and attach it to the frame
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.widgets_frame, anchor='nw')

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind('<Configure>', on_configure)

        # Add elements to the canvas
        #self.canvas_elements = [tk.Canvas(self.widgets_frame, bg="white", width=200, height=200) for _ in
        #                   range(len(active_buttons))]
        self.canvas_elements.append(self.create_canvas(active_buttons))
        for element in self.canvas_elements:
            element.pack()

    def validate_amount(self, event):
        # Validate the input in the amount field to allow only numbers
        if not str.isdigit(self.amount_entry.get()):
            self.amount_entry.delete(0, "end")

    def save_values(self):
        # Print the values from the amount and name fields
        amount = self.amount_entry.get()
        name = self.name_entry.get()
        print(f"Amount: {amount}, Name: {name}")

    def display_text(self):
        if hasattr(self, "text_frame"):
            # Destroy the previous canvas frame if it exists
            if self.text_frame is not None:
                self.text_frame.destroy()

        self.text_frame = tk.Frame(self.text_window)
        self.text_frame.pack()

        texField = tkinter.scrolledtext.ScrolledText(self.text_frame)
        texField.pack()

        if self.testCounter == 0:
            file = open("_file.txt")
            self.testCounter += 1
        else:
            file = open("../example.txt")
        line = file.readline()
        while line:
            print(line)
            texField.insert("end", line)
            line = file.readline()
        file.close()

    def list_active_buttons(self):
        # Print the value from the input field
        value = self.input_field.get()
        print(f"Input field value: {value}")

        active_buttons = []
        for i, row in enumerate(self.grid_buttons):
            for j, button in enumerate(row):
                if button["relief"] == tk.SUNKEN:
                    active_buttons.append((i, j))
        print(f"Active buttons: {active_buttons}")

        # Create a new window for the canvas if it doesn't exist, or use the existing one
        if not hasattr(self, "canvas_window"):
            self.canvas_window = tk.Toplevel()
            self.canvas_window.title("Canvas")
            self.canvas_y = 0
        self.display_canvas(active_buttons)

        # Create a new window for the text if it doesn't exist, or use the existing one
        if not hasattr(self, "text_window"):
            self.text_window = tk.Toplevel()
            self.text_window.title("Text")
        self.display_text()

        # Reset all buttons and the input field
        for row in self.grid_buttons:
            for button in row:
                button.config(relief=tk.RAISED)
        self.input_field.delete(0, 'end')


root = tk.Tk()
app = App(root)
root.mainloop()
