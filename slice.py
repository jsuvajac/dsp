import wave
import numpy as np
import matplotlib.pyplot as plt
import struct

class Slice:
    def __init__(self, file):
        self.file_name = file
        self.file = wave.open(file, 'rb')
        self.file_params = self.file.getparams()
        self.samples = []

    def read(self, num_samples=0, offset=0):
        if num_samples > self.file.getnframes():
            return
        # if samples not provided will read entire file
        if num_samples == 0:
            num_samples = self.file.getnframes()

        self.samples = np.frombuffer(
            self.file.readframes(num_samples),
            offset=offset,
            dtype=np.int16)

    def write(self, out_name, repeats=1, speed=1):
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

    def plot(self):
        # wav
        plt.figure(1)
        plot_a = plt.subplot(211)
        plot_a.plot(self.samples)
        plot_a.set_ylabel('amplitude')

        #spectrograph
        plot_b = plt.subplot(212)
        plot_b.specgram(self.samples, Fs=self.file.getframerate())
        plot_b.set_xlabel('time')
        plot_b.set_ylabel('frequency')
        plt.show()
