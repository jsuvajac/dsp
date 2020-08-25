from __future__ import annotations

import simpleaudio as sa # TODO: replace with pyaudio
import numpy as np
import wave
import struct

# TODO: fade-in/ fade-out
# TODO: filters

class ReadHead:
    def __init__(self, wav):
        self.wav = wav
        self.index = 0
    def readframes(self, size):
        chunk = self.wav.slice_samples[self.index:self.index + size]
        self.index += size
        return np.array(chunk)

class Wav:
    def __init__(self, file: str):
        self.path = file
        self.file = wave.open(file, 'rb')

        self.samples = [] # non mutable buffer read from file
        self.slice_samples = [] # mutable file to be updated by repeat and speed_change

        self.play_object = None # simpleaudio's buffer player
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

        self.reset_buffer()

    def reset_buffer(self):
        self.slice_samples = self.samples.copy()

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
        elif speed >= 1: # speedup
            out_list = [self.slice_samples[i] for i in range(len(self.slice_samples)) if i % speed == 0]
        elif speed <= -1: # speedup and reverse
            out_list = [self.slice_samples[-i] for i in range(len(self.slice_samples)) if i % speed == 0]
        elif speed < 1 and speed > 0: # slowdown
            out_list = [self.slice_samples[i] for i in range(len(self.slice_samples)) for x in range(int(1/speed))]
        elif speed > -1 and speed < 0: # slowdown and reverse
            out_list = [self.slice_samples[-i] for i in range(len(self.slice_samples)) for x in range(-int(1/speed))]
            
        self.slice_samples = out_list

    def apply_slice(self, start: int, end: int):
        print(start, end)
        if start == end:
            return

        print(len(self.slice_samples))

        if end < start:
            self.slice_samples = self.slice_samples[end:start]
        else:
            self.slice_samples = self.slice_samples[start:end]
        print(len(self.slice_samples))

    def write_slice(self, out_name: str, start: int = 0, end: int = -1):
        end = len(self.slice_samples)
        out = wave.open(out_name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(44100.0)

        for i in range(start, end):
            out.writeframesraw(struct.pack("<h", self.slice_samples[i]))

    def play(self, start=0, end=-1, wait=False):
        self.play_object = sa.play_buffer(np.array(self.slice_samples[start:end]), 1, 2, 44100)
        if wait:
            self.play_object.wait_done()

    def stop(self):
        sa.stop_all()

if __name__ == "__main__":
    wav = Wav("input/piano.wav")

    # test 1
    speeds = [10, -5, 0.25, -0.25, -15, -0.5]
    for s in speeds:
        print(f"x {s}:")
        wav.apply_speed_change(s)
        wav.play(wait=True)

    wav.apply_repeat(2)
    print(f"after 2 repeats:")
    wav.play(wait=True)

    print()
    wav.reset_buffer()


    # test 2
    print("speed up and slow down by the same factor -> distorsion")
    wav.apply_speed_change(22) # speed up for the sake of time
    factor = 5
    repeat = 4

    for s in range(repeat):
        wav.apply_speed_change(1/factor)
        print(f"x {s} len: {len(wav.slice_samples)}")
        wav.play(wait=True)

        wav.apply_speed_change(factor)
        print(f"x {s} len: {len(wav.slice_samples)}")
        wav.play(wait=True)
        print()