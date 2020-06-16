"""PyAudio Example: Play a wave file (callback version)"""

import pyaudio
import wave
import time
import sys

from wav import *
import numpy as np

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')
wav = Wav(sys.argv[1])

speeds = [10, -5, 0.25, -0.25]
for s in speeds:
    print(f"x {s}:")
    wav.apply_speed_change(s)
    #wav.play(wait=True)
reader = ReadHead(wav)



test_arr = np.array(wav.slice_samples)
location = 0


p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    #print(in_data, frame_count, time_info, status)
    #data = wf.readframes(frame_count)
    print(in_data)

    data = reader.readframes(frame_count)

    print(type(data))
    print(data)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
stream2 = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()


stream2.start_stream()

while stream.is_active() and stream2.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()