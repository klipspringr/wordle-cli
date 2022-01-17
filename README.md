# wordle-cli

Command-line clone of Josh Wardle's [Wordle](https://www.powerlanguage.co.uk/wordle/), inspired by [Paul Battley's Ruby version](https://github.com/threedaymonk/wordle). Features:

- play against random solutions, or against the once-a-day "official" Wordle solution (with `--today`)
- official dictionaries of solutions and valid guesses
- spoiler-free emoji summaries for sharing
- optional hints mode (`--hints`) to show number of possible words remaining

![Screenshot of a Wordle CLI game](/assets/screenshot.png?raw=true "Screenshot of a Wordle CLI game")

## Download and run

Requires **Python 3.6** or later, and a **modern terminal app**.

To download the code and run it:

```bash
git clone https://github.com/klipspringr/wordle-cli.git && cd wordle-cli
python3 play.py
```

Alternatively, if you don't have git: click `Code > Download ZIP` on GitHub, extract the ZIP, open a terminal, `cd` to the extracted folder and run `python3 play.py`.

A **terminal with support for colours and emoji** is required. On Windows and WSL, [Windows Terminal](https://aka.ms/terminal) is the best choice. PowerShell and the Windows command prompt are only supported if running in Windows Terminal.

Not tested on **macOS**, but should work &mdash; let me know if any problems!

## Options

Usage: `python3 play.py [-h|--help] [--today|SOLUTION] [--hints]`

|Argument               |Behaviour                                                  |
|-----------------------|-----------------------------------------------------------|
|_none_                 |Use a random solution from the official Wordle dictionary  |
|`-h` , `--help`        |Print this help text and quit                              |
|`--today`              |Use today's official Wordle solution                       |
|`SOLUTION`             |Use a given SOLUTION (probably only useful for debugging)  |
|`--hints`              |After each guess, report number of possible words remaining|

Hints mode (`--hints`) looks like this:

![Screenshot of a Wordle CLI game with hints](/assets/screenshot_hints.png?raw=true "Screenshot of a Wordle CLI game with hints")

## Configuration

To change the terminal colours, sharing emoji and other variables, save the file `config.ini.defaults` as `config.ini` and uncomment and edit the relevant lines. Colours are specified using ECMA-48 Select Graphic Rendition codes ([cheat sheet](https://i.stack.imgur.com/6otvY.png)).

## Solving Wordle

Using [Knuth's minimax algorithm for Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm) and a hardcoded first guess, Wordle can be won for all words on the official solutions list. The algorithm is seeded with the official list of valid _guesses_ (not solutions). This list is effectively available to human players as well, as the game rejects invalid words without using a guess. This repo contained a solver, but it was unnecessarily slow, so I've rewritten it and may release it in due course.
