#!/usr/bin/env python3.8

import json
import time
import sys
import calendar
import platform

plat = platform.system()

if plat == 'Darwin':
    from speak_macos import Speak
    voice = 'com.apple.voice.compact.en-GB.Daniel'
else:
    print("Don't know how to set up for {}".format(plat))
    sys.exit(1)

from vosk import Model, KaldiRecognizer
import pyaudio

class Listen:
    # https://alphacephei.com/vosk/models

    def __init__(self, model, input_device_index):
        model = Model(model)
        self.recognizer = KaldiRecognizer(model, 16000)
        mic = pyaudio.PyAudio()

        try:
            self.stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192, input_device_index=input_device_index)
            self.stream.start_stream()
        except:
            print("Is your microphone plugged in?")
            sys.exit()

    def listen(self):
        data = self.stream.read(4096)
        return self.recognizer.AcceptWaveform(data)

    def result(self):
        text = self.recognizer.Result()
        data = json.loads(text)
        return data['text']

class Response:
    def respond(self, text):
        if text == 'date':
            return self._date()
        elif text == 'time':
            return self._time()
        else:
            return 'Pardon'

    def _date(self):
        return time.strftime("%a, %d %b %Y", time.gmtime())

    def _time(self):
        # leading zeros will be said so we need to remove them
        t = time.strftime("%I %M %p", time.gmtime()).replace(' 0', ' ')
        if t[0] == '0':
            return t[1:]
        else:
            return t

def get_ts():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    return time_stamp
    
listen = Listen("./models/vosk-model-small-en-us-0.15", 1)
speak = Speak(voice)
response = Response()

speak.say("Ready for you now")

# Trigger words
WAKE_UP = 'hello'
GO_TO_SLEEP = 'goodbye'

# Listening state
WAITING = 'waiting'
LISTENING = 'listening'

# TImeout after nothing being said for X seconds
TIMEOUT = 30

state = WAITING
last_utterance = 0

while True:
    if listen.listen():
        text = listen.result()

        if state == WAITING:
            if text == WAKE_UP:
                speak.say('hanging on your every word')
                state = LISTENING
                last_utterance = get_ts()
        elif state == LISTENING:
            if text == GO_TO_SLEEP:
                speak.say("nice chatting with you, till next time")
                state = WAITING
            elif text == '': # Nothing is said
                if get_ts() - last_utterance > TIMEOUT:
                    speak.say("Timeout")
                    state = WAITING
            else:
                speak.say(response.respond(text))
                last_utterance = get_ts()

