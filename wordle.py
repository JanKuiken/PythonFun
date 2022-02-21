#!/usr/bin/env python3
"""
Wordle/Lingo programmaatje in Python

nav.: https://www.youtube.com/watch?v=v68zYyaEmEA
      "Solving Wordle using information theory"

Eerst even zonder 'information theory' maar gewoon eens kijken of we zelf
iets slims kunnen verzinnen, we gaan verschillende methodes proberen...

oh ja we gaan wel nederlandse woorden gebruiken, bestand /usr/share/dict/nederlands moet bestaan

Bronnen:
  - Bovenstaande youtube video
  - https://www.nytimes.com/games/wordle/index.html
  - https://nl.wikipedia.org/wiki/Lingo
  - Wat eigen verzinsels:
    - We zijn mild, niet bestaande woorden die je invoert worden genegeerd.
    - Lege invoer (je tiept alleen <enter>) verwijdert je laatste invoer.
    - Tig keer <enter> resulteert in een nieuw woord om te raden.
    - 's173' is de 'secret key' en laat het te raden woord zien.
    - '?' laat deze uitleg nog een keer dit zien... 
  - \u001b[48;5;241m\u001b[30m a \u001b[0m geeft een letter weer die niet voorkomt in het te raden woord
  - \u001b[48;5;142m\u001b[30m a \u001b[0m is een letter weer die voorkomt in het te raden woord maar niet op de juiste plaats staat 
  - \u001b[48;5;28m\u001b[30m a \u001b[0m is een letter weer die voorkomt en op de juiste plaats staat 
  - ... en verder zoek je het maar uit.
"""
from string import ascii_lowercase
import random

DEBUG = True

DEFAULT_WORDS_FILE   = '/usr/share/dict/nederlands'
DEFAULT_WORD_LENGTH  = 5
DEFAULT_MAX_GUESSES  = 6

NOT_YET_USED         = 100
NOT_IN_WORD          = 101
IN_WORD_IN_PLACE     = 102
IN_WORD_NOT_IN_PLACE = 103

WORDS                = None   # will be filled by init_words

def init_words():
    global WORDS, WORDS_SET
    WORDS = []
    set_ascii_lowercase = set(ascii_lowercase)
    with open(DEFAULT_WORDS_FILE) as f:
        for line in f.readlines():
            word = line.strip() # remove trailing \n
            if len(word) == DEFAULT_WORD_LENGTH:
                set_word = set(word)
                # ignore non lower case ascii
                if set_word.issubset(set_ascii_lowercase): 
                    WORDS.append(word)

init_words() # fill WORDS


class Wordle():

    def __init__(self):
    
        self._secret_word = random.choice(WORDS)
        self.guesses      = [None] * DEFAULT_MAX_GUESSES 
        self.results      = [None] * DEFAULT_MAX_GUESSES
        for no in range(DEFAULT_MAX_GUESSES):
            self._reset_guess(no)
        self.guess_no = 0

        self.print()

    def _reset_guess(self, no):
        self.guesses[no] = ' ' * DEFAULT_WORD_LENGTH 
        self.results[no] = [NOT_YET_USED] * DEFAULT_WORD_LENGTH            

    def _determine_results(self):
        test_word = list(self.guesses[self.guess_no])
        ref_word = list(self._secret_word)
        self.results[self.guess_no] = [NOT_IN_WORD] * DEFAULT_WORD_LENGTH
        for i in range(DEFAULT_WORD_LENGTH):
            if test_word[i] == ref_word[i]:
                self.results[self.guess_no][i] = IN_WORD_IN_PLACE
                test_word[i] = '+'
                ref_word[i] = '-'
        for i in range(DEFAULT_WORD_LENGTH):
            if test_word[i] in ref_word:
                self.results[self.guess_no][i] = IN_WORD_NOT_IN_PLACE
                ref_word.remove(test_word[i])

    def print(self):
        # to colour text and background, see:
        # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
        ascii_escape_colors = {
            NOT_YET_USED         : u'\u001b[48;5;238m\u001b[30m',
            NOT_IN_WORD          : u'\u001b[48;5;241m\u001b[30m',
            IN_WORD_IN_PLACE     : u'\u001b[48;5;28m\u001b[30m',
            IN_WORD_NOT_IN_PLACE : u'\u001b[48;5;142m\u001b[30m', 
        }
        ascii_escape_reset = u'\u001b[0m'
        for guess in range(DEFAULT_MAX_GUESSES):
            print('   ', end='')  # a little space as prefix
            for pos in range(DEFAULT_WORD_LENGTH):
                print(ascii_escape_colors[self.results[guess][pos]], end='')
                print(' ' + self.guesses[guess][pos] + ' ', end='')
                print(ascii_escape_reset, end='')
            print()
        print()

    def guess(self, guess):
        print('\n\n')
        if guess == "": # remove last entry, or change guessing word
            if self.guess_no > 0:
                self.guess_no -= 1
                print("\nDeleted guess '" + self.guesses[self.guess_no] + "'\n")
                self._reset_guess(self.guess_no)
            else:
                print("\nNew word selected\n")
                self._secret_word = random.choice(WORDS)
        elif guess == "s173":
            print("\nWord to look for : '" + self._secret_word + "'\n")
        elif guess == "?":
            print(__doc__)
        elif not guess in WORDS:
            print("\n'" + str(guess) +"' is not a valid word...\n")
        elif self.guess_no >= DEFAULT_MAX_GUESSES:
            print("\nNumbers of guesses exceeded...\n")
        else:
            self.guesses[self.guess_no] = guess
            self._determine_results()
            self.guess_no += 1

        # oke whe are done, let's print current situation...
        self.print()


def print_hint(guesses, results):
    """
    Eerste stap naar AI, kunnen we handige tips maken....
    """
    known      = ['_'] * DEFAULT_WORD_LENGTH
    required   = []
    possible   = [l for l in ascii_lowercase]
    impossible = []
    for guess, result in zip(guesses, results):
        for i, (ch, res) in enumerate(zip(guess, result)):
            if ch != '_':
                if res == NOT_IN_WORD:
                    if ch in possible:
                        possible.remove(ch)
                        impossible.append(ch)
                elif res == IN_WORD_NOT_IN_PLACE:
                    if not ch in required:
                        required.append(ch)
                    if ch in possible:
                        possible.remove(ch)
                elif res == IN_WORD_IN_PLACE:
                    required.append(ch)
                    known[i] = ch
    print('      known :', ' '.join(known))
    print('   required :', ' '.join(required))
    print('   possible :', ' '.join(possible))
    print(' impossible :', ' '.join(impossible))
    print()

def main():
    print(__doc__)
    w = Wordle()
    while True:
        guess = input('Make a guess : ')
        w.guess(guess)
        print_hint(w.guesses, w.results)

if __name__ == '__main__':
     main()

