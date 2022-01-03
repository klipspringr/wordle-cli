Command-line clone of Josh Wardle's [WORDLE](https://www.powerlanguage.co.uk/wordle/). Features:
- play against random solutions, or against the once-a-day "official" Wordle solution (with `--today`)
- official dictionaries of solutions and valid guesses
- spoiler-free emoji summaries for sharing

### Getting started
Requirements:
- Python 3.6 or later
- a terminal which supports colours and ANSI CSI codes, e.g. [Windows Terminal](https://aka.ms/terminal).

To get the code:
```
git clone https://github.com/klipspringr/wordle-cli.git && cd wordle-cli
```
alternatively, if you don't have git: click `Code > Download ZIP` on GitHub, extract the ZIP somewhere, and open a terminal and `cd` to the extracted folder.

To run on **Linux** or **WSL**:
```
./play.py
```
To run on **Windows**:
```
python3 play.py
```
Notes:
- **cmd.exe** (the Windows command prompt) is not supported, you need [Windows Terminal](https://aka.ms/terminal) or PowerShell
- not tested on **macOS**, but should work &mdash; let me know if any problems!

### Options
Usage: `./play.py [-h|--help|--today|SOLUTION]`

|Argument               |Behaviour                                                  |
|-----------------------|-----------------------------------------------------------|
|_none_                 |Use a random solution from the official Wordle dictionary  |
|`-h` &#124; `--help`   |Print this help text and quit                              |
|`--today`              |Use today's official Wordle solution                       |
|`SOLUTION`             |Use a given SOLUTION                                       |
