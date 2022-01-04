Command-line clone of Josh Wardle's [WORDLE](https://www.powerlanguage.co.uk/wordle/), inspired by [Paul Battley's Ruby version](https://github.com/threedaymonk/wordle). Features:
- play against random solutions, or against the once-a-day "official" Wordle solution (with `--today`)
- official dictionaries of solutions and valid guesses
- spoiler-free emoji summaries for sharing

![Screenshot of a Wordle CLI game](/assets/screenshot.png?raw=true "Screenshot of a Wordle CLI game")

### Download and run (`./play.py`)
Requires Python 3.6 or later, and a terminal which supports colours and ANSI CSI codes, e.g. [Windows Terminal](https://aka.ms/terminal).

To get the code:
```
git clone https://github.com/klipspringr/wordle-cli.git && cd wordle-cli
```
alternatively, if you don't have git: click `Code > Download ZIP` on GitHub, extract the ZIP, open a terminal and `cd` to the extracted folder.

To run on **Linux** or **WSL**:
```
./play.py
```
To run on **Windows** in [Windows Terminal](https://aka.ms/terminal) or PowerShell:
```
python3 play.py
```
The Windows command prompt (`cmd.exe`) is not supported.

Not tested on **macOS**, but should work &mdash; let me know if any problems!

### Options
Usage: `./play.py [-h|--help|--today|SOLUTION]`

|Argument               |Behaviour                                                  |
|-----------------------|-----------------------------------------------------------|
|_none_                 |Use a random solution from the official Wordle dictionary  |
|`-h` , `--help`        |Print this help text and quit                              |
|`--today`              |Use today's official Wordle solution                       |
|`SOLUTION`             |Use a given SOLUTION (probably only useful for debugging)  |

### Config file

To tweak the terminal colours and other variables, copy `config.ini.defaults` to `config.ini` and uncomment and edit the relevant lines. Colours are specified using ECMA-48 Select Graphic Rendition codes ([cheat sheet](https://i.stack.imgur.com/6otvY.png)).
