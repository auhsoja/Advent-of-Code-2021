import sys
import numpy as np
import itertools
from utils import *
import math

def intersection(cube1, cube2):
    xb1, yb1, zb1 = cube1
    xb2, yb2, zb2 = cube2
    for a, b in zip(cube1, cube2):
        if a[0] > b[1] or a[1] < b[0]:
            return None

    return tuple((max(a[0], b[0]), min(a[1], b[1])) for a, b in zip(cube1, cube2))

def difference(cube1, cube2):
    int = intersection(cube1, cube2)
    if not int:
        return [cube1]

    # If the cube was intersected, generate the 6 resultant subcubes
    new_cubes = []
    new_cubes.append((cube1[0], cube1[1], (cube1[2][0], int[2][0] - 1)))
    new_cubes.append((cube1[0], cube1[1], (int[2][1] + 1, cube1[2][1])))
    new_cubes.append(((cube1[0][0], int[0][0] - 1), cube1[1], int[2]))
    new_cubes.append(((int[0][1] + 1, cube1[0][1]), cube1[1], int[2]))
    new_cubes.append((int[0], (cube1[1][0], int[1][0] - 1), int[2]))
    new_cubes.append((int[0], (int[1][1] + 1, cube1[1][1]), int[2]))

    return [(x, y, z) for x, y, z in new_cubes if x[0] <= x[1] and y[0] <= y[1] and z[0] <= z[1]]


def solve(text):
    # For small example, can just make the whole array. No segtree needed.
    grid = np.zeros((101, 101, 101))

    LOW = -50

    for line in text:
        on, ranges = line.split()
        on = int("on" in on)
        ranges = ranges.split(",")
        ranges = [x[2:] for x in ranges]
        ranges = [[int(k)-LOW for k in r.split("..")] for r in ranges]
        (x1, x2), (y1, y2), (z1, z2) = ranges

        for (a, b) in ranges:
            if abs(a+LOW) > 50 or abs(b+LOW) > 50:
                continue

        grid[x1:x2+1, y1:y2+1, z1:z2+1] = on

    print(grid.sum())


def solve2(text):
    cubes = []
    for line in text:
        on, ranges = line.split()
        on = int("on" in on)
        ranges = ranges.split(",")
        ranges = [x[2:] for x in ranges]
        ranges = [[int(k) for k in r.split("..")] for r in ranges]

        this_cube = ranges
        new_cubes = []
        for cube in cubes:
            new_cubes.extend(difference(cube, this_cube))
        if on:
            new_cubes.append(this_cube)
        cubes = new_cubes

    tot = 0
    for cube in cubes:
        tot += math.prod(cube[i][1] - cube[i][0] + 1 for i in range(3))

    print(tot)

test = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".split("\n")

#test = """on x=10..12,y=10..12,z=10..12
#on x=11..13,y=11..13,z=11..13
#off x=9..11,y=9..11,z=9..11
#on x=10..10,y=10..10,z=10..10""".split("\n")

solve(test)
solve2(test)

#sys.exit()

text = get_day(22)
solve(text)
solve2(text)
