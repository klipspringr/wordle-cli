#!/usr/bin/env python3
import sys

import wordle
from cli import CLIPlayer, Colours

if __name__=="__main__":
    game = wordle.Game()
    player = CLIPlayer()

    today_solution = False
    forced_solution = None
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("Usage: ./play.py [-h|--help|--today|SOLUTION]")
            print()
            print("no parameters\tUse a random solution from the official Wordle dictionary")
            print("-h|--help\tPrint this help text and quit")
            print("--today\t\tUse today's official Wordle solution")
            print("SOLUTION\tUse a given SOLUTION (e.g. play.py TIGHT)")
            exit()
        elif sys.argv[1] == "--today":
            today_solution = True
        elif game.is_valid_solution(sys.argv[1].upper()):
            forced_solution = sys.argv[1].upper()
            player.warn(f"Solution will be { forced_solution }")
        else:
            player.warn(f"Ignoring invalid argument { sys.argv[1].upper() }")

    while True:
        try:
            game.play(player, forced_solution=forced_solution, today_solution=today_solution)
        except KeyboardInterrupt:
            print()
            player.quit()
            
        try:
            input(f"Play again { Colours.DIM }[Enter]{ Colours.RESET } or exit { Colours.DIM }[Ctrl-C]{ Colours.RESET }? ")
            print()
        except KeyboardInterrupt:
            print()
            exit()
