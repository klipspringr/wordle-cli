from wordle import Game, LetterStates

class RobotPlayer:
    ASSUME_GUESSES_VALID = True
    
    PRESETS = ["FILES", "PRANG", "DUTCH"] # https://po-ru.com/2021/12/24/ruining-the-fun-of-wordle-with-strategy

    # Some alternative presets of varying usefulness:
    #PRESETS = ["SOARE", "UNTIL"]
    #PRESETS = ["ARISE", "CLOUT", "NYMPH", "BADGE"]
    #PRESETS = ["ORATE", "LYSIN", "CHUMP", "BEGAD"]
    #PRESETS = ["FILES", "PRANG", "DUTCH", "WOMBY"]

    def __init__(self, valid_guesses : tuple):
        self._all_words = valid_guesses

        self.response_history = []
        self._possible_solutions = []
        self._guessed_words = set()
        self.common_guesses = [{guess: 0 for guess in self._all_words} for _ in range(Game.ROUNDS)]

    def start(self):
        self.response_history = []
        self._possible_solutions = [word for word in self._all_words]
        self._guessed_words = set()

    def guess(self, round) -> str:
        if len(self._possible_solutions) == 1:
            guess = self._possible_solutions[0]
        elif round <= len(self.PRESETS):
            guess = self.PRESETS[round - 1]
        else:
            guess = self.minimax_guess()

        self.common_guesses[round - 1][guess] += 1
        return guess

    def minimax_guess(self):
        scores = {}
        count_possible_solutions = len(self._possible_solutions)
        # For every possible guess
        for guess in self._all_words:
            if guess in self._guessed_words:
                continue
            min_eliminated = count_possible_solutions
            # Test possible guess against every possible solution
            for possible_solution in self._possible_solutions:
                states = Game.check_guess(guess, possible_solution)
                eliminated = 0
                # Count number of possible solutions that would be eliminated by the guess, if the true solution was possible_solution
                for s in self._possible_solutions:
                    if not Game.is_same_response(guess, s, states):
                        eliminated += 1
                if eliminated < min_eliminated:
                    min_eliminated = eliminated
                if min_eliminated == 0:
                    break # no need to test against further possible solutions if min eliminated already zero 
            scores[guess] = min_eliminated
        
        max_score = max(scores.values())
        best_guesses = [guess for guess, score in scores.items() if score == max_score]
        if len(best_guesses) == 1:
            return best_guesses[0]

        # if more than one best guess, sort alphabetically and return first one (ensures guesses are deterministic)
        # prefer a best guess which is a possible solution
        best_guesses = sorted(best_guesses)
        for best_guess in best_guesses:
            if best_guess in self._possible_solutions:
                return best_guess
        return best_guesses[0]

    def handle_response(self, guess: str, states: list[LetterStates]):
        self.response_history.append((guess, states))
        if states == Game.WIN_STATES:
            return

        self._guessed_words.add(guess)
        self._possible_solutions = [possible_solution for possible_solution in self._possible_solutions if Game.is_same_response(guess, possible_solution, states)]
