from __future__ import annotations

from wav import *
from gui import *
import config as cfg

import sys
import os

class Slicer():
    def __init__(self):
        self.files = []
        self.dir_list = [cfg.dir_wave, cfg.dir_slice]
        self.dirs = {}

        self.wave_files = {}
        self.gui = None

    def parse_dirs(self):
        for folder in self.dir_list:
            for _, _, f in os.walk(folder):
                self.dirs[folder] = f
                for file in self.dirs[folder]:
                    self.files.append(folder +'/'+ file)

    def load_wave_files(self):
        bad_files = []
        for file in self.files:
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
                    self.wave_files[file] = slice

        self.files = list(set(self.files).symmetric_difference(set(bad_files)))
        #print(self.wave_files)

    def run(self):
        self.gui.run()

    def get_wave_list(self):
        return self.wave_files

    def get_wave(self, name: str) -> Wav:
        return self.wave_files[name]

    def insert_wave(self, name: str):
        self.files.append(name)
        self.wave_files[name] = Wav(name)

    def gui_setup(self):
        self.gui = Window(self.get_wave_list, self.get_wave,  self.insert_wave)
        for file in self.files:
            self.gui.create_play_button(file)



def main(argc, argv):
    app = Slicer()

    # default: read from 
    if argc == 1:
        app.parse_dirs()

    elif argc == 2 and (argv[1] == '-h' or argv[1] == '--help'): 
        print(f"Usage: {cfg.title}.py  --  opens wav files in the input dir by default")
        exit(0)

    elif argv[1] == '-d':
        if argc == 2:
            pass
        if argc > 2:
            app.dir_list.extend(dir_list=argv[2:])

        app.parse_dirs()
        #print(dirs)

    elif argc == 2: # single file
        app.files.append(argv[1])
    
    app.load_wave_files()
    app.gui_setup()
    app.run()
    

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)