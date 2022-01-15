import os
import random
from datetime import datetime
from enum import Enum
from typing import List

class LetterStates(Enum):
    NOTGUESSEDYET = 0
    NOTPRESENT = 1
    INCORRECTPOSITION = 2
    CORRECTPOSITION = 3

class Game:
    ROUNDS = 6
    LENGTH = 5
    WIN_STATES = [LetterStates.CORRECTPOSITION for _ in range(LENGTH)]

    def __init__(self, path_solutions="data/solutions.txt", path_guesses="data/guesses.txt"):
        with open(os.path.join(os.path.dirname(__file__), path_solutions), "r") as f:
            self.VALID_SOLUTIONS = tuple(l.upper() for l in f.read().splitlines() if len(l) == self.LENGTH)

        with open(os.path.join(os.path.dirname(__file__), path_guesses), "r") as f:
            self.VALID_GUESSES = tuple(l.upper() for l in f.read().splitlines() if len(l) == self.LENGTH)

        # official list of guesses does not include solutions, so add them, ignoring duplicates (albeit no duplicates in official lists)
        self.VALID_GUESSES = tuple(set(self.VALID_SOLUTIONS + self.VALID_GUESSES))

    def is_valid_solution(self, solution) -> bool:
        return len(solution) == self.LENGTH and solution in self.VALID_SOLUTIONS
   
    def play(self, player, forced_solution=None, today_solution=False):
        if forced_solution:
            solution = forced_solution
        elif today_solution:
            delta = (datetime.utcnow() - datetime(2021, 6, 19)).days % len(self.VALID_SOLUTIONS)
            solution = self.VALID_SOLUTIONS[delta]
        else:
            solution = random.choice(self.VALID_SOLUTIONS)
        
        player.start()
        round = 1
        while round <= self.ROUNDS:
            while True:
                guess = player.guess(round)
                if player.ASSUME_GUESSES_VALID:
                    break
                elif len(guess) != self.LENGTH or not guess.isalpha():
                    guess = guess.strip()
                    player.warn(f"{ guess[:5]+'..' if len(guess) > self.LENGTH else guess } invalid")
                elif guess not in self.VALID_GUESSES:
                    player.warn(f"{ guess } not in dict".strip())
                else:
                    break
           
            states = Game.check_guess(guess, solution)
            player.handle_response(guess, states)
            if states == Game.WIN_STATES:
                if hasattr(player, "handle_win"):
                    player.handle_win(round, game_identifier=(delta if today_solution else None))
                return round

            round += 1

        if hasattr(player, "handle_loss"):
            player.handle_loss(solution)
        return None
    
    @staticmethod
    def check_guess(guess: str, solution: str) -> List[LetterStates]:
        if guess == solution:
            return Game.WIN_STATES
        
        # https://mathspp.com/blog/solving-wordle-with-python
        # pool is set of letters in the solution available for INCORRECTPOSITION
        pool = {}
        for g, s in zip(guess, solution):
            if g == s:
                continue
            if s in pool:
                pool[s] += 1
            else: 
                pool[s] = 1

        states = []
        for guess_letter, solution_letter in zip(guess, solution):
            if guess_letter == solution_letter:
                states.append(LetterStates.CORRECTPOSITION)
            elif guess_letter in solution and guess_letter in pool and pool[guess_letter] > 0:
                states.append(LetterStates.INCORRECTPOSITION)
                pool[guess_letter] -= 1
            else:
                states.append(LetterStates.NOTPRESENT)
        return states

    @staticmethod
    def is_same_response(guess: str, solution: str, other_response: List[LetterStates]) -> bool:
        if guess == solution:
            return other_response == Game.WIN_STATES
        
        # https://mathspp.com/blog/solving-wordle-with-python
        # pool is set of letters in the solution available for INCORRECTPOSITION 
        pool = {}
        for g, s in zip(guess, solution):
            if g == s:
                continue
            if s in pool:
                pool[s] += 1
            else: 
                pool[s] = 1

        for guess_letter, solution_letter, other_state in zip(guess, solution, other_response):
            if guess_letter == solution_letter:
                if other_state != LetterStates.CORRECTPOSITION:
                    return False
            elif guess_letter in solution and guess_letter in pool and pool[guess_letter] > 0:
                if other_state != LetterStates.INCORRECTPOSITION:
                    return False
                pool[guess_letter] -= 1
            else:
                if other_state != LetterStates.NOTPRESENT:
                    return False
        
        return True
