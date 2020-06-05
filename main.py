from slice import Slice
from gui import Gui

def main():
    gui = Gui()

    wav = Slice('input/piano.wav')
    wav.read()
    gui.add_slice(wav)

    out = Slice('input/reverse_piano.wav')
    out.read()
    gui.add_slice(out)
    #out.play()


    gui.run()
    #wav.play()

    #wav.write('out.wav', repeats=1, speed=-1/2)
if __name__ == "__main__":
    main()