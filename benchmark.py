#!/usr/bin/env python3
import sys

from wordle import Game
from cli import CLIConfig, CLIPlayer
from robot import RobotPlayer

if __name__=="__main__":
    game = Game()
    player = RobotPlayer(game.VALID_GUESSES)
    # NOTE: to constraining guesses to list of solutions, comment out the line above and uncomment the line below (this is cheating!)
    #player = RobotPlayer(game.VALID_SOLUTIONS)

    try:
        config = CLIConfig.from_ini()
    except:
        config = CLIConfig()

    print_losses = True
    print_wins = False
    stop_on_loss = False
    solutions = game.VALID_SOLUTIONS
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("Usage: ./benchmark.py [STRING|INTEGER]")
            print()
            print("Solves Wordle for all words in the official solution list")
            print("Options:")
            print("-h, --help\tPrint this help text and quit")
            print("STRING\t\tPlay against a single, specified solution (STRING must be in data/solutions.txt) ")
            print(f"INTEGER\t\tPlay against a given number of solutions (INTEGER must be between 1 and {len(game.VALID_SOLUTIONS)})")
            exit()
        elif sys.argv[1].isdigit():
            arg = int(sys.argv[1])
            if not (1 <= arg <= len(game.VALID_SOLUTIONS)):
                print(f"If argument is number, must be between 1 and number of valid solutions ({len(game.VALID_SOLUTIONS)})")
                exit()
            solutions = game.VALID_SOLUTIONS[:arg]
        elif sys.argv[1].isalpha():
            arg = sys.argv[1].upper()
            if not arg in game.VALID_SOLUTIONS:
                print(f"If argument is string, must be in the list of valid solutions")
                exit()
            solutions = [arg]
            print_wins = True

    print(f"Iterating {len(solutions)} solution(s), with {len(player._all_words)} valid guesses in dictionary and {len(player.PRESETS)} preset(s){(': '+', '.join(preset for preset in player.PRESETS) if len(player.PRESETS) > 0 else '')} ")

    results = []
    try:
        for solution in solutions:
            result = game.play(player, forced_solution=solution)
            results.append(result)
            if (result == None and print_losses) or (result is not None and print_wins):
                print(f"{len(results):04}: {config.LOSE+'LOSS' if result == None else config.WIN+'WIN' }: {solution}{config.RESET} guessed: { ' '.join(CLIPlayer.pretty_response(guessed_word, states, config) for guessed_word, states in player.response_history) }\xA0")
            elif len(results) % 100 == 0:
                print(f"{len(results):04}")
            if stop_on_loss and result == None:
                print("Stopping on LOSS")
                break
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        games = len(results)
        wins = sum(1 for r in results if r != None)
        losses = games - wins
        if games > 0:
            print(f"{games} games, {wins} wins ({wins*100/games:.1f}%), { losses } losses ({losses*100/games:.1f}%)")
            if wins > 0:
                print(f"wins took {(sum(g for g in results if g != None)/wins):.1f} guesses on average")
                for round in range(1, Game.ROUNDS + 1):
                    round_wins = sum(1 for g in results if g == round)
                    common_guess = max(player.common_guesses[round - 1], key=player.common_guesses[round - 1].get)
                    common_guess_count = player.common_guesses[round - 1][common_guess]
                    print(  f"round {round}:\t",
                            f"{round_wins} wins ({round_wins*100/wins:.1f}% of wins)",
                            f", most common guess: {common_guess} ({common_guess_count}x)" if common_guess_count > 0 else "",
                            sep="")
                            