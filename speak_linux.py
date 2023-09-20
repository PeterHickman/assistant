import pyttsx3

class Speak:
    def __init__(self, voice):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', voice)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
