from constants import Choices, Outcomes
import random
from object_detection import Camera
import time


class Player:

    def __init__(self, nlp, tts, od, name: str = None):
        self.name = name
        self.choice = None
        self.score = 0
        self.outcome = None
        self.nlp = nlp
        self.tts = tts
        self.od = od
        self.camera = Camera()

    def get_player_name(self):
        correct_name = False

        while not correct_name:
            self.tts.speak(text="What is your Name?")
            self.name = self.nlp.listen_for_speech()

            self.tts.speak(text=f"Your name is {self.name}, is that correct? Say yes or no.")
            good_name = self.nlp.listen_for_speech()

            if 'yes' in good_name:
                correct_name = True
                self.tts.speak(text=f"Good luck {self.name}!")

            else:
                correct_name = False
                self.tts.speak(text="Trying again.")

    def select_move(self):
        if self.name == "Agent":
            self.choice = Choices(random.choice(list(Choices)))
            print(f"AGENT CHOICE: {self.choice}")
        else:
            valid_selection = False

            while not valid_selection:
                self.tts.speak(text="Please choose Rock, Paper, or Scissors.")

                self.tts.speak(text="The camera is on, please place your hand in the frame with your move.")
                time.sleep(2)

                self.tts.speak(text="Taking picture in 3 seconds.")
                self.camera.capture_image()

                self.tts.speak(text="Picture taken. Predicting player choice.")
                self.od.model_predict(uploaded='player_images/player_choice.png')

                self.tts.speak(text=f"Did you choose {self.od.prediction}? Yes or No?")
                selection = self.nlp.listen_for_speech()

                if "no" in selection:
                    while True:
                        self.tts.speak(text="What was your selection?")
                        selection = self.nlp.listen_for_speech()

                        file_path = "player_images/player_choice.png"

                        if "rock" in selection:
                            self.choice = Choices.ROCK
                            self.od.label_and_save(file_path=file_path, label="rock")
                            break
                        elif "paper" in selection:
                            self.choice = Choices.PAPER
                            self.od.label_and_save(file_path=file_path, label="paper")
                            break
                        elif "scissors" in selection:
                            self.choice = Choices.SCISSORS
                            self.od.label_and_save(file_path=file_path, label="scissors")
                            break
                        else:
                            self.tts.speak(text="I didn't understand.")

                else:
                    if "rock" in self.od.prediction:
                        self.choice = Choices.ROCK
                    elif "paper" in self.od.prediction:
                        self.choice = Choices.PAPER
                    else:
                        self.choice = Choices.SCISSORS

                valid_selection = True

    def update_score(self):
        if self.outcome == Outcomes.WIN:
            self.score += 1
