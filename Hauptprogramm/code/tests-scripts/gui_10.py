import tkinter as tk

def _mode():
    button.config(relief=tk.SUNKEN)


# Create the main window
window = tk.Tk()
window.title("Button Grid")

# Create a 10x10 grid of buttons
for i in range(10):
    for j in range(10):
        button = tk.Button(window, text="", width=1, height=1, bg="gray", activebackground="lightgray", relief=tk.SUNKEN
                           command = _mode)
        button.grid(row=i, column=j)

# Run the main loop
window.mainloop()
