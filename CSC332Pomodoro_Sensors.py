#!/usr/bin/env python3

# CSC 332 Pomodoro Timer
# Alex Brockman
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
#from gpizero import Servo
#import aiy.voicehat
import RPi.GPIO as GPIO

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.OUT) #Servo slot 0
GPIO.setup(6,GPIO.OUT)  #Servo slot 1
GPIO.setup(13,GPIO.OUT) #Servo slot 2
GPIO.setup(5,GPIO.OUT)  #Servo slot 3


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
        
        third = float(interval / 3)

        while not self._done.wait(0.5):
            duration = time.monotonic() - start
            
            print(
                "{:8s}: {:07.2f} second(s) left [Press button to stop]".format(
                    state, interval * 60 - duration
                ),
                end="\r",
                flush=True,
            )
            
            #LED light logic
            if (interval * 60 - duration) > 60 * (2.0 * third):
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.HIGH)
                GPIO.output(13,GPIO.HIGH)
            elif (interval * 60 - duration) > 60 * (1.0 * third):
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.HIGH)
                GPIO.output(13,GPIO.LOW)
            elif (interval * 60 - duration) > 60 * (0.0 * third):
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.LOW)
                GPIO.output(13,GPIO.LOW)
            else:
                GPIO.output(26,GPIO.LOW)
                GPIO.output(6,GPIO.LOW)
                GPIO.output(13,GPIO.LOW)
                
            #If the time is over, break
            if duration > interval * 60:
                break
            

    def _work(self):
        tts.say("Time to work! The LED lights will turn off as time elapses.")

        self._board.led.state = Led.PULSE_SLOW

        record_file(
            AudioFormat.CD, filename=self._file, wait=self._wait, filetype="wav",
        )

        self._done.clear()

        session_score = pyloudness.get_loudness(self._file)["Loudness Range"]["LRA"]


        tts.say("Session score: {:.2}".format(session_score))

        if session_score > 5:
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
    def distance():
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
 
        return distance


def main():
    #study time, break time, round times
    Pomodoro(1, 1).start(2)


if __name__ == "__main__":
    main()

