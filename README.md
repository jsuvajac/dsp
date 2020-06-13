# Slicer
Simple wave file slicer and sampler

### Run
```
python3 slicer.py -d
```

### Test
```
python3 wav.py
```

## Gui
* load in wave files
* plot amplitude and spectral graphs
* select file from file list
* play/stop

## Wav
* Read in a wav file into a non mutable buffer 'samples'
* Apply changes to the buffer
* Save the newly formed slice as a new wav file

### Sample modifying features

    reverse
    speed up
    slow down
    repeat
    reset to original
