'''
takes in a prompt and converts text to speech
listens for player voice input after question prompt using speech recognition
ambient background dampening
wait for trigger word to listen for player audio command
'''

import speech_recognition as sr
import pyttsx3 as tts


class NLP:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_for_speech(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("listening...")
            voice = self.recognizer.listen(source, phrase_time_limit=3)
            command = self.recognizer.recognize_sphinx(voice)
        try:
            print("You said: " + self.recognizer.recognize_sphinx(voice))
        except sr.UnknownValueError:
            print("Audio input not understood.")
        except sr.RequestError as e:
            print("Error; {0}".format(e))

        return command.lower()


class TTS:
    def __init__(self):
        self.engine = tts.init()
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.rate - 20)

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
