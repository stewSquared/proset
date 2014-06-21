import os
import sys
from proset import Deck


def newGame(numDots=6):
    def chooseFrom(cards):
        def cardDisplay(card):
            return (bin(card)[2:].zfill(numDots)
                    .replace('0', '---').replace('1', '<O>'))

        for count, card in enumerate(cards):
            print("{} : {}".format(count+1, cardDisplay(card)))

        chosen = [int(i) for i in
                  input("\nChoose cards by entering numbers: ").split()]
        while(not all(1 <= i <= len(cards) for i in chosen)):
            chosen = [int(i) for i in
                      input("\nOut of range. Try again: ").split()]

        selectors = [(i+1) in chosen for i in range(len(cards))]
        return selectors

    deck = Deck(numDots)
    os.system("clear")
    print("\nWelcome to proset. {} cards remaining.\n"
          .format(deck.cardsRemaining()))
    while not deck.isEmpty():
        selection = chooseFrom(deck.upcards)
        if deck.remove(selection):
            os.system("clear")
            print("\nCorrect. {} cards remaining.\n"
                  .format(deck.cardsRemaining()))
        else:
            os.system("clear")
            print("\nBad guess. {} cards remaining.\n"
                  .format(deck.cardsRemaining()))
    print("Game complete. Thank you for playing.\n")


if __name__ == '__main__':
    numDots = int(sys.argv[1]) if (len(sys.argv) > 1) else 6
    newGame(numDots)
