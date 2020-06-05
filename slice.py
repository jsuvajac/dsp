from __future__ import annotations

import wave
import numpy as np
import matplotlib.pyplot as plt
import struct

class Slice:
    def __init__(self, file: str):
        self.file = wave.open(file, 'rb')
        self.samples = []
        # plot
        self.fig = None
        self.wav_plot = None
        self.spec_plot = None

    def read(self, num_samples: int = 0, offset: int = 0):
        if num_samples > self.file.getnframes():
            return
        # if samples not provided will read entire file
        if num_samples == 0:
            num_samples = self.file.getnframes()

        self.samples = np.frombuffer(
            self.file.readframes(num_samples),
            offset=offset,
            dtype=np.int16)

    def write(self, out_name: str, repeats: int = 1, speed: float = 1):
        if speed == 0:
            return
        out = wave.open(out_name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(44100.0)

        out_list = []

        # insert samples num_repeat times
        for i in range(repeats):
            for x in range(len(self.samples)):
                out_list.append(self.samples[x])

        # TODO: breakup into methods
        # write
        if speed >= 1:
            for i in range(len(out_list)):
                if i % speed == 0:
                    out.writeframesraw(struct.pack("<h", out_list[i]))
        elif speed <= -1:
            for i in range(len(out_list)):
                if i % speed == 0:
                    out.writeframesraw(struct.pack("<h", out_list[-i]))
        # slowdown
        elif speed < 1 and speed > 0:
            for i in range(len(out_list)): 
                for x in range(int(1/speed)):
                    out.writeframesraw(struct.pack("<h", out_list[i]))
        elif speed > -1 and speed < 0:
            for i in range(len(out_list)): 
                for x in range(-int(1/speed)):
                    out.writeframesraw(struct.pack("<h", out_list[-i]))
        
        out.close()
        return out_list

    def write_slice(self, out_name: str, start: int, end: int):
        out = wave.open(out_name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(44100.0)

        for i in range(start, end):
            out.writeframesraw(struct.pack("<h", self.samples[i]))

    #TODO: separate gui form slice
    #TODO: integrate with tkinter
    def plot(self):
        # wav
        self.fig = plt.figure(1)
        self.wav_plot = plt.subplot(211)
        self.wav_plot.plot(self.samples)
        self.wav_plot.set_ylabel('amplitude')

        #spectrograph
        self.spec_plot = plt.subplot(212)
        self.spec_plot.specgram(self.samples, Fs=self.file.getframerate(), NFFT=1024)
        self.spec_plot.set_xlabel('time')
        self.spec_plot.set_ylabel('frequency')
        #cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

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
            print("quit plot")

        plt.show()

    #TODO: implement slicing with event callback
    def onclick(self,event: Event):
        try:
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                'double' if event.dblclick else 'single', event.button,
                event.x, event.y, event.xdata, event.ydata)
            
        except Exception:
            # ignore clicks outside of plotts
            pass

    def setTitle(self, s: str):
        self.wav_plot.set_title(s, fontsize=16)
        plt.draw()