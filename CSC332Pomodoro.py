#!/usr/bin/env python3

# CSC 332 Pomodoro Timer
# Alec Brockman
# Carlos Samaniego
# Jules Amosah

import time
import threading
import pyloudness

from aiy.board import Board, Led
from aiy.voice.audio import (
    AudioFormat,
    play_wav,
    record_file,
    Recorder,
)
from aiy.voice import tts


class Pomodoro:
    """Handles all Pomodoro logic"""

    _file = "recording.wav"

    _score = 0

    def __init__(self, worktime, breaktime):
        self._done = threading.Event()
        self._board = Board()
        self._worktime = worktime
        self._breaktime = breaktime

    def _wait(self, state="Working"):
        start = time.monotonic()

        interval = self._worktime if state == "Working" else self._breaktime

        while not self._done.wait(0.5):
            duration = time.monotonic() - start
            if duration > interval * 60:
                break
            print(
                "{:8s}: {:07.2f} second(s) left [Press button to stop]".format(
                    state, interval * 60 - duration
                ),
                end="\r",
                flush=True,
            )

    def _work(self):
        tts.say("Time to work!")

        self._board.led.state = Led.PULSE_SLOW

        record_file(
            AudioFormat.CD, filename=self._file, wait=self._wait, filetype="wav",
        )

        tts.say("Session ended")

        self._done.clear()

        session_score = pyloudness.get_loudness(self._file)["Loudness Range"]["LRA"]

        if session_score > 40:
            tts.say("Try to be a little more quiet next round")

        self._score += session_score

    def _break(self):
        tts.say("Break time! Relax your brain!")

        self._board.led.state = Led.BEACON_DARK

        self._wait("Break")

        tts.say("Your break is over!")

        self._done.clear()

    def start(self, reps):
        self._board.led.state = Led.BEACON
        tts.say(
            "Welcome to the Pomodoro timer. I am currently set to run {} times. Press the button to start!".format(
                reps
            )
        )
        self._board.led.state = Led.PULSE_QUICK
        self._board.button.wait_for_press()
        self._board.button.when_pressed = self._done.set
        self._board.led.state = Led.PULSE_SLOW
        tts.say("I'll rate your productivity based on how quiet you are.")
        for x in range(1, reps):
            tts.say(
                "The next round begins in 5 seconds, press the button if you would like to exit the timer"
            )
            self._board.led.state = Led.PULSE_QUICK
            if self._done.wait(5):
                tts.say("Goodbye!")
                self._board.led.state = Led.OFF
                self._board.close()
                return
            self._board.led.state = Led.ON
            tts.say("Round {}".format(x))
            self._work()
            tts.say("Current score: {:03.2f} noise points".format(self._score))
            self._break()

        tts.say(
            "Congratulations! You have completed the session. Your final score is {:03.2f}".format(
                self._score
            )
        )


def main():
    Pomodoro(25, 5).start(5)


if __name__ == "__main__":
    main()
