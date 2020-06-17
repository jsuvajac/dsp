import threading
import time

from wav import *


class Pattern:
    def __init__(self, wav, beat_count):
        self.wav = wav

        self.pattern = [1 for f in range(beat_count)]
        self.beat_count = beat_count
        # auto set length based on number of hits and sample length
        self.length = len(self.wav.samples)/44100.0 * beat_count
        #print(self.pattern, self.length, self.beat_count)
    def lengthen(self, factor):
        print(self.pattern, factor)
        temp = []
        for i in self.pattern:
            for j in range(factor-1):
                temp.append(0)
            temp.append(i)
        self.pattern = temp



class Sequencer:
    def __init__(self):
        self.run = True

        self.sequence = [] # of patterns
        self.num_steps = 0
        self.step_size = 0

    def stop_sequencer(self):
        self.run = False

    def add_pattern(self, pattern):
        if self.sequence == []:
            self.step_size = pattern.length/pattern.beat_count
            self.num_steps = pattern.beat_count
            self.sequence.append(pattern)

        elif self.num_steps == pattern.beat_count:
            self.sequence.append(pattern)
            return

        else:
            self.num_steps *= pattern.beat_count
            self.step_size = self.step_size/pattern.beat_count

            # TODO: fix with gcd
            for pat in self.sequence:
                pat.lengthen(pattern.beat_count)
                print(pat.pattern)
            pattern.lengthen(int(self.num_steps/pattern.beat_count))
            print(pattern.pattern)
            self.sequence.append(pattern)



    def on_play_pattern(self, sequence):
        t = threading.Thread(target=self.play_ntimes, args=(self.sequence, ), daemon=True)
        t.start()

    def play(self, seq):
        index = 0
        while self.run:
            start = time.time()
            for i, pat in enumerate(seq):
                if pat.pattern[index] == 1:
                    pat.wav.play()

            if index == 0:
                print()

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
    pat1 = Pattern(Wav("slice/slice_1.wav"), 2)
    #pat1.pattern = [0,0,1,0,1]

    pat2 = Pattern(Wav("slice/slice_1.wav"), 3)

    #pat3 = Pattern(Wav("slice/slice_3.wav"), 6)
    #pat3.pattern = [1,0,1,0,1,0]

    seq = Sequencer()
    seq.add_pattern(pat1)
    seq.add_pattern(pat2)
    seq.step_size = 0.25
    #seq.add_pattern(pat3)

    try:
        seq.play(seq.sequence)
    except KeyboardInterrupt:
        seq.stop_sequencer()
