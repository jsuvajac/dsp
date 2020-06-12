from __future__ import annotations

import simpleaudio as sa # TODO: replace with pyaudio
import numpy as np
import wave
import struct

class Wav:
    def __init__(self, file: str):
        self.path = file
        self.file = wave.open(file, 'rb')

        self.samples = [] # non mutable buffer read from file
        self.slice_samples = [] # mutable file to be updated by repeat and speed_change

        self.play_object = None
        self.read()

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
        self.slice_samples = self.samples.copy()
        #print(self.samples)

    def apply_repeat(self, repeats: int = 1):
        out_list = []
        for i in range(repeats):
            for x in range(len(self.slice_samples)):
                out_list.append(self.slice_samples[x])
        self.slice_samples = out_list

    def apply_speed_change(self, speed: float = 1):
        out_list = []
        if speed == 0:
            return
        if speed >= 1: # speedup
            out_list = [self.slice_samples[i] for i in range(len(self.slice_samples)) if i % speed == 0]
        elif speed <= -1: # speedup and reverse
            out_list = [self.slice_samples[-i] for i in range(len(self.slice_samples)) if i % speed == 0]
        elif speed < 1 and speed > 0: # slowdown
            out_list = [self.slice_samples[i] for i in range(len(self.slice_samples)) for x in range(int(1/speed))]
        elif speed > -1 and speed < 0: # slowdown and reverse
            out_list = [self.slice_samples[-i] for i in range(len(self.slice_samples)) for x in range(-int(1/speed))]
            
        self.slice_samples = out_list
        
    def write_slice(self, out_name: str, start: int, end: int):
        out = wave.open(out_name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(44100.0)

        for i in range(start, end):
            out.writeframesraw(struct.pack("<h", self.slice_samples[i]))

    def play(self, start=0, end=-1):
        self.play_object = sa.play_buffer(self.slice_samples[start:end], 1, 2, 44100)
        #play_obj.wait_done()

    def stop(self):
        sa.stop_all()