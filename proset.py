import sys
import pygame
import pygame.gfxdraw
from pygame.locals import *
from itertools import product, compress
from functools import reduce
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
        if selectors.count(True) < 3: return False

        cards = list(compress(enumerate(self.upcards), selectors))
        if reduce(lambda a, b: a^b,
                  (c for i, c in cards)) == 0:
            for selectedIndex in (i for i, c in cards):
                try:
                    newCard = self.stock.pop()
                except IndexError:
                    newCard = 0
                self.upcards[selectedIndex] = newCard
            self.upcards = list(filter(None, self.upcards))
            return True
        else:
            return False


class Card:
    col_ratios = 3/10, 7/10
    row_ratios = 3/14, 7/14, 11/14
    colors = tuple("red, yellow, dark blue, orange, green, magenta"
                   .split(", "))

    def __init__(self, value, rect):
        self.value = value
        self._rect = rect.copy()
        self.big_rect = rect.inflate(*(_//6 for _ in rect.size))
        self.selected = False

    @property
    def rect(self):
        return self.big_rect if self.selected else self._rect

    @property
    def centers(self):
        width, height = self.rect.size
        return tuple((int(x*width), int(y*height))
                     for x, y in product(self.col_ratios, self.row_ratios))

    def flip(self):
        self.selected = not self.selected

    def render(self):
        width, height = self.rect.size
        colors = self.colors
        centers = self.centers
        radius = width//8
        num_dots = 6

        card = pygame.Surface(self.rect.size)
        card.fill(Color("white"))
        pygame.draw.rect(card, Color("black"), card.get_rect(), 1)

        selectors = (bool(int(c)) for c in bin(self.value)[2:].zfill(num_dots))
        for (center, color) in compress(zip(self.centers, self.colors),
                                        selectors):
            x, y = center
            pygame.gfxdraw.aacircle(card, x, y, radius, Color(color))
            pygame.gfxdraw.filled_circle(card, x, y, radius, Color(color))
            # In case gfxdraw breaks, use this:
            # pygame.draw.circle(card, Color(color), center, RADIUS)
        return card


def card_rects(size):
    width, height = size
    table = pygame.Surface(size)
    bgcolor = Color("dark green")
    table.fill(bgcolor)

    card_width = width / 7
    card_height = card_width * 7 / 5
    card_size = card_width, card_height
    card_gap = card_width / 4

    fst_row_x = (width - card_width*4 - card_gap*3)//2
    fst_row_y = (height - card_height*2 - card_gap)//2
    snd_row_x = (width - card_width*3 - card_gap*2)//2
    snd_row_y = (height + card_gap)//2

    positions = [((fst_row_x + n*(card_gap + card_width)), fst_row_y)
                 for n in range(4)]
    positions.extend(((snd_row_x + n*(card_gap + card_width)), snd_row_y)
                     for n in range(3))

    return (Rect(pos, card_size) for pos in positions)


def new_game(num_dots, size):
    screen = pygame.display.set_mode(size)
    bgcolor = Color("dark green")
    deck = Deck(num_dots)

    def evaluate():
        nonlocal cards, chosen
        selection = [i in chosen for i in range(len(deck.upcards))]
        if deck.remove(selection):
            chosen = []
            cards = [Card(val, rect) for val, rect in
                     zip(deck.upcards, card_rects(size))]
            show_cards()

    def select(card_index):
        if card_index >= len(cards): return

        if card_index in chosen:
            chosen.remove(card_index)
        else:
            chosen.append(card_index)
        cards[card_index].flip()
        show_cards()

    def show_cards():
        screen.fill(bgcolor)
        for card in cards:
            screen.blit(card.render(), card.rect)
        pygame.display.flip()

    chosen = []
    cards = [Card(val, rect) for val, rect in
             zip(deck.upcards, card_rects(size))]
    show_cards()

    while not deck.isEmpty():
        for event in pygame.event.get():
            if event.type is KEYDOWN:
                if event.key == K_SPACE:
                    evaluate()
                elif event.unicode.isdigit():
                    select(int(event.unicode)-1)
                elif event.key == K_ESCAPE:
                    chosen = []
                    show_cards()
            elif event.type is QUIT:
                sys.exit()


if __name__ == '__main__':
    numDots = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    try:
        size = (tuple(map(int, sys.argv[2:4]))
                if len(sys.argv) > 3 else (1024, 768))
    except ValueError:
        size = (1024, 768)
    # view module renders only up to six dots on a card
    # This is prevented here, but not tested anywhere else!
    numDots = min(numDots, 6)
    new_game(numDots, size)
