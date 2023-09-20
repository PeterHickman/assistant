# Assistant

When everybody and their dog is creating voice controlled assistants I wanted in. And I don't even own a dog!

I have a thing for offline applications, I know that there are some excellent free online tts and stt services but I wanted an offline one. I spent hours battling [CMU Sphinx](https://cmusphinx.github.io/) to get it to work on my Mac only to give up as it was a complete pain. Then I found out about [Vosk](https://github.com/alphacep/vosk-api) and my interest was reignited

I mostly work on a Macintosh so this is where most of the work is being done, next I try to get it to work on Linux (specifically Zorin) and I hope to get it running on a Raspberry Pi. Maybe Windows if I have some dreadful sins to atone for :)

My Macintosh environment is old and crusty (unlike my Linux environment which was a fresh install) and so might already have a bunch of dependencies already installed that are not listed here. Unlike on Linux where I had a fresh install so anything that was needed caused the setup to fail

## Setting up on a Macintosh

Best to run this with Python 3.8 in a venv. The requirements are in `requirements.macos.txt`. The `mics.py` script will list the various input sources available to you (if you have plugged them in) and the `voices_macos.py` script will list the available voices

Download a small model from [models](https://alphacephei.com/vosk/models) and unpack it in the `models` directory

You should be good to go

## Setting up on Linux (not Raspberry Pi)

This is a work in progress. The requirements are in `requirements.linux.txt` but before that you might need to install a few things:

```
apt install python3.8-venv
apt install python3-pip
apt install portaudio19-dev
apt install python3-pyaudio
apt install python3-espeak
```

I had to install these from a fresh install of Zorin, but had similar issues with Debian 12. Again `mics.py` will list your input sources and `voices_linux.py` will list the available voices

