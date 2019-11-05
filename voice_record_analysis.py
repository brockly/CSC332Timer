#!/usr/bin/env python3

import time
import threading
import pyloudness

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder
from aiy.voice import tts

FILENAME = 'recording.wav'

WORKTIME = 2.0
BREAKTIME = 0.5

def pomodoro():
    with Board() as board:
        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                if duration > WORKTIME*60:
                    break
                print('Working: %.02f second(s) left [Press button to stop]' % (WORKTIME*60 - duration), end='\r', flush=True)
                time.sleep(0.5)

        record_file(AudioFormat.CD, filename=FILENAME, wait=wait, filetype='wav')
                
        loudness_stats = pyloudness.get_loudness(FILENAME)
        
        return loudness_stats['Loudness Range']['LRA']

def main():
    score_sum = 0
    for x in range(1, 5):
        score_sum += pomodoro()
        tts.say("Break Time!")

if __name__ == '__main__':
    main()