from __future__ import annotations

from wav import *
import config as cfg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.backend_bases import key_press_handler

import numpy as np

from tkinter import *
from tkinter import ttk


class Window:
    def __init__(self, get_wave_list_func, get_wave_func, insert_wave_func):
        self.get_wave_list = get_wave_list_func
        self.get_wave = get_wave_func
        self.insert_wave = insert_wave_func

        self.root = Tk()
        self.root.title(cfg.title)
        self.root.geometry(cfg.resolution) 
        self.root.config(bg=cfg.col_bg)
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        # Style
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.style = ttk.Style()
        self.style.theme_use(self.style.theme_names()[-1])
        #print(ttk.Style().lookup("TFrame", "background"))
        self.style.configure('.',background=cfg.col_ttk_bg)
        #self.style.configure('.',foreground="#111100")
        self.style.configure('TButton',background=cfg.col_ttk_tbutton_bg)
    
        # horizontal bars
        self.top_frame = Frame(self.root, width=1200, height=20, padx=5, pady=5, bg=cfg.col_accent_1)
        self.top_frame.pack(side=TOP, fill=X)
 
        self.middle_frame = Frame(self.root, width=1200, height=200, padx=5, pady=5, bg=cfg.col_accent_2)
        self.middle_frame.pack(side=TOP, fill=BOTH)

        self.bottom_frame = Frame(self.root, width=1200, height=20, padx=5, pady=5, bg=cfg.col_accent_1)
        self.bottom_frame.pack(side=TOP, fill=X)
 
        # bottom tray
        self.bottom_tray = Frame(self.root, width=1200, height=100, padx=5, pady=5, bg=cfg.col_accent_1)
        self.bottom_tray.pack(side=BOTTOM, fill=BOTH)

        # vertical bars in the middle
        self.file_frame = ttk.Frame(self.middle_frame, width=50, height=400)
        self.file_frame.pack(side=LEFT, fill=Y)

        self.plot_frame = ttk.Frame(self.middle_frame, width=300, height=400)
        self.plot_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.widget_frame = ttk.Frame(self.middle_frame, width=50, height=400)
        self.widget_frame.pack(side=LEFT, fill=Y)

        # quit btn
        button = ttk.Button(master=self.bottom_tray, text="Quit", command=self.root.quit)
        button.pack(side=LEFT, expand=True)

        button = ttk.Button(master=self.bottom_tray, text="Spectral Plot", command=self.on_display_spectral)
        button.pack(side=LEFT, expand=True)

        button = ttk.Button(master=self.bottom_tray, text="Polar Plot", command=self.on_display_polar)
        button.pack(side=LEFT, expand=True)

        self.display_spectral = False

        self.fig = None
        self.canvas = None
        self.tree = None
        self.locators = []

        self.sample_buttons = []

        self.slice_count = 1
        self.display_files(self.get_wave_list())

        self.slice = self.get_wave("input/piano.wav")

        self.gui_setup()


    def plot(self):
        if self.fig is not None:
            self.fig.clf()
        # wav

        if not self.display_spectral:
            self.fig = plt.figure(1)
            self.wav_plot = plt.subplot(111)
            self.wav_plot.plot(self.slice.slice_samples)
            #self.wav_plot.set_ylabel('amplitude')
            self.wav_plot.axis('off')
            self.fig.set_facecolor(cfg.col_bg)
            self.setTitle("")
        #spectrograph
        else:
            self.fig = plt.figure(1)
            self.wav_plot = plt.subplot(211)
            self.wav_plot.plot(self.slice.slice_samples)
            #self.wav_plot.set_ylabel('amplitude')
            self.wav_plot.axis('off')
            self.fig.set_facecolor(cfg.col_bg)
            self.setTitle("")
 
            self.spec_plot = plt.subplot(212)
            self.spec_plot.specgram(self.slice.slice_samples, Fs=self.slice.file.getframerate(), NFFT=1024)
            #self.spec_plot.set_xlabel('time')
            #self.spec_plot.set_ylabel('frequency')
            self.spec_plot.axis('off')

        if self.canvas:
            self.canvas.draw()
        
   
    def gui_setup(self):
        self.plot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('key_press_event', self.on_key)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        #self.plot_toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame).pack(side=side, fill=X)
        #self.plot_toolbar.update()

        self.widget_panel_setup(self.widget_frame, TOP)

    def widget_panel_setup(self, master, side):
        ttk.Label(master, text="").pack(side=side, expand=True)

        self.play_button = ttk.Button(master=master, text="Play", command=self.slice.play)
        self.play_button.pack(side=TOP)


        self.stop_button = ttk.Button(master=master, text="Stop", command=self.slice.stop)
        self.stop_button.pack(side=TOP)

        self.display_separator(master, side)

        self.reverse_button = ttk.Button(master=master, text="Reverse", command=self.on_reverse_click)
        self.reverse_button.pack(side=TOP)

        self.display_separator(master, side)


        # speed
        self.speed_slider = IntVar()
        ttk.Label(master, textvariable=self.speed_slider).pack(side=side)
        ttk.Scale(master, from_=2, to_=10, length=300, command=lambda s:self.speed_slider.set(int(float((s))))).pack(side=side)
        self.speed_slider.set(2)

        self.speed_button = ttk.Button(master=master, text="speed up", command=self.on_speed_click)
        self.speed_button.pack(side=TOP)


        self.display_separator(master, side)


        # slow
        self.slow_slider = IntVar()
        ttk.Label(master, textvariable=self.slow_slider).pack(side=side)
        ttk.Scale(master, from_=2, to_=10, length=300, command=lambda s:self.slow_slider.set(int(float((s))))).pack(side=side)
        self.slow_slider.set(2)

        self.slow_button = ttk.Button(master=master, text="slow down", command=self.on_slow_click)
        self.slow_button.pack(side=TOP)


        self.display_separator(master, side)


        # repeats
        self.repeat_slider = IntVar()
        ttk.Label(master, textvariable=self.repeat_slider).pack(side=side)
        ttk.Scale(master, from_=2, to_=10, length=300, command=lambda s:self.repeat_slider.set(int(float((s))))).pack(side=side)
        self.repeat_slider.set(2)

        self.repeat_button = ttk.Button(master=master, text="repeat", command=self.on_repeat_click)
        self.repeat_button.pack(side=TOP)


        self.display_separator(master, side)


        self.slice_button = ttk.Button(master=master, text="Slice", command=self.on_slice_click)
        self.slice_button.pack(side=TOP)



        self.display_separator(master, side)


        self.reset_button = ttk.Button(master=master, text="Reset", command=self.slice.reset_buffer)
        self.reset_button.pack(side=TOP)

        ttk.Label(master, text="").pack(side=side, expand=True)

    def display_separator(self, master, side, empty=False, expand=True, orient=HORIZONTAL):
        ttk.Label(master, text="").pack(side=side, expand=True)
        if not empty:
            ttk.Separator(master, orient=orient).pack(side=side, fill=BOTH, expand=expand)
            ttk.Label(master, text="").pack(side=side, expand=True)

    def display_files(self,files):
        if not self.tree:
            self.tree = ttk.Treeview(self.file_frame)
            self.tree.bind("<Double-1>", self.on_file_select)
            self.tree.heading("#0",text="wav files",anchor=W)
            self.tree.pack(side=TOP, fill=BOTH, expand=True)

            self.display_separator(self.file_frame, TOP, expand=False)

            self.write_button = ttk.Button(master=self.file_frame, text="Write to file", command=self.on_write_slice_click)
            self.write_button.pack(side=TOP)

            self.display_separator(self.file_frame, TOP, empty=True)


        # clean
        for i in self.tree.get_children():
            self.tree.delete(i)
        # repopulate
        for f in files:
            self.tree.insert("", 0, text=f)

     

    def run(self):
        self.root.mainloop()

    def setTitle(self, s: str):
        self.wav_plot.set_title(self.slice.path, fontsize=16)
        plt.suptitle(s)
        plt.draw()





