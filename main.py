from slice import Slice

def main():
    wav = Slice('input/piano.wav')
    wav.read()
    wav.plot()
    wav.play()
    #wav.write('out.wav', repeats=1, speed=-1/2)

    out = Slice('out.wav')
    out.read()
    out.plot()
    #out.play()

if __name__ == "__main__":
    main()