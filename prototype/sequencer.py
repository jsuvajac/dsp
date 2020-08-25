import threading
import time
from math import gcd

from wav import *

# TODO: replace simple audio with pyaudio for better performance and concurrent sample playback

class Pattern:
    def __init__(self, wav, num_steps):
        self.wav = wav

        self.pattern = [1 for f in range(num_steps)]
        self.num_steps = num_steps
        # auto set length based on number of hits and sample length
        self.length = len(self.wav.samples)/44100.0 * num_steps
        #print(self.pattern, self.length, self.num_steps)

    # insert padding after each beat 
    def lengthen(self, factor):
        #print(self.pattern, factor)
        
        temp = []
        for i in self.pattern:
            temp.append(i)
            for j in range(factor-1):
                temp.append(0)
        self.pattern = temp
        self.num_steps = len(temp)


# polyrhythmicr sequencer
class Sequencer:
    def __init__(self):
        self.run = True

        self.sequence = [] # of patterns
        self.num_steps = 0
        self.step_size = 0
    
    def stop_sequencer(self):
        self.run = False

    def add_pattern(self, pattern):
        """
        if the sequencer contains a patter of 3 and a pattern of 4 beats is added:
            -> the sequencer will have 12 beats as that is the smalles length with factors 3 and 4

        if we add a pattern of 2 the sequence will not change as 2 is a factor of 12

        if we add a pattern of 9 the sequence will be 36 since that is the shortest sequence with factors 12 and 9
        """
        if self.sequence == []:
            self.step_size = pattern.length/pattern.num_steps
            self.num_steps = pattern.num_steps
            self.sequence.append(pattern)

        elif self.num_steps == pattern.num_steps:
            self.sequence.append(pattern)
            return

        else:
           
            gcd_val = gcd(self.num_steps,pattern.num_steps)

            #print(self.num_steps, pattern.num_steps)
            temp_num_steps = int(self.num_steps*pattern.num_steps/ gcd_val)

            for pat in self.sequence:
                pat.lengthen(int(temp_num_steps/self.num_steps))

            pattern.lengthen(int(temp_num_steps/pattern.num_steps))

            self.num_steps = temp_num_steps
            self.sequence.append(pattern)


    def on_play_pattern(self):
        t = threading.Thread(target=self.play, args=(self.sequence, ))
        t.start()

    def play(self, seq):
        index = 0
        while self.run:
            if index == 0:
                print()
            print(f"{index+1} ",end='', flush=True)

            start = time.time()

            for i, pat in enumerate(seq):
                if pat.pattern[index] == 1:
                    pat.wav.play()

            #print(index, end='')
            index += 1
            index %= self.num_steps

            #print(f" step: {self.step_size:.4f}", end='')

            end = time.time()

            delta = self.step_size -(end-start )
            if delta < 0:
                delta = 0
            #print(f" af-op: {delta:.4f}", end='')
        
            #print(f" sleep: {self.step_size+delta:.4f}", end='')
            time.sleep(self.step_size + delta)

            end = time.time()
            #print(f" del: {end-start:.4f}")

if __name__=="__main__":
    patterns = []

    print("Test: pass the god damn butter")
    patterns.append(Pattern(Wav("input/high.wav"), 3))
    patterns.append(Pattern(Wav("input/high.wav"), 4))
    patterns.append(Pattern(Wav("input/high.wav"), 9))
    #patterns.append(Pattern(Wav("input/mid.wav"), 5))
    #patterns.append(Pattern(Wav("input/low.wav"), 3))

    seq = Sequencer()

    for pat in patterns:
        seq.add_pattern(pat)
        print(f"beat count: {pat.num_steps} {len(pat.pattern)} patterns:")
        for p in seq.sequence:
            print(f"\t{p.pattern}")


    seq.step_size = 1/seq.num_steps

    try:
        seq.play(seq.sequence)
    except KeyboardInterrupt:
        seq.stop_sequencer()
