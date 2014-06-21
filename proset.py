from functools import reduce
from itertools import compress
from random import shuffle


class Deck:
    def __init__(self, numDots):
        stock = list(range(1, 2**numDots))
        shuffle(stock)
        upcards = [stock.pop() for _ in range(numDots + 1)]
        self.stock = stock
        self.upcards = upcards

    def cardsRemaining(self):
        return len(self.stock) + len(self.upcards)

    def isEmpty(self):
        return len(self.upcards) == 0

    def remove(self, selectors):
        cards = list(compress(enumerate(self.upcards), selectors))
        if reduce(lambda a, b: a^b,
                  (c for i, c in cards)) == 0:
            for selectedIndex in (i for i, c in cards):
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
