from player import Player
from constants import ReadyStatus, Choices, Outcomes
from time import sleep
# from ocr import Camera
from nlp import NLP, TTS


class RPS:
    def __init__(self):
        self.round_num = 0
        self.play_again = True
        self.ready = ReadyStatus.NOT_READY
        self.tts = TTS()
        self.nlp = NLP()
        self.human_player = Player(nlp=self.nlp, tts=self.tts)
        self.computer_player = Player(name="Agent", nlp=self.nlp, tts=self.tts)

    def initial_setup(self):
        self.tts.speak(text="Welcome to Rock Paper Scissors Companion!")
        # print("=== Welcome to Rock Paper Scissors Companion!===\n")
        self.human_player.get_player_name()

    def play_round(self):
        self.new_round_setup()
        self.get_ready_status()

        self.select_moves()
        self.determine_outcome()

        self.update_scores()
        self.display_scores()

        self.continue_playing()

    def get_ready_status(self):
        while self.ready == ReadyStatus.NOT_READY:
            self.tts.speak(text="Are you ready to play? Answer yes or no.")
            selection = self.nlp.listen_for_speech()

            if "yes" in selection:
                self.ready = ReadyStatus.READY
            elif "no" in selection:
                self.ready = ReadyStatus.NOT_READY
                print("Waiting 5 seconds and trying again.\n")
                sleep(5)
            elif "yes" not in selection or "no" not in selection:
                self.ready = ReadyStatus.NOT_READY
                self.tts.speak(text=f"Invalid choice: {selection}. Please say yes or no.")

    def determine_outcome(self):
        print(f"{self.human_player.name} chose: {self.human_player.choice}."
              f"{self.computer_player.name} chose: {self.computer_player.choice}")

        if self.human_player.choice == self.computer_player.choice:
            print("The outcome is a DRAW!\n")
            self.human_player.outcome = Outcomes.DRAW
            self.computer_player.outcome = Outcomes.DRAW

        elif (self.human_player.choice == Choices.ROCK and self.computer_player.choice == Choices.PAPER) or \
                (self.human_player.choice == Choices.PAPER and self.computer_player.choice == Choices.SCISSORS) or \
                (self.human_player.choice == Choices.SCISSORS and self.computer_player.choice == Choices.ROCK):

            print(f"{self.human_player.name} LOSES!\n")
            self.human_player.outcome = Outcomes.LOSE
            self.computer_player.outcome = Outcomes.WIN

        else:
            print(f"{self.human_player.name} WINS!\n")
            self.human_player.outcome = Outcomes.WIN
            self.computer_player.outcome = Outcomes.LOSE

    def update_scores(self):
        self.human_player.update_score()
        self.computer_player.update_score()

    def select_moves(self):
        self.human_player.select_move()
        self.computer_player.select_move()

    def display_scores(self):
        print(f"The score is:\n"
              f"{self.human_player.name}: {self.human_player.score}\n"
              f"{self.computer_player.name}: {self.computer_player.score}\n")

    def update_round_number(self):
        self.round_num += 1

    def continue_playing(self):
        valid_choice = False

        while not valid_choice:
            play = int(input("Would you like to play again? (1)Yes (0)No"))

            if play < 0 or play > 1:
                print("Invalid choice please choose 0 or 1.\n")
                valid_choice = False
            elif play == 0:
                print("GOOD BYE!")
                self.play_again = False
                valid_choice = True
            elif play == 1:
                self.play_again = True
                valid_choice = True

    def new_round_setup(self):
        self.ready = ReadyStatus.NOT_READY
        self.update_round_number()

    def run(self):
        self.initial_setup()
        while self.play_again:
            self.play_round()


if __name__ == '__main__':
    game = RPS()
    game.run()
