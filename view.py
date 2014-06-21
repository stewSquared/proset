import sys
import pygame
import pygame.gfxdraw
from pygame.locals import *
from itertools import product, compress, zip_longest


def cardGenerator(size):
    width, height = size
    colRatios = 3/10, 7/10
    rowRatios = 3/14, 7/14, 11/14
    centers = [(int(x*width), int(y*height))
               for x, y in product(colRatios, rowRatios)]
    colors = "red, yellow, dark blue, orange, green, magenta".split(", ")
    numDots = min(len(centers), len(colors))
    radius = width//8

    def cardImage(n=2**numDots-1):
        card = pygame.Surface(size)
        card.fill(Color("white"))
        # pygame.draw.rect(card, Color("black"), card.get_rect(), 2)
        pygame.gfxdraw.rectangle(card, card.get_rect(), Color("black"))

        selectors = [bool(int(c)) for c in bin(n)[2:].zfill(numDots)]
        for (center, color) in compress(zip(centers, colors), selectors):
            x, y = center
            pygame.gfxdraw.aacircle(card, x, y, radius, Color(color))
            pygame.gfxdraw.filled_circle(card, x, y, radius, Color(color))
            # In case gfxdraw breaks, use this:
            # pygame.draw.circle(card, Color(color), center, RADIUS)
        return card

    return cardImage


def tableGenerator(size):
    width, height = size
    table = pygame.Surface(size)
    bgcolor = Color("dark green")
    table.fill(bgcolor)

    cardWidth = width / 7
    cardHeight = cardWidth * 7 / 5
    cardGap = cardWidth / 4
    cardGen = cardGenerator((int(cardWidth), int(cardHeight)))

    fstRowX = (width - cardWidth*4 - cardGap*3)//2
    fstRowY = (height - cardHeight*2 - cardGap)//2
    sndRowX = (width - cardWidth*3 - cardGap*2)//2
    sndRowY = (height + cardGap)//2

    positions = [((fstRowX + n*(cardGap + cardWidth)), fstRowY)
                 for n in range(4)]
    positions.extend(((sndRowX + n*(cardGap + cardWidth)), sndRowY)
                     for n in range(3))

    def tableImage(cardNums):
        for n, p in zip_longest(cardNums, positions):
            if n is not None:
                table.blit(cardGen(n), p)
            else:
                # table.blit(cardGen(0), p)
                table.fill(bgcolor, cardGen().get_rect().move(p))
        return table

    return tableImage


if __name__ == '__main__':  # A demo!
    from random import random as r
    size = (1440, 900)
    screen = pygame.display.set_mode(size)
    show = tableGenerator(size)
    cardVals = (int(r()*63+1) for _ in range(7))

    screen.blit(show(cardVals), (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
