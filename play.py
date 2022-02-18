#!/usr/bin/env python3
import random
import sys
from datetime import datetime

import wordle
from cli import CLIPlayer

def print_help_exit():
    print("Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]")
    print()
    print("Option\t\t\tBehaviour (* = mutually-exclusive)")
    print("------\t\t\t----------------------------------")
    print("none\t\t\tUse a random solution from the official Wordle dictionary")
    print("--today\t\t\t* Use today's official Wordle solution")
    print("DAY (number)\t\t* Use the official solution from this DAY")
    print("SOLUTION (string)\t* Use a given SOLUTION (must be 5-letter word)")
    print("--hints\t\t\tAfter each guess, report number of possible words remaining")
    print("-h, --help\t\tPrint this help text and quit")
    exit()

if __name__=="__main__":
    game = wordle.Game()
    player = CLIPlayer()
    
    fixed_solution = None
    hints = False
    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            print_help_exit()
        elif arg == "--today" and fixed_solution == None:
            delta = (datetime.utcnow() - datetime(2021, 6, 19)).days % len(game.VALID_SOLUTIONS)
            fixed_solution = game.VALID_SOLUTIONS[delta]
            player.GAME_NUMBER = delta
        elif arg.isdigit() and int(arg) >= 0 and fixed_solution == None:
            delta = int(arg) % len(game.VALID_SOLUTIONS)
            fixed_solution = game.VALID_SOLUTIONS[delta]
            player.GAME_NUMBER = delta
        elif arg.isalpha() and len(arg) == game.LENGTH and fixed_solution == None:
            arg = arg.upper()
            # fixed solution must be in official guesses list, but doesn't have to be in solutions list
            if arg in game.VALID_GUESSES:
                fixed_solution = arg
                player.warn(f"Solution will be { arg }")
            else:
                player.warn(f"Invalid solution { arg }, must be a valid guess")
                print_help_exit()
        elif arg == "--hints":
            hints = True
        else:
            player.warn(f"Invalid argument { arg }")
            print_help_exit()
        
    while True:
        try:
            game.play(player, random.choice(game.VALID_SOLUTIONS) if fixed_solution == None else fixed_solution, hints=hints)
        except (KeyboardInterrupt, EOFError):
            print()
            player.quit()
        
        if fixed_solution != None:
            exit()
            
        try:
            player.again()
            print()
        except (KeyboardInterrupt, EOFError):
            print()
            exit()
