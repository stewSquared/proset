from functools import reduce
from itertools import compress
from random import shuffle
import os

NUM_DOTS = 6

def newGame():
    deck = list(range(1, 2**NUM_DOTS)); shuffle(deck)
    table = []
    for _ in range(NUM_DOTS + 1): table.append(deck.pop())

    os.system("clear")
    print("\nWelcome to proset. {} cards remaining.\n".format(len(deck) +
                                                              len(table)))
    while len(table) + len(deck) > 0:
        cards = list(compress(enumerate(table), cliTurn(table)))
        if reduce(lambda a, b: a^b, 
                  (c for i,c in cards)) == 0:
            for selectedIndex in (i for i,c in cards):
                print(selectedIndex)
                try:
                    newCard = deck.pop()
                except IndexError:
                    newCard = 0
                table[selectedIndex] = newCard
            table = list(filter(None, table))

            os.system("clear")
            print("\nCorrect. {} cards remaining.\n".format(len(deck) +
                                                            len(table)))
        else:
            os.system("clear")
            print("\nBad guess. {} cards remaining.\n".format(len(deck) +
                                                               len(table)))

    print("Game complete. Thank you for playing.\n")

def cliTurn(cards):
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
