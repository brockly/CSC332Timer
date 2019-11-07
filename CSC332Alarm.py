#!/usr/bin/env python3

from aiy.voice import tts
import vlc
import logging
import platform
import subprocess
import sys

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts
import time

p = vlc.MediaPlayer("file:///home/pi/Music/George Michael - Careless Whisper.mp3")

# Tell the user the one minute timer has been set and play the music
def timer():
    tts.say("Timer set for 1 minute")
    time.sleep(60)
    p.play()
    time.sleep(10)


# Pause the music and ask the first question
def question1():
    p.pause()
    tts.say("What is 1+1?")


# Ask the last question
def question2():
    tts.say("Now for a slightly harder question...")
    tts.say("What is 121 divided by 12?")


def _on_button_pressed(self):
    # Check if we can start a conversation. 'self._can_start_conversation'
    # is False when either:
    # 1. The assistant library is not yet ready; OR
    # 2. The assistant library is already in a conversation.
    if self._can_start_conversation:
        self._assistant.start_conversation()


def process_event(assistant, led, event):
    logging.info(event)
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print("You said:", event.args["text"])
        text = event.args["text"].lower()
        if text == "start the clock":
            assistant.stop_conversation()
            timer()
            question1()
        elif text == "two":
            tts.say("Good job! Answer one more question to stop the timer.")
            question2()
        elif text == "12":
            tts.say("The timer has been turned off!")
        else:
            tts.say("Wrong answer, try again")
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.
    elif (
        event.type == EventType.ON_CONVERSATION_TURN_FINISHED
        or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
        or event.type == EventType.ON_NO_RESPONSE
    ):
        led.state = Led.BEACON_DARK  # Ready.
    elif (
        event.type == EventType.ON_ASSISTANT_ERROR
        and event.args
        and event.args["is_fatal"]
    ):
        sys.exit(1)


def main():
    logging.basicConfig(level=logging.INFO)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, board.led, event)


if __name__ == "__main__":
    main()
