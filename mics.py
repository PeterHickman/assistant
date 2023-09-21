#!/usr/bin/env python3.8

##
# List all the available input sources and their index
##

import sounddevice

for device in sounddevice.query_devices(device=None, kind=None):
    if device['max_input_channels'] > 0:
        print("{} - {} ({} channels)".format(device['index'], device['name'], device['max_input_channels']))
