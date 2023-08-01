import tkinter as tk
import random
import time
import os

DEFAULT_BENCHMARK_FOLDER = "benchmark"

class App:
    def __init__(self, root):
        self.root = root
        root.title("Playfield")
        # Create width label
        self.width_label = tk.Label(text="Playfield Width:")
        # Create an input field
        self.content_width_entry = tk.StringVar()
        self.width_entry = tk.Entry(textvariable=self.content_width_entry, validate="key")
        self.width_entry.config(validatecommand=(self.width_entry.register(lambda x: x.isdigit()), "%P"))
        #self.width_entry = tk.Entry()
        # Create height label
        self.height_label = tk.Label(text="Playfield Height:")
        # Create an input field
        self.content_height_entry = tk.StringVar()
        self.height_entry = tk.Entry(textvariable=self.content_height_entry, validate="key")
        self.height_entry.config(validatecommand=(self.height_entry.register(lambda x: x.isdigit()), "%P"))
        #self.height_entry = tk.Entry()
        # Create submit button
        self.submit_button = tk.Button(text="Submit", command=self.actionButton)

        # Layout
        self.width_label.pack()
        self.width_entry.pack()
        self.height_label.pack()
        self.height_entry.pack()
        self.submit_button.pack()

        # The size of each suqare  in the sub-canvases
        self.pixelCanvasSize = 10
        self.all_active_buttons = []
        self.all_playstone_name = []
        self.all_playstone_amount = []
        self.list_of_all_active_buttons = []
        self.playfieldHeight = 0
        self.playfieldWidth = 0

    def init_Canvas(self):
        # Create a new window for the grid of buttons
        self.canvas_window = tk.Toplevel()
        self.canvas_window.title("Canvas")
        self.canvas_window.geometry('300x300') # sets the size of the window to 200x200 pixels

        # Create and configure the frame that holds the main canvas
        self.frame = tk.Frame(self.canvas_window)
        self.frame.pack(expand=True, fill='both')

        # Create the main canvas, set its size and add it to the frame
        self.canvas = tk.Canvas(self.frame, width=200, height=200)
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
        #self.add_button = tk.Button(self.canvas_window, text="Add Canvas", command=self.random_add)
        #self.add_button.pack()

    def on_configure(self, event):
        """ Update the scrollredion of the main canvas whenever it is resized """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_canvas(self, active_buttons):
        """ Create a new sub-canvas with the given x-y coordinates for the black squares """
        #width = max(j for i, j in active_buttons) + 1
        height = max(j for i, j in active_buttons) + 1
        #height = max(i for i, j in active_buttons) + 1
        width = max(i for i, j in active_buttons) + 1

        canvas = tk.Canvas(self.widgets_frame,
                           width= self.pixelCanvasSize * width,
                           height= self.pixelCanvasSize * height)
        container = tk.Frame(canvas)
        for j, i in active_buttons:
            canvas.create_rectangle(self.pixelCanvasSize * j,
                                    self.pixelCanvasSize * i,
                                    self.pixelCanvasSize * (j + 1),
                                    self.pixelCanvasSize * (i + 1), fill="black")
        return canvas

    def show_new_canvas(self):
        print(self.all_active_buttons)
        self.canvas_elements.append(self.create_canvas(self.all_active_buttons))
        self.add_canvas_elements(self.canvas_elements)
        self.update_scrollbar()

    def random_add(self):
        """ Generate a new List of x-y coordinates, create a new sub-canvas with these coordinates, and add it to the main canvas """
        active_buttons = [(random.randint(0,4),random.randint(0,4)) for _ in range(5)]
        print(active_buttons)
        active_buttons = self.all_active_buttons
        self.canvas_elements.append(self.create_canvas(active_buttons))
        #self.canvas_elements.append(self.create_canvas(self.all_active_buttons))
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

    def create_grid(self):
        # Get the values from the fields
        self.playfieldWidth = int(self.width_entry.get())
        self.playfieldHeight = int(self.height_entry.get())

        # Create a new window for the grid of buttons
        self.grid_window = tk.Toplevel()
        self.grid_window.title("Grid")

        # Create the grid of buttons
        self.grid_buttons = []
        for i in range(self.playfieldHeight):
            row = []
            for j in range(self.playfieldWidth):
                button = tk.Button(self.grid_window, text=f"{j},{i}", command=lambda i=i, j=j: self.button_clicked(j, i))
                button.grid(row=i, column=j, sticky=tk.W+tk.E)
                row.append(button)
            self.grid_buttons.append(row)

        # Create a text label
        self.label2 = tk.Label(self.grid_window, text="Playstone Name:")
        self.label2.grid(row=self.playfieldHeight, column=0, columnspan=self.playfieldWidth, sticky=tk.W + tk.E)

        # Create an input field
        self.input_field2 = tk.Entry(self.grid_window)
        self.input_field2.grid(row=self.playfieldHeight + 1, column=0, columnspan=self.playfieldWidth,
                               sticky=tk.W + tk.E)

        # Create a text label
        self.label = tk.Label(self.grid_window, text="How often is the playstone present?")
        self.label.grid(row=self.playfieldHeight + 2, column=0, columnspan=self.playfieldWidth, sticky=tk.W+tk.E)

        # Create an input field
        self.input_field = tk.Entry(self.grid_window)
        self.input_field.grid(row=self.playfieldHeight + 3, column=0, columnspan=self.playfieldWidth, sticky=tk.W+tk.E)

        # Create the submit button for printing the list of active buttons
        self.list_button = tk.Button(self.grid_window, text="Add Playstone", command=self.list_active_buttons)
        self.list_button.grid(row=self.playfieldHeight+4, column=0, columnspan=self.playfieldWidth, sticky=tk.W+tk.E)

        # Create a text label
        self.label3 = tk.Label(self.grid_window, text="")
        self.label3.grid(row=self.playfieldHeight + 5, column=0, columnspan=self.playfieldWidth, sticky=tk.W + tk.E)

        # Create a text label
        self.label4 = tk.Label(self.grid_window, text="")
        self.label4.grid(row=self.playfieldHeight + 6, column=0, columnspan=self.playfieldWidth, sticky=tk.W + tk.E)

        # Create the submit button for printing the list of active buttons
        self.list_button = tk.Button(self.grid_window, text="Save All in Text File", command=self.create_text_from_data)
        self.list_button.grid(row=self.playfieldHeight + 7, column=0, columnspan=self.playfieldWidth,
                              sticky=tk.W + tk.E)

    def on_check(self):
        state = self.check.get()
        if state == 1:
            print("Checkbox aktiv")
        else:
            print("Checkbox nicht aktiv")

    def button_clicked(self, i, j):
        """
        This function will change the button relief between raised and sunken when it's clicked
        and print the coordinates of the button that was clicked.
        """
        button = self.grid_buttons[j][i]
        if button["relief"] == tk.SUNKEN:
            button.config(relief=tk.RAISED)
        else:
            button.config(relief=tk.SUNKEN)
            # Print the coordinates of the button that was clicked
            print(f"Button at position {i},{j} was clicked")

    def reset_field(self):
        # Reset all buttons and the input field
        for row in self.grid_buttons:
            for button in row:
                button.config(relief=tk.RAISED)
        self.input_field.delete(0, 'end')
        self.input_field2.delete(0, 'end')

    def list_active_buttons(self):
        """
        This function will print the value from the input field and the coordinates
        of the active buttons (i.e buttons with relief = SUNKEN) and then reset all buttons
        """
        # Print the value from the input field
        value = self.input_field.get()
        print(f"Input field value: {value}")

        active_buttons = []
        for i, row in enumerate(self.grid_buttons):
            for j, button in enumerate(row):
                if button["relief"] == tk.SUNKEN:
                    active_buttons.append((j, i))
        print(f"Active buttons: {active_buttons}")

        if active_buttons == [] or \
                self.input_field.get() == "" or \
                self.input_field2.get() == "" or \
                not self.input_field.get().isdigit():

            if not self.input_field.get().isdigit():
                self.label3.config(text="Wrong input for the amount")
            else:
                self.label3.config(text="Wrong Input nothing was added")

            self.label4.config(text="Please enter again")
            self.reset_field()
            return

        self.all_active_buttons = active_buttons
        self.shiftArrayElements()

        self.label3.config(text="  Name for last Stone: " + str(self.input_field2.get()))
        self.label4.config(text="Amount for last Stone: " + str(self.input_field.get()))

        self.all_playstone_amount.append(int(self.input_field.get()))
        self.all_playstone_name.append(str(self.input_field2.get()))
        self.list_of_all_active_buttons.append(self.all_active_buttons)

        self.show_new_canvas()

        self.reset_field()

    def shiftArrayElements(self):
        shiftX = 1000000
        shiftY = 1000000

        for index in range(len(self.all_active_buttons)):
            element = self.all_active_buttons[index]
            shiftX = min(shiftX, element[0])
            shiftY = min(shiftY, element[1])
        print("shiftX = ", shiftX, "shiftY = ", shiftY)

        for index in range(len(self.all_active_buttons)):
            element = list(self.all_active_buttons[index])
            element[0] -= shiftX
            element[1] -= shiftY
            self.all_active_buttons[index] = tuple(element)

    def actionButton(self):
        self.submit_button.config(state="disable")
        self.create_grid()
        self.init_Canvas()

    def to_Text(self, string1, string2):
        return str(string1) + " " + str(string2) + "\n"

    def array_to_Text(self, array):
        result: str
        result = ""

        for y in range(len(array)):
            for x in range(len(array[y])):
                result += array[y][x]
            result+= "\n"

        return result

    def create_text_file_head(self):
        result: str

        result = "p pack\n"
        result += self.to_Text(self.playfieldWidth, self.playfieldHeight)

        return result

    def create_text_playstone(self, index):
        result: str

        result = self.to_Text(str(self.all_playstone_amount[index]), str(self.all_playstone_name[index]))

        maxY = -1
        maxX = -1

        for element in self.list_of_all_active_buttons[index]:
            maxX = max(maxX, element[0])
            maxY = max(maxY, element[1])


        tempString = ""
        array = []
        for y in range(maxY+1):
            tempArray = []
            for x in range(maxX+1):
                tempArray.append(".")
                tempString += "."
            array.append(tempArray)
            print(tempString)
            tempString = ""

        array_active_buttons = self.list_of_all_active_buttons[index]
        for element in array_active_buttons:
            print("element[0]", element[0])
            print("element[1]", element[1])
            array[element[1]][element[0]] = "#"

        result += self.array_to_Text(array)
        result += "%%%\n"

        return result

    def save_text_in_file(self, resultString):
        '''Check if directory exists, if not, create it'''
        check_folder = os.path.isdir(DEFAULT_BENCHMARK_FOLDER)

        # If folder doesn't exists, then create it
        if not check_folder:
            os.makedirs(DEFAULT_BENCHMARK_FOLDER)
            print("created folder : ", DEFAULT_BENCHMARK_FOLDER)
        else:
            print(DEFAULT_BENCHMARK_FOLDER, "folder already exists.")

        foldername = DEFAULT_BENCHMARK_FOLDER + "/"
        fileName = "benchmark"
        fileEnding = ".txt"
        lt = time.localtime()
        jahr, monat, tag, stunde, minute = lt[0:5]
        date = f"{tag:02d}-{monat:02d}-{jahr:4d}--{stunde:02d}-{minute:02d}"

        fileName = foldername+fileName+date+fileEnding

        with open(fileName, "w") as file:
            file.write(resultString)

    def create_text_from_data(self):
        print("create_text_from_data")
        print(self.all_playstone_name)
        print(self.all_playstone_amount)
        print(self.list_of_all_active_buttons)

        resultString = self.create_text_file_head()
        for index in range(len(self.list_of_all_active_buttons)):
            resultString += self.create_text_playstone(index)

        self.save_text_in_file(resultString)

        print(resultString)

        self.label3.config(text="All stones saved in the file")
        self.label4.config(text="   Windows can be closed")


root = tk.Tk()
app = App(root)
root.mainloop()
