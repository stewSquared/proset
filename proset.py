from functools import reduce
from itertools import compress
from random import shuffle
import os

NUM_DOTS = 4

class Deck:
    def __init__(self, numDots):
        stock = list(range(1, 2**numDots)); shuffle(stock)
        upcards = []
        for _ in range(numDots + 1): upcards.append(stock.pop())
        self.stock = stock
        self.upcards = upcards

    def cardsRemaining(self):
        return len(self.stock) + len(self.upcards)
    
    def isEmpty(self):
        return len(self.stock) + len(self.upcards) == 0

    def remove(self, selectors):
        cards = list(compress(enumerate(self.upcards), selectors))
        if reduce(lambda a, b: a^b,
                  (c for i,c in cards)) == 0:
            for selectedIndex in (i for i,c in cards):
                print(selectedIndex)
                try:
                    newCard = self.stock.pop()
                except IndexError:
                    newCard = 0
                self.upcards[selectedIndex] = newCard
            self.upcards = list(filter(None, self.upcards))
            return True
        else:
            return False

def newGame():
    deck = Deck(NUM_DOTS)
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

def chooseFrom(cards):
    def cardDisplay(card):
        return bin(card)[2:].zfill(NUM_DOTS).replace('0','---').replace('1','<O>')

    for count, card in enumerate(cards):
        print("{} : {}".format(count+1, cardDisplay(card)))
    
    chosen = [int(i) for i in
              input("\nChoose cards by entering numbers: ").split()]
    while(not all(1 <= i <= len(cards) for i in chosen)):
        chosen = [int(i) for i in
                  input("\nOut of range. Try again: ").split()]

    selectors = [(i+1) in chosen for i in range(len(cards))]
    return selectors

if __name__ == '__main__': newGame()
