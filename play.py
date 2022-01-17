#!/usr/bin/env python3
import sys

import wordle
from cli import CLIPlayer

def print_help():
    print("Usage: python3 play.py [-h|--help] [--today|SOLUTION] [--hints]")
    print()
    print("Default:\tUse a random solution from the official Wordle dictionary")
    print("Options:")
    print("-h, --help\tPrint this help text and quit")
    print("--today\t\tUse today's official Wordle solution")
    print("SOLUTION\tUse a given SOLUTION (probably only useful for debugging)")
    print("--hints\t\tAfter each guess, report number of possible words remaining")
    exit()

if __name__=="__main__":
    game = wordle.Game()
    player = CLIPlayer()
    
    today_solution = False
    forced_solution = None
    hints = False
    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            print_help()
        elif arg == "--today" and forced_solution == None:
            today_solution = True
        elif game.is_valid_solution(arg.upper()) and today_solution == False:
            forced_solution = arg.upper()
        elif arg == "--hints":
            hints = True
        else:
            player.warn(f"Invalid argument { arg }")
            print_help()

    if forced_solution:
        player.warn(f"Solution will be { forced_solution }")

    while True:
        try:
            game.play(player, forced_solution=forced_solution, today_solution=today_solution, hints=hints)
        except (KeyboardInterrupt, EOFError):
            print()
            player.quit()
        
        if forced_solution or today_solution:
            exit()
            
        try:
            player.again()
            print()
        except (KeyboardInterrupt, EOFError):
            print()
            exit()
