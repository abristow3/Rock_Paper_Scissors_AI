import speech_recognition as sr
import pyttsx3 as tts
import sounddevice


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


if __name__ == '__main__':

    sr.Microphone.list_microphone_names()
    nlp = NLP()
    tts = TTS()

    tts.speak(text="Hello this is a test. Please speak now")
    audio = nlp.listen_for_speech()
    tts.speak(text=f"you said {audio}")
