from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Playing with Scales")

mainframe = ttk.Frame(root, padding="24 24 24 24")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

slider = IntVar()

ttk.Label(mainframe, textvariable=slider).grid(column=1, row=0, columnspan=5)
ttk.Scale(mainframe, from_=0, to_=100, length=300,  variable=slider).grid(column=1, row=4, columnspan=5)

ttk.Label(mainframe, textvariable=slider).grid(column=2, row=10, columnspan=5)
ttk.Scale(mainframe, from_=0, to_=100, length=300,  variable=slider).grid(column=1, row=14, columnspan=5)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


root.mainloop()
#
#class Window:
#    def __init__(self):
#        self.root = Tk()
#        self.pannel = ttk.Frame(self.root, padding="20 20 20 20")
#        self.pannel.grid(column=0, row=0, sticky=(N, W, E, S))