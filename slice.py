import wave
import struct

def main():
    wav = Slice('input/piano.wav')
    wav.read(100000, 45000)
    wav.write('out.wav', repeats=30, speed=8)

class Slice:
    def __init__(self, file):
        self.file_name = file
        self.file = wave.open(file, 'rb')
        self.file_params = self.file.getparams()
        self.samples = []

    def read(self, num_samples, offset=0):
        if num_samples > self.file.getnframes():
            return
        if offset > 0:
            frame = self.file.readframes(offset)
        frame = self.file.readframes(num_samples)
        self.samples = struct.unpack(f"<{str(num_samples)}h", frame)
        self.file.rewind()

    def write(self, out_name, repeats=1, speed=1):
        out = wave.open(out_name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(44100.0)

        out_list = []

        # insert samples num_repeat times
        for i in range(repeats):
            for x in range(len(self.samples)):
                out_list.append(self.samples[x])

        # write
        if speed >= 1:
            for i in range(len(out_list)):
                if i % speed == 0:
                    out.writeframesraw(struct.pack("<h", out_list[i]))

        elif speed < 1 and speed > 0:
            for i in out_list: 
                for x in range(int(1/speed)):
                    out.writeframesraw(struct.pack("<h", i))
        
        out.close()
        

if __name__ == "__main__":
    main()