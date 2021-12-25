import sys
import numpy as np
import itertools
from utils import *


def next_p(i, j, M, N, east):
    if east:
        return (i, (j+1) % N)
    else:
        return ((i+1) % M, j)


def blockers(i, j, M, N):
    # If a sea cuc moves, the only
    # people that might get freed to move
    # are above and left
    return ((i-1) % M, j), (i, (j-1) % N)


def print_board(locs):
    for line in locs:
        print(''.join(line))

    print()


def solve(text):
    M = len(text)
    N = len(text[0])
    locs = [['.' for j in range(N)] for i in range(M)]
    movers = set()

    for i, line in enumerate(text):
        for j, c in enumerate(line):
            if c != '.':
                locs[i][j] = c
                if c == '>':
                    movers.add((i, j, True))
                else:
                    movers.add((i, j, False))

    steps = 0
    while len(movers) > 0:
        steps += 1
        # print_board(locs)
        # Tells us if it's east turn or south turn
        for b in range(2):
            updates = []
            adds = []
            rems = []
            for i, j, east in movers:
                if east == bool(b):
                    continue

                i2, j2 = next_p(i, j, M, N, east)
                if locs[i2][j2] != '.':
                    rems.append((i, j, east))
                    continue

                c = '>' if east else 'v'
                updates.append((i, j, c, i2, j2))

                (upi, upj), (lefti, leftj) = blockers(i, j, M, N)
                if locs[upi][upj] == 'v':
                    adds.append((upi, upj, False))
                if locs[lefti][leftj] == '>':
                    adds.append((lefti, leftj, True))

            for (i1, j1, c, i2, j2) in updates:
                adds.append((i2, j2, c == '>'))
                rems.append((i, j, c == '>'))
                locs[i1][j1] = '.'
                locs[i2][j2] = c

            movers -= set(rems)
            movers |= set(adds)

    print(steps)


test = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".split("\n")

solve(test)

# sys.exit()

text = get_day(25)
solve(text)
