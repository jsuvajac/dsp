from __future__ import annotations

from wav import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.backend_bases import key_press_handler

import numpy as np

from tkinter import *
from tkinter import ttk

"""
    #TODO: implement a verticla threshold based slicing methode
    def run(self):
        if self.slice is None:
            return
        self.plot()
        i = 1
        try: 
            while True:
                #TODO: replace with event input as keypresses act as left click
                #TODO: handle only clicks on the correct graph or update both
                pts = np.asarray(plt.ginput(2, timeout=2))
                if len(pts) == 2:
                    x_pts = np.sort(pts[:,0])
                    self.setTitle("Press a key to save slice or mous button to skip")
                    self.wav_plot.axvline(x= int(x_pts[0]), color = 'r')
                    self.wav_plot.axvline(x= int(x_pts[1]), color = 'r')
                    #if plt.waitforbuttonpress():
                        #self.slice.write_slice(self.slice.path+"_slice_"+str(i)+".wav"
                            #,int(x_pts[0]), int(x_pts[1]))
                        #i += 1
                self.plot()
        except Exception:
            print(f"quit plot: {self.slice.path}")
"""


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("slicer")
        self.root.geometry('800x600') 
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        
        #TODO: imporve gui with frames
        self.fig = None
        self.canvas = None
        self.slice = None

    #def add_button(self):
        #self.slider = IntVar()
        #ttk.Label(self.pannel, textvariable=self.slider).grid(column=0, row=0, columnspan=5)
        #ttk.Scale(self.pannel, from_=0, to_=100, length=300,  variable=self.slider).grid(column=0, row=4, columnspan=5)
        #for child in self.pannel.winfo_children(): child.grid_configure(padx=5, pady=5)

    def add_slice(self, slice):
        self.slice = slice

    def plot(self):
        if self.fig is not None:
            self.fig.clf()
        # wav
        self.fig = plt.figure(1)
        self.wav_plot = plt.subplot(211)
        self.wav_plot.plot(self.slice.samples)
        self.wav_plot.set_ylabel('amplitude')

        self.setTitle("Select 2 cutting points")
        #spectrograph
        self.spec_plot = plt.subplot(212)
        self.spec_plot.specgram(self.slice.samples, Fs=self.slice.file.getframerate(), NFFT=1024)
        self.spec_plot.set_xlabel('time')
        self.spec_plot.set_ylabel('frequency')
   
    def gui_setup(self):
        self.plot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('key_press_event', self.on_key)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        button = ttk.Button(master=self.root, text="Quit", command=self.root.quit)
        button.pack(side=LEFT)


        self.play_button = ttk.Button(master=self.root, text="Play", command=self.slice.play)
        self.play_button.pack(side=TOP)
        self.stop_button = ttk.Button(master=self.root, text="Stop", command=self.slice.stop)
        self.stop_button.pack(side=TOP)


    def display_files(self,files):
        self.tree = ttk.Treeview(self.root)
        self.tree.bind("<Double-1>", self.on_file_select)
        self.tree.heading("#0",text="wav files",anchor=W)
        self.tree.pack(side=LEFT, fill=BOTH, expand=1)

        for f in files:
            self.tree.insert("", 0, text=f)

    def run(self):
        self.root.mainloop()

    def setTitle(self, s: str):
        self.wav_plot.set_title(s, fontsize=16)
        plt.suptitle(self.slice.path)
        plt.draw()

    def on_file_select(self, event: Event):
        item = self.tree.selection()[0]
        file_path = self.tree.item(item,"text")
        print("you clicked on", file_path)
        self.add_slice(Wav(file_path))
        self.plot()
        self.play_button['command'] = self.slice.play
        self.stop_button['command'] = self.slice.stop
        #print(self.play_button['command'])

    def on_key(self, event: Event):
        key_press_handler(event, self.canvas)
        print('you pressed', event.key, event.xdata, event.ydata)
        if event.key == "escape":
            self.root.quit()

    def on_click(self, event: Event):
        try:
            print(event)
            
        except Exception:
            # ignore clicks outside of plotts
            pass
