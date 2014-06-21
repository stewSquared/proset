import os
import sys
import pygame
pygame.init()
from proset import Deck
from view import tableGenerator


def newGame(numDots, size):
    screen = pygame.display.set_mode(size)
    render = tableGenerator(size)
    deck = Deck(numDots)

    def chooseFrom(cards):
        screen.blit(render(cards), (0, 0))
        pygame.display.flip()

        chosen = [int(i) for i in
                  input("\nChoose cards by entering numbers: ").split()]
        while(not all(1 <= i <= len(cards) for i in chosen)):
            chosen = [int(i) for i in
                      input("\nOut of range. Try again: ").split()]

        selectors = [(i+1) in chosen for i in range(len(cards))]
        return selectors

    os.system("clear")
    print("\nWelcome to proset. {} cards remaining.\n"
          .format(deck.cardsRemaining()))

    while not deck.isEmpty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

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
    try:
        numDots = int(sys.argv[1]) if len(sys.argv) > 1 else 4
        size = (tuple(map(int, sys.argv[2:4]))
                if len(sys.argv) > 3 else (1024, 768))
    except ValueError:
        numDots = 4
        size = (1024, 768)
    # view module renders only up to six dots on a card
    # This is prevented here, but not tested anywhere else!
    numDots = min(numDots, 6)
    newGame(numDots, size)
