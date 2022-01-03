import platform
import shutil
import string
import subprocess
import sys

try:
    import readline
except ImportError:
    pass

import wordle


class Colours:
    RESET = "\x1b[0m"
    WARN = "\x1b[33m"
    WIN = "\x1b[1;32m"
    LOSE = "\x1b[1;31m"
    HI = "\x1b[1m"
    DIM = "\x1b[2m"
    STATES = {
        wordle.LetterStates.CORRECTPOSITION:    "\x1b[42;30m",
        wordle.LetterStates.INCORRECTPOSITION:  "\x1b[43;30m",
        wordle.LetterStates.NOTPRESENT:         "\x1b[40;37m",
        wordle.LetterStates.NOTGUESSEDYET:      DIM
    }
    EMOJI = {
        wordle.LetterStates.CORRECTPOSITION:    "🟩",
        wordle.LetterStates.INCORRECTPOSITION:  "🟨",
        wordle.LetterStates.NOTPRESENT:         "⬛"
    }

class CLIPlayer:
    _ROUNDS = wordle.Game.ROUNDS
    _WINS = ["🤯 GENIUS", "🧠 MAGNIFICENT", "🔥 IMPRESSIVE", "🏆 SPLENDID", "🏅 GREAT", "👍 NICE"]

    _lines_since_hint = 0
    _round_history = []
    _all_letters = {}

    def initialise(self):
        self._lines_since_hint = 0
        self._response_history = []
        self._all_letters = {letter: wordle.LetterStates.NOTGUESSEDYET for letter in string.ascii_uppercase}

        self.out(f"Let's play a game of Wordle")
        self.show_hint(first=True)

    def guess(self, round):
        prompt = f"Guess { round }/{ self._ROUNDS}: "
        guess = input(prompt).upper()
        sys.stdout.write(f"\033[A{prompt}")
        return guess

    def response(self, response):
        self._response_history.append(response)
        for letter, state in response:
            if self._all_letters[letter] != wordle.LetterStates.CORRECTPOSITION:
                self._all_letters[letter] = state
        self.out(CLIPlayer.pretty_response(response))
        self.show_hint()

    def warn(self, warning):
        self.out(f"{ Colours.WARN }{ warning }")

    def win(self, round, number=None):
        self.out(f"{ Colours.WIN }{ self._WINS[round - 1] }! Got it in { round }/{ self._ROUNDS } rounds")
        
        share_text = "wordle-cli {n}{r}/{R}\n".format(n=f"{number} " if number else "", r=round, R=self._ROUNDS)
        for response in self._response_history:
            share_text += "\n" + "".join(Colours.EMOJI[state] for _, state in response)

        if CLIPlayer.try_clipboard(share_text):
            self.out(f"{ Colours.DIM }📣 Shareable summary copied to clipboard")
        else:
            self.out(f"{ Colours.DIM }📣 Shareable summary:")
            self.out(share_text + "\n")

    def lose(self, solution):
        self.out(f"{ Colours.LOSE }🤦 LOSE! The solution was { solution }")

    def quit(self):
        self.out(f"{ Colours.LOSE }QUIT!")

    def out(self, string=""):
        # print reset and non-breaking space to avoid glitching on terminal resize
        print(f"{ string }{ Colours.RESET }\xA0")
        if self._lines_since_hint > 0:
            self._lines_since_hint += 1

    def show_hint(self, first=False):
        sys.stdout.write("\033[F" * self._lines_since_hint)
        sys.stdout.write(CLIPlayer.pretty_response(self._all_letters.items())+"\xA0")
        sys.stdout.write("\033[E" * self._lines_since_hint)
        if first:
            sys.stdout.write("\n")
            self._lines_since_hint = 1

    @staticmethod
    def pretty_response(response) -> str:
        return "".join(f"{ Colours.STATES[state] }{ letter }{ Colours.RESET }" for letter, state in response)

    @staticmethod
    def try_clipboard(text):
        try:
            if hasattr(platform.uname(), "release") and "microsoft-standard" in platform.uname().release:
                clip = shutil.which("clip.exe") # WSL
            elif platform.system() == "Linux":
                clip = shutil.which("xclip") # Untested!
            elif platform.system() == "Darwin":
                clip = shutil.which("pbcopy") # Untested!
            if clip == None:
                return False
            p = subprocess.Popen(clip, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, env={'LANG': 'en_US.UTF-8'})
            p.communicate(input=text.encode('utf-8'))
            return p.returncode == 0
        except:
            return False
