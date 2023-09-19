#!/usr/bin/env python3.8

import sys
import platform

if platform.system() != 'Linux':
    print("The script will only run on Linux")
    sys.exit(1)

import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
	print("{} - {} {}".format(voice.id, voice.name, voice.gender))

