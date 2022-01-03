import os
import random
from datetime import datetime
from enum import Enum

class LetterStates(Enum):
    NOTGUESSEDYET = 0
    NOTPRESENT = 1
    INCORRECTPOSITION = 2
    CORRECTPOSITION = 3

class Game:
    ROUNDS = 6
    LENGTH = 5
    VALID_SOLUTIONS = tuple()
    VALID_GUESSES = tuple()

    _solution = ""

    def __init__(self, path_solutions="data/solutions.txt", path_guesses="data/guesses.txt"):
        with open(os.path.join(os.path.dirname(__file__), path_solutions), "r") as f:
            self.VALID_SOLUTIONS = tuple(l.upper() for l in f.read().splitlines() if len(l) == self.LENGTH)

        with open(os.path.join(os.path.dirname(__file__), path_guesses), "r") as f:
            self.VALID_GUESSES = tuple(l.upper() for l in f.read().splitlines() if len(l) == self.LENGTH)

        # default list of guesses does not include solutions, so add them
        self.VALID_GUESSES = tuple(set(self.VALID_SOLUTIONS + self.VALID_GUESSES))

    def is_valid_solution(self, s):
        return len(s) == self.LENGTH and s in self.VALID_SOLUTIONS
   
    def play(self, player, forced_solution=None, today_solution=False):
        if today_solution:
            delta = (datetime.utcnow() - datetime(2021, 6, 19)).days % len(self.VALID_SOLUTIONS)
            self._solution = self.VALID_SOLUTIONS[delta]
        elif forced_solution:
            self._solution = forced_solution
        else:
            self._solution = random.choice(self.VALID_SOLUTIONS)
        
        player.initialise()
        round = 1
        while round <= self.ROUNDS:
            while True:
                guess = player.guess(round)
                if len(guess) != self.LENGTH or not guess.isalpha():
                    player.warn(f"{ guess } invalid guess (expected 5-letter word)".strip())
                elif guess not in self.VALID_GUESSES:
                    player.warn(f"{ guess } not in dictionary")
                else:
                    break
           
            response = []
            for index, letter in enumerate(guess):
                if letter == self._solution[index]:
                    response.append((letter, LetterStates.CORRECTPOSITION))
                elif letter in self._solution:
                    response.append((letter, LetterStates.INCORRECTPOSITION))
                else:
                    response.append((letter, LetterStates.NOTPRESENT))
            player.response(response)

            if guess == self._solution:
                player.win(round, delta if today_solution else None)
                return round
            round += 1

        player.lose(self._solution)
        return None