# EVENTS
# TODO: separate events from gui

    def on_file_select(self, event: Event):
        item = self.tree.selection()[0]
        file_path = self.tree.item(item,"text")
        print("you clicked on", file_path)
        self.slice = Wav(file_path)
        self.plot()
        self.canvas.draw()
        self.play_button['command'] = self.slice.play
        self.stop_button['command'] = self.slice.stop

    def on_key(self, event: Event):
        key_press_handler(event, self.canvas)
        print('you pressed', event.key, event.xdata, event.ydata)
        if event.key == "escape":
            self.root.quit()

    def on_click(self, event: Event):
        # left
        if event.button == 1 and type(event.xdata) is np.float64:
            # ignore clicks on spectral plot
            if self.display_spectral:
                if (self.fig.get_size_inches()*self.fig.dpi)[1]/2 > event.y:
                    return
            self.locators.append(int(event.xdata))
            if len(self.locators) > 2:
                self.locators.pop(0)
                self.fig.clf()
                self.plot()
            #print(self.locators)
            for x in self.locators:
                self.wav_plot.axvline(x=x, color = cfg.col_accent_2)
        # right
        elif type(event.xdata) is np.float64:
            self.locators.append(int(event.xdata))
            self.reset_plot()

        self.canvas.draw()

    def reset_plot(self):
        self.locators = []
        self.fig.clf()
        self.plot()

    def on_slice_click(self):
        print(self.locators)
        self.locators = np.sort(self.locators)
        if len(self.locators) == 2:
            if self.locators[0] < 0:
                self.locators[0] = 0
            self.slice.apply_slice(self.locators[0], self.locators[1])
        self.reset_plot()


    def on_speed_click(self):
        self.slice.apply_speed_change(self.speed_slider.get())
        self.reset_plot()

    def on_slow_click(self):
        factor = self.slow_slider.get()
        print(factor)
        self.slice.apply_speed_change(1/factor)
        self.reset_plot()

    def on_reverse_click(self):
        self.slice.apply_speed_change(-1)
        self.reset_plot()

    def on_repeat_click(self):
        self.slice.apply_repeat(self.repeat_slider.get())
        self.reset_plot()


    def on_write_slice_click(self):
        while True:
            path = cfg.dir_slice+"/"+"slice_"+ str(self.slice_count) + ".wav"
            if path in self.get_wave_list():
                print(path)
                self.slice_count += 1
            else:
                break
        
        self.slice.write_slice(path)
        self.insert_wave(path)

        self.slice.reset_buffer()

        self.display_files(self.get_wave_list())


        self.create_play_button(path)


    def create_play_button(self, path):
        # display a sample
        frame = ttk.Frame(self.bottom_frame, width=150, height=150, padding=50)
        frame.pack(side=LEFT)

        self.sample_buttons.append(frame)

        #fig = FigureCanvasTkAgg(self.fig, master=self.sample_buttons[-1])
        #fig.draw()
        #fig.pack(side=TOP, fill=BOTH)

        ttk.Button(master=self.sample_buttons[-1], text=path, command=lambda: self.get_wave(path).play()).pack(side=TOP)
        ttk.Separator(self.bottom_frame, orient=VERTICAL).pack(side=LEFT, fill=Y)

    def on_display_spectral(self):
        self.display_spectral = not self.display_spectral
        self.reset_plot()

    #TODO: fix multiple plots
    def on_display_polar(self):
        #self.plot()
        #self.fig2.clf()
        self.fig = plt.figure(1)
        self.polar_plot = plt.subplot(111, projection='polar')
        self.polar_plot.plot([1,1,1,1,1,1], "o")
        #self.wav_plot.set_ylabel('amplitude')
        #self.wav_plot.axis('off')
        #self.fig.set_facecolor(cfg.col_bg)
        #self.setTitle("")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_tray)
        #self.canvas.mpl_connect('button_press_event', self.on_click)
        #self.canvas.mpl_connect('key_press_event', self.on_key)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

