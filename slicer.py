from wav import *
from gui import *

import sys
import os


def main(argc, argv):
    files = []

    dir_list = ['input', 'slice']
    dirs = {}

    wave_slices = []

    # default: read from 
    if argc == 1:
        for folder in dir_list:
            for _, _, f in os.walk(folder):
                dirs[folder] = f
                for file in dirs[folder]:
                    files.append(folder +'/'+ file)

    elif argc == 2 and (argv[1] == '-h' or argv[1] == '--help'): 
        print("Usage: slicer.py  --  opens wav files in the input dir by default")
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

    elif argc == 2: # single file
        files.append(argv[1])
    
    
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

    #TODO: create application state/ backend
    gui = Window(files)
    gui.display_files(files)
    gui.run()
    

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)