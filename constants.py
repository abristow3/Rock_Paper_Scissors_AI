from enum import Enum


class Outcomes(Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2


class Choices(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class ReadyStatus(Enum):
    NOT_READY = 0
    READY = 1

