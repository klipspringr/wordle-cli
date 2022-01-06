## Solving Wordle

[Wordle](https://www.powerlanguage.co.uk/wordle/) is a popular game where you guess a five-letter word within six attempts. After each guess, the game tells you if each letter of your guess was (a) correct i.e. in the solution in the same position; (b) present in the solution but not in that position; or (c) not present in the solution.

This program demonstrates that, by using [Knuth's minimax algorithm](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm) with some presets for early guesses, Wordle can be played and successfully solved within six guesses for every possible solution, in a reasonable time.

The "official" version of Wordle specifies 12,972 valid guesses and 2,315 solutions. This program guesses words from the valid guess list, which is effectively available to a human player (as the game rejects invalid guesses without using up a guess).

### Results
I ran `./benchmark.py` with the first three guesses preset to FILES, PRANG, DUTCH. The program won every game:

```
$ ./benchmark.py
Iterating 2315 solution(s), with 12972 valid guesses in dictionary and 3 presets: FILES, PRANG, DUTCH
2315 games, 2315 wins (100.0%), 0 losses (0.0%)
Wins took 4.5 guesses on average
round 1:    0 wins (0.0%), most common guess: FILES (2315x)
round 2:    5 wins (0.2%), most common guess: PRANG (2310x)
round 3:    142 wins (6.1%), most common guess: DUTCH (2169x)
round 4:    1058 wins (45.7%), most common guess: ABAMP (19x)
round 5:    1013 wins (43.8%), most common guess: AJWAN (3x)
round 6:    97 wins (4.2%), most common guess: MAYBE (1x)
```

### Scope for improvement

This took 87 minutes on an antiquated laptop: no doubt there is lots of scope for optimisation, perhaps starting with dropping down to C for `check_guess`.

The algorithm guarantees a solution but makes no promises about minimising the number of guesses. It may be possible to reduce the average number of guesses (currently 4.5) with a better set of presets.

### Credits
- [goingonit's description](https://www.metafilter.com/193704/Wordle-A-daily-word-guessing-game#8185176) of Knuth's minimax algorithm for Mastermind
- preset list and some design elements taken from [Paul Battley's blog](https://po-ru.com/2021/12/24/ruining-the-fun-of-wordle-with-strategy) and [code](https://github.com/threedaymonk/wordle)
- [Rodrigo Girão Serrão](https://mathspp.com/blog/solving-wordle-with-python) spotted an important detail of Wordle's response to repeated letters
- [Josh Wardle](https://www.powerlanguage.co.uk/) for inventing Wordle
