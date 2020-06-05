from slice import Slice
from gui import Gui

import sys

# example: 
# ls input | awk '$0="input/"$0' | python3 slicer.py

def main(argc, argv):
    files = []
    #TODO: more robust argparsing
    if argc == 1:
        while True:
            try:
                filename = input()
            except EOFError:
                break
            if filename == "":
                break
            files.append(filename)
    elif argc == 2 and (argv[1] == '-h' or argv[1] == '--help'): 
        print("Usage: slicer.py [FILE]")
        exit(0)
    #TODO: replace with -d directory searching command
    elif argc == 2 and argv[1] == '-m': 
        files.append('input/piano.wav')
        files.append('input/reverse_piano.wav')

    elif argc == 2:
        files.append(argv[1])
    
    gui = Gui()

    for file in files:
        print(filename)
        slice = Slice(file)
        slice.read()
        gui.add_slice(slice)

    gui.run()

    #wav.write('out.wav', repeats=1, speed=-1/2)
if __name__ == "__main__":
    main(len(sys.argv), sys.argv)