from functools import reduce
from random import shuffle
import os

def newGame():
    deck = list(range(1,64)); shuffle(deck)
    table = []

    os.system("clear")
    print("\nWelcome to proset. There are {} cards.\n".format(len(deck)))

    while len(table) + len(deck) > 0:
        while len(table) < 7 and len(deck) > 0:
            table.append(deck.pop())

        while True:
            guess = cliTurn(table)
            os.system("clear")
            if (reduce(lambda a, b: a^b, guess) == 0):
                for card in guess: table.remove(card)
                print("\nCorrect. {} cards remaining.\n".format(len(deck) +
                                                                len(table)))
                break
            else:
                print("\nBad guess.\n")
    print("Game complete. Thank you for playing.")

def cliTurn(cards):
    def cardDisplay(card):
        return bin(card)[2:].zfill(6).replace('0','---').replace('1','-O-')

    for count, card in enumerate(cards):
        print("{} : {}".format(count+1, cardDisplay(card)))
    
    chosen = [int(card)-1 for card in
              input("Choose cards by entering numbers: ").split()]

    while(not all(card in range(len(cards)) for card in chosen)):
        chosen = [int(card)-1 for card in
                  input("Bad input. Try again: ").split()]

    return set(cards[card] for card in chosen)

if __name__ == '__main__': newGame()
