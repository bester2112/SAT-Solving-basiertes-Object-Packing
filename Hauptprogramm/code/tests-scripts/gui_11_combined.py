import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.width_label = tk.Label(text="Width:")
        self.width_entry = tk.Entry()
        self.height_label = tk.Label(text="Height:")
        self.height_entry = tk.Entry()
        self.submit_button = tk.Button(text="Submit", command=self.create_grid)

        # Layout
        self.width_label.pack()
        self.width_entry.pack()
        self.height_label.pack()
        self.height_entry.pack()
        self.submit_button.pack()

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

        # Reset all buttons and the input field
        for row in self.grid_buttons:
            for button in row:
                button.config(relief=tk.RAISED)
        self.input_field.delete(0, 'end')





root = tk.Tk()
app = App(root)
root.mainloop()