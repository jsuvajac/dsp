from wav import *
from gui import *

import sys
import os


def main(argc, argv):
    files = []

    dir_list = ['input']
    dirs = {}

    wave_slices = []

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

    elif argv[1] == '-d': # directory
        if argc == 2:
            pass
        if argc > 2:
            for in_dir in argv[2:]:
                dir_list.append(in_dir)

        for folder in dir_list:
            for _, _, f in os.walk(folder):
                dirs[folder] = f
                for file in dirs[folder]:
                    files.append(folder +'/'+ file)

        #print(dirs)

    elif argc == 2 and argv[1] == '-t': # testing
        files.append('input/piano.wav')

    elif argc == 2: # single file
        files.append(argv[1])
    
    
    gui = Window()
    bad_files = []
    for file in files:
        try:
            f = open(file,"r")
        except FileNotFoundError:
            print(f'file "{file}" does not exist!')
            bad_files.append(file)
        else:
            f.close()
            try:
                slice = Wav(file)
            except Exception:
                print(f'cannot open file: {file}')
                bad_files.append(file)
            else:
                wave_slices.append(slice)

    files = list(set(files).symmetric_difference(set(bad_files)))
    gui.add_slice(wave_slices[0])
    gui.display_files(files)
    gui.gui_setup()
    gui.run()
    

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)