ProSET
======
Projective Set is the game of finding 2-dimensional subspaces in \mathbb{F}_2^6.

USAGE:

proset.py is a GUI version of the game. Cards are selected either by
clicking or typing 1-7. A maximum of six dots (seven cards) is
allowed. The number of dots (default 6) and resolution (default
1024x768) can be adjusted via command line argument.

    python proset.py 
    OR python proset.py <num_dots>
    OR python proset.py <num_dots> <resolution_width> <resolution_height>

cli.py plays ProSET with a simple command line. An unlimited number of
dots are allowed this way.

Very few pygame apps are made with python 3 (yet), so it's not likely
that anyone will take the time to build the latest version of pygame
from the mecurial repository just to play this.

The next step is a scala/play-framework/HTML5 implementation that runs
persistently on a server and allows for an unspecified number of players
to drop in and procrastinate away.