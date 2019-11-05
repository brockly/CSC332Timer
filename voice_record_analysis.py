import argparse
import time
import threading
import pyloudness

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press()

        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

        record_file(AudioFormat.CD, filename=args.filename, wait=wait, filetype='wav')
        print('Press button to save the recorded sound.')
        board.button.wait_for_press()
        
        loudness_stats = pyloudness.get_loudness("recording.wav")
        print(loudness_stats)
        print(loudness_stats['Loudness Range'])

if __name__ == '__main__':
    main()