#!/usr/bin/env python3
import random
import sys
from datetime import datetime

import wordle
from cli import CLIPlayer

def print_help():
    print("Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]")
    print()
    print("Option\t\tBehaviour (* = mutually-exclusive)")
    print("------\t\t----------------------------------")
    print("none\t\tUse a random solution from the official Wordle dictionary")
    print("--today\t\t* Use today's official Wordle solution")
    print("DAY (number)\t* Use the official solution from this DAY")
    print("SOLUTION (str)\t* Use a given SOLUTION (must be 5-letter word)")
    print("--hints\t\tAfter each guess, report number of possible words remaining")
    print("-h, --help\tPrint this help text and quit")
    exit()

if __name__=="__main__":
    game = wordle.Game()
    player = CLIPlayer()
    
    solution = None
    hints = False
    loop = False
    bot = False
    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            print_help()
        elif arg == "--today" and solution == None:
            delta = (datetime.utcnow() - datetime(2021, 6, 19)).days % len(game.VALID_SOLUTIONS)
            solution = game.VALID_SOLUTIONS[delta]
            player.GAME_NUMBER = delta
        elif arg.isdigit() and int(arg) >= 0 and solution == None:
            delta = int(arg) % len(game.VALID_SOLUTIONS)
            solution = game.VALID_SOLUTIONS[delta]
            player.GAME_NUMBER = delta
        elif arg.isalpha() and len(arg) == game.LENGTH and solution == None:
            solution = arg.upper()
            player.warn(f"Solution will be { solution }")
        elif arg == "--hints":
            hints = True
        elif arg == "--bot":
            bot = True
        else:
            player.warn(f"Invalid argument { arg }")
            print_help()

    if solution == None:
        solution = random.choice(game.VALID_SOLUTIONS)
        loop = True
         
    while True:
        try:
            game.play(player, solution, hints=hints, bot=bot)
        except (KeyboardInterrupt, EOFError):
            print()
            player.quit()
        
        if not loop:
            exit()
            
        try:
            player.again()
            print()
        except (KeyboardInterrupt, EOFError):
            print()
            exit()
