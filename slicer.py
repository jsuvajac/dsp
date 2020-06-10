from wav import *
from gui import *

import sys
import os


def main(argc, argv):
    files = []
    wave_slices = []
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
    
    gui = Window()

    for file in files:
        try:
            f = open(file,"r")
        except FileNotFoundError:
            print(f'file "{file}" does not exist!')
        else:
            f.close()
            slice = Wav(file)
            slice.read()
            wave_slices.append(slice)
            #gui.add_slice(slice)
    gui.add_slice(wave_slices[0])
    gui.display_files(files)
    gui.plot()
    gui.run()
    

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)