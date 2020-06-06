from slice import Slice
from gui import Gui

import sys
import os

# example: 
# ls input | awk '$0="input/"$0' | python3 slicer.py

def main(argc, argv):
    files = []
    wav_dir = 'input'
    #TODO: more robust argparsing
    if argc == 1: # pipe support
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

    elif argc == 2 and argv[1] == '-d': # directory
        for _, _, f in os.walk(wav_dir):
            files = f
            break
        for i in range(len(files)):
            files[i] = wav_dir +'/'+ files[i]

    elif argc == 2 and argv[1] == '-t': # testing
        files.append('input/piano.wav')

    elif argc == 2: # single file
        files.append(argv[1])
    
    gui = Gui()

    for file in files:
        slice = Slice(file)
        slice.read()
        gui.add_slice(slice)

    gui.run()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)