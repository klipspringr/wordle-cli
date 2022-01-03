import os
import platform
import shutil
import string
import subprocess
import sys
from configparser import ConfigParser

try:
    import readline
except ImportError:
    pass

from wordle import LetterStates, Game

class CLIConfig:
    RESET = "\x1b[0m"
    WARN = "\x1b[33m"
    WIN = "\x1b[1;32m"
    LOSE = "\x1b[1;31m"
    HI = "\x1b[1m"
    DIM = "\x1b[2m"
    STATE_COLOURS = {
        LetterStates.CORRECTPOSITION:    "\x1b[42;30m",
        LetterStates.INCORRECTPOSITION:  "\x1b[43;30m",
        LetterStates.NOTPRESENT:         "\x1b[40;37m",
        LetterStates.NOTGUESSEDYET:      "\x1b[2m"
        }
    SHARE_EMOJI = {
        LetterStates.CORRECTPOSITION:    "🟩",
        LetterStates.INCORRECTPOSITION:  "🟨",
        LetterStates.NOTPRESENT:         "⬛"
        }
    WIN_MESSAGES = {
        1: "🤯 GENIUS",
        2: "🧠 MAGNIFICENT",
        3: "🔥 IMPRESSIVE",
        4: "🏆 SPLENDID",
        5: "🏅 GREAT",
        6: "👍 NICE"
        }

class CLIPlayer:
    _C : CLIConfig
    _ROUNDS = Game.ROUNDS

    _lines_since_hint = -1
    _round_history = []
    _all_letters = {}

    def __init__(self, config_file="config.ini"):
        try:
            self._C = self.parse_config(config_file)
        except Exception as e:
            self._C = CLIConfig()
            self.warn(f"Failed to parse config file, ignoring it ({ e })")

    def start(self):
        self._lines_since_hint = -1
        self._response_history = []
        self._all_letters = {letter: LetterStates.NOTGUESSEDYET for letter in string.ascii_uppercase}

        self.out(f"Let's play a game of Wordle")
        self.update_hint()

    def guess(self, round) -> str:
        prompt = f"Guess { round }/{ self._ROUNDS}: "
        guess = input(prompt).upper()
        sys.stdout.write(f"\033[A\033[{len(prompt)}C\033[K") # move cursor up one line, right by len(prompt), then clear rest of line
        return guess

    def response(self, response):
        self._response_history.append(response)
        for letter, state in response:
            if self._all_letters[letter] != LetterStates.CORRECTPOSITION:
                self._all_letters[letter] = state
        self.out(self.pretty_response(response))
        self.update_hint()

    def warn(self, warning):
        self.out(f"{ self._C.WARN }{ warning }")

    def win(self, round, number=None):
        self.out(f"{ self._C.WIN }{ self._C.WIN_MESSAGES[round] }! Got it in { round }/{ self._ROUNDS } rounds")
        
        share_text = "wordle-cli {n}{r}/{R}\n".format(n=f"{number} " if number else "", r=round, R=self._ROUNDS)
        for response in self._response_history:
            share_text += "\n" + "".join(self._C.SHARE_EMOJI[state] for _, state in response)

        if CLIPlayer.try_clipboard(share_text):
            self.out(f"📣 Shareable summary copied to clipboard")
        else:
            self.out(f"📣 Shareable summary:")
            self.out(share_text + "\n")

    def lose(self, solution):
        self.out(f"{ self._C.LOSE }🤦 LOSE! The solution was { solution }")

    def quit(self):
        self.out(f"{ self._C.LOSE }QUIT!")

    def again(self) -> str:
        return input(f"Play again { self._C.DIM }[Enter]{ self._C.RESET } or exit { self._C.DIM }[Ctrl-C]{ self._C.RESET }? ")

    def out(self, string=""):
        # print reset and non-breaking space to avoid glitching on terminal resize
        print(f"{ string }{ self._C.RESET }\xA0")
        if self._lines_since_hint >= 1:
            self._lines_since_hint += 1

    def update_hint(self):
        if self._lines_since_hint >= 1:
            sys.stdout.write(f"\033[{self._lines_since_hint}F") # move cursor up to hint line
        sys.stdout.write(self.pretty_response(self._all_letters.items())+"\xA0")
        if self._lines_since_hint >= 1:
            sys.stdout.write(f"\033[{self._lines_since_hint}E") # move cursor back down
        elif self._lines_since_hint == -1:
            sys.stdout.write("\n")
            self._lines_since_hint = 1

    def pretty_response(self, response) -> str:
        return CLIPlayer.pretty_response(response, self._C)
    
    # static method for use by other Player types
    @staticmethod
    def pretty_response(response, config: CLIConfig = CLIConfig()) -> str:
        return "".join(f"{ config.STATE_COLOURS[state] }{ letter }{ config.RESET }" for letter, state in response)

    @staticmethod
    def parse_config(config_file) -> CLIConfig:
        c = CLIConfig()
        parser = ConfigParser(comment_prefixes=("#"))
        if len(parser.read(os.path.join(os.path.dirname(__file__), config_file))) == 0:
            return c
        # loop through attributes of CLIConfig class and override values from config, if set
        for attr in dir(c):
            if isinstance(getattr(c, attr), dict) and parser.has_section(attr):
                for key in getattr(c, attr):
                    if parser.has_option(attr, str(key)):
                        getattr(c, attr)[key] = ("\x1b[{v}m" if attr == "STATE_COLOURS" else "{v}").format(v=parser.get(attr, str(key)))
                        #print(f"set { attr }[{ key }] to { getattr(c, attr)[key] } TEST {c.RESET}") # debug
            elif not attr.startswith("__") and attr != "RESET" and attr.isupper() and parser.has_option("COLOURS", attr):
                setattr(c, attr, "\x1b[{v}m".format(v=parser.get("COLOURS", attr)))
                #print(f"set { attr } to { getattr(c, attr) } TEST {c.RESET}") # debug
        return c

    @staticmethod
    def try_clipboard(text) -> bool:
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
