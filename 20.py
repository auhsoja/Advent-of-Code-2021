import sys
import numpy as np
import itertools
from utils import *


def plot(pts):
    lo_i = min(pts.keys())
    hi_i = max(pts.keys())

    lo_j = 0
    hi_j = 0

    for d in pts.values():
        k = d.keys()
        if min(k) < lo_j:
            lo_j = min(k)
        if max(k) > hi_j:
            hi_j = max(k)


    board = [['.' for j in range(hi_j-lo_j+1)] for i in range(hi_i-lo_i+1)]
    for i, d in pts.items():
        for j, v in d.items():
            if v:
                board[i-lo_i][j-lo_j] = '#'

    out = []
    for l in board:
        out.append(''.join(l))

    print("\n".join(out))
    print("\n\n")


def new_val(i, j, code, pts, s):
    out = ''
    for ii in range(-1, 2):
        for jj in range(-1, 2):
            if i+ii in pts and j+jj in pts[i+ii]:
                out += str(pts[i+ii][j+jj])

            else:
                # We have to do this stupidity because they added
                # the rule to make uncharted territory oscillate
                out += str(s%2)

    idx = int(out, 2)
    return 1 if code[idx] == "#" else 0


def solve(text, steps):
    print(text[0], "\n",text[1],"\n", text[2],"\n", text[3])
    code = text[0]
    text = text[2:]

    pts = defaultdict(dict)
    for i, line in enumerate(text):
        for j, c in enumerate(line):
            val = 1 if c == '#' else 0
            pts[i][j] = val

    lo_i = 0
    hi_i = len(text) - 1
    lo_j = 0
    hi_j = len(text[0]) - 1

    for s in range(steps):
        lo_i -= 1
        hi_i += 1
        lo_j -= 1
        hi_j += 1

        updates = []
        for i,j in itertools.product(range(lo_i, hi_i+1), range(lo_j, hi_j+1)):
            new_v = new_val(i, j, code, pts, s)
            updates.append((i,j,new_v))

        for i,j,new_v in updates:
            if i not in pts:
                pts[i][j] = 0
            if j not in pts[i]:
                pts[i][j] = 0

            pts[i][j] = new_v

    lit = 0
    for i, d in pts.items():
        for j, v in d.items():
            lit += v

    print(lit)


test = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".split("\n")

#solve(test, 2)

#sys.exit()

text = get_day(20)
solve(text, 50)
