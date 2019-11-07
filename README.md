# CSC332Timer

## By: Alex Brockman, Carlos Samaniego, Juleo Amosah

---

In this project we use a Raspberry Pi and an AIY Voice Kit in order to create our own timer that turns off when we answer two different math questions. The project is a work in progress and we plan to add it to the future Wake Forest Ubiquitous Computing space.

## Non-Library Requirements for Alarm Clock Project

- Start voice detection when device is turned on
- Use "OK Google" hotword to "start the clock" for 1 minute
- When alarm goes off, user must answer 2 math questions or timer will continue

_Note: User must answer questions after saying "OK Google" again_

For Part 2 of the project, we are building a Pomodoro timer with context-aware functionality. It will use the internal microphone to score your productivity during a particular work session.

We will need these two libraries at a minimum to accomplish our goals:

- [aiy.voice.audio](https://aiyprojects.readthedocs.io/en/latest/aiy.voice.audio.html) for its audio recorder function
- [PyLoudness](https://github.com/mr-rigden/pyloudness) for sound measurements
