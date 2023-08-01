from tkinter import *

def update_bbox_size():
    # Calculate the bounding box coordinates
    x1, y1, x2, y2 = bounding_box.bbox(ALL)

    # Print the size of the bounding box
    print(f"Bounding box size: {x2-x1}x{y2-y1}")

# Create the root window
root = Tk()

# Create a canvas with a 50x50 pixel size
canvas = Canvas(root, width=50, height=50)

# Create a text field for the amount
amount_field = Entry(root)

# Create a text field for the name
name_field = Entry(root)

# Create a save button
save_button = Button(root, text="Save")

# Create a bounding box around all of the elements
bounding_box = Frame(root, bd=1, relief=SUNKEN)

# Add the canvas, text fields, and button to the bounding box
canvas.pack(side=LEFT)
amount_field.pack(side=LEFT)
name_field.pack(side=LEFT)
save_button.pack(side=LEFT)

# Add the bounding box to the root window
bounding_box.pack(side=LEFT)

# Update the layout to ensure that the widgets are displayed
root.update()
root.after(1000, update_bbox_size)
# Run the main loop
root.mainloop()

# Schedule the update_bbox_size function to be called every 1000 milliseconds

