#!/usr/bin/env python3.8

import sys
import platform

if platform.system() != 'Darwin':
    print("The script will only run on Darwin/Macos")
    sys.exit(1)

from AppKit import NSSpeechSynthesizer

i = 0
for voice in NSSpeechSynthesizer.availableVoices():
   print("{} - {}".format(i, voice))
   i = i + 1
