from constants import Choices, Outcomes
import random
# from ocr import Camera


class Player:
    '''

    '''

    def __init__(self, nlp, tts, name: str = None):
        self.name = name
        self.choice = None
        self.score = 0
        self.outcome = None
        self.nlp = nlp
        self.tts = tts

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
            # Select move at random for computer player
            self.choice = Choices(random.choice(list(Choices)))
            print(f"AGENT CHOICE: {self.choice}")
        else:
            valid_selection = False
            # camera = Camera()
            #
            # print("Please make a selection with your hand and press 'q' when ready to take a picture")
            # camera.capture_video()

            # CV To detect player choice from image goes here
            # selection = ocr.prediction()
            # self.choice = Choices(selection)
            # print(f"Your Choice: {self.choice}\n")

            while not valid_selection:
                self.tts.speak(text="Please choose Rock, Paper, or Scissors.")
                selection = self.nlp.listen_for_speech()

                # selection = int(input(f"{self.name} please make a selection:\n"
                #                       "(0) Rock\n"
                #                       "(1) Paper\n"
                #                       "(2) Scissors\n"))
                if "rock" in selection:
                    self.tts.speak(text=f"Your choice was rock")

                    selection = 0
                    self.choice = Choices(selection)
                    valid_selection = True
                elif "paper" in selection:
                    self.tts.speak(text=f"Your choice was paper")

                    selection = 1
                    self.choice = Choices(selection)
                    valid_selection = True
                elif "scissors" in selection:
                    self.tts.speak(text=f"Your choice was scissors")

                    selection = 2
                    self.choice = Choices(selection)
                    valid_selection = True
                else:
                    self.tts.speak(text=f"Invalid choice. You said {selection}.")
                    valid_selection = False

                # if selection < 0 or selection > 2:
                #     print(f"Invalid choice: {selection}. Please choose between 1 and 3.\n")
                #     valid_selection = False
                # else:
                #     self.choice = Choices(selection)
                #     print(f"Your Choice: {self.choice}\n")
                #     valid_selection = True

    def update_score(self):
        if self.outcome == Outcomes.WIN:
            self.score += 1
