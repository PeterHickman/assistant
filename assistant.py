#!/usr/bin/env python3.8

import json
import time
import sys
import calendar
import platform

plat = platform.system()

if plat == 'Darwin':
    from speak_macos import Speak
elif plat == 'Linux':
    from speak_linux import Speak
else:
    print("Don't know how to set up for {}".format(plat))
    sys.exit(1)

import settings

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
    return calendar.timegm(time.gmtime())
    
listen = Listen(settings.model, settings.input_device_index)
speak = Speak(settings.voice)
response = Response()

speak.say(settings.greeting)

# Listening state
WAITING = 'waiting'
LISTENING = 'listening'

state = WAITING
last_utterance = get_ts()

while True:
    if listen.listen():
        text = listen.result()

        if state == WAITING:
            if text == settings.wake_up_word:
                speak.say(settings.ready)
                state = LISTENING
                last_utterance = get_ts()
        elif state == LISTENING:
            if text == settings.sleep_word:
                speak.say(settings.goodbye)
                state = WAITING
            elif text == '': # Nothing is said
                pass
            else:
                speak.say(response.respond(text))
                last_utterance = get_ts()

    if get_ts() - last_utterance > settings.timeout and state == LISTENING:
        speak.say(settings.goodbye)
        state = WAITING

