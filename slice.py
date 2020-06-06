from __future__ import annotations

import simpleaudio as sa # TODO: replace with pyaudio
import numpy as np
import wave
import struct

class Slice:
    def __init__(self, file: str):
        self.path = file
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

    def repeat(self, repeats: int = 1):
        out_list = []
        for i in range(repeats):
            for x in range(len(self.samples)):
                out_list.append(self.samples[x])
        self.samples = out_list

    def update_speed(self, speed: float = 1):
        out_list = []
        if speed == 0:
            return
        # write
        if speed >= 1:
            out_list = [self.samples[i] for i in range(len(self.samples)) if i % speed == 0]
        elif speed <= -1:
            out_list = [self.samples[-i] for i in range(len(self.samples)) if i % speed == 0]
        # slowdown
        elif speed < 1 and speed > 0:
            out_list = [self.samples[i] for i in range(len(self.samples)) for x in range(int(1/speed))]
        elif speed > -1 and speed < 0:
            out_list = [self.samples[-i] for i in range(len(self.samples)) for x in range(-int(1/speed))]
            
        self.samples = out_list
        
    def write_slice(self, out_name: str, start: int, end: int):
        out = wave.open(out_name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(44100.0)

        for i in range(start, end):
            out.writeframesraw(struct.pack("<h", self.samples[i]))

    #TODO: fix playback after speed or repeat change
    def play(self, start=0, end=-1):
        play_obj = sa.play_buffer(self.samples[start:end], 1, 2, 44100)
        #play_obj.wait_done()