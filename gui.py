from __future__ import annotations
from slice import Slice

import matplotlib.pyplot as plt
import numpy as np

#TODO: integrate with tkinter
class Gui:
    def __init__(self):
        self.slices = [] 
        self.slice = None
        self.slice_index = None

    def add_slice (self, slice: Slice):
        print(slice.path)
        self.slices.append(slice)
        if self.slice is None:
            self.slice = self.slices[0]
            self.slice_index = 0

    def plot(self):
        # wav
        self.fig = plt.figure(1)
        self.wav_plot = plt.subplot(211)
        self.wav_plot.plot(self.slice.samples)
        self.wav_plot.set_ylabel('amplitude')

        #spectrograph
        self.spec_plot = plt.subplot(212)
        self.spec_plot.specgram(self.slice.samples, Fs=self.slice.file.getframerate(), NFFT=1024)
        self.spec_plot.set_xlabel('time')
        self.spec_plot.set_ylabel('frequency')
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        cid = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        # TEMP: get 2 cutting points
        i = 1
        try: 
            while True:
                self.setTitle("Select 2 cutting points")
                pts = np.asarray(plt.ginput(2, timeout=-1))
                x_pts = np.sort(pts[:,0])
                self.setTitle("Press a key to save slice or mous button to skip")
                if plt.waitforbuttonpress():
                    self.write_slice("slice_"+str(i)+".wav",int(x_pts[0]), int(x_pts[1]))
                i += 1
        except Exception:
            print(f"quit plot: {self.slice.path}")

        plt.show()

    def updateSlice(self, slice: Slice):
        self.slice = slice

    def setTitle(self, s: str):
        self.wav_plot.set_title(s, fontsize=16)
        plt.draw()

    def on_key(self, event: Event):
        print('you pressed', event.key, event.xdata, event.ydata)
        if event.key == "right":
            self.slice_index += 1
            self.slice_index %= len(self.slices)
            self.slice = self.slices[self.slice_index]
            self.fig.clf()
            self.plot()
        if event.key == "left":
            self.slice_index -= 1
            self.slice_index %= len(self.slices)
            self.slice = self.slices[self.slice_index]
            self.fig.clf()
            self.plot()


    def onclick(self,event: Event):
        try:
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                'double' if event.dblclick else 'single', event.button,
                event.x, event.y, event.xdata, event.ydata)
            print(event)
            
        except Exception:
            # ignore clicks outside of plotts
            pass
