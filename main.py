from slice import Slice

def main():
    wav = Slice('input/piano.wav')
    wav.read()
    wav.plot()
    wav.write('out.wav', repeats=1, speed=-1/2)

    out = Slice('out.wav')
    out.read()
    out.plot()


if __name__ == "__main__":
    main()