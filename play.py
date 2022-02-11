#!/usr/bin/env python3

import argparse
import random

from datetime import datetime

import wordle

from cli import CLIPlayer


def parse_cli_args() -> argparse.Namespace:
    def _solution_arg_verifier(solution_arg: str) -> str:
        if not isinstance(solution_arg, str) or len(solution_arg) != game.LENGTH:
            raise argparse.ArgumentTypeError(f"--solution argument must be a {game.LENGTH}-letter word")
        if solution_arg not in game.VALID_SOLUTIONS:
            raise argparse.ArgumentTypeError(f"{solution_arg} is not in dict")
        return solution_arg.upper()

    args = argparse.ArgumentParser()
    args.add_argument("--hints",
                      action="store_true",
                      help="After each guess, report number of possible words remaining")
    solution_args = args.add_mutually_exclusive_group()
    solution_args.add_argument("--today",
                               action="store_true",
                               help="Use today's official Wordle solution")
    solution_args.add_argument("--day",
                               type=int,
                               help="Use the official solution from this DAY")
    solution_args.add_argument("--solution",
                               type=_solution_arg_verifier,
                               help=f"Use a given SOLUTION (must be {game.LENGTH}-letter word)")

    return args.parse_args()


if __name__ == "__main__":
    game = wordle.Game()
    player = CLIPlayer()

    cli_args = parse_cli_args()

    if cli_args.today:
        delta = (datetime.utcnow() - datetime(2021, 6, 19)).days % len(game.VALID_SOLUTIONS)
        solution = game.VALID_SOLUTIONS[delta]
        player.GAME_NUMBER = delta

    elif cli_args.day:
        delta = cli_args.day % len(game.VALID_SOLUTIONS)
        solution = game.VALID_SOLUTIONS[delta]
        player.GAME_NUMBER = delta

    elif cli_args.solution:
        solution = cli_args.solution
        player.warn(f"Solution will be {solution}")

    else:
        solution = random.choice(game.VALID_SOLUTIONS)

    while True:
        try:
            game.play(player, solution, hints=cli_args.hints)
        except (KeyboardInterrupt, EOFError):
            print()
            player.quit()

        try:
            player.again()
            print()
        except (KeyboardInterrupt, EOFError):
            print()
            exit()
