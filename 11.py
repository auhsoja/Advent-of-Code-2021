import requests
import numpy as np
import sys

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

class Bug():
    def __init__(self, i, j):
        self.pt = (i,j)

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text, days):
    arr = np.zeros((10, 10), dtype=np.uint8)
    for i in range(10):
        arr[i, :] = np.array([int(k) for k in text[i]])

    arr += days
    pad = np.pad(arr, ((1, 1), (1, 1)))
    flashes = 0
    while True:
        for i in range(1, 11):
            for j in range(1, 11):
                flash = pad[i, j] // 10
                res = pad[i, j] % 10
                flashes += flash
                pad[i, j] = res
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if ii == 0 and jj == 0:
                            continue

                        pad[i+ii, j+jj] += flash
        if (pad[1:-1, 1:-1] > 9).sum() == 0:
            print(pad[1:-1, 1:-1])
            break

    print(flashes)


def solve2(text, days):
    arr = np.zeros((10, 10), dtype=np.uint8)
    for i in range(10):
        arr[i, :] = np.array([int(k) for k in text[i]])

    flashes = 0
    for _ in range(days):
        arr += 1
        pad = np.pad(arr, ((1, 1), (1, 1)))
        flashes = 0
        while True:
            for i in range(1, 11):
                for j in range(1, 11):
                    flash = pad[i, j] // 10
                    res = pad[i, j] % 10
                    flashes += flash
                    pad[i, j] = res
                    for ii in range(-1, 2):
                        for jj in range(-1, 2):
                            if ii == 0 and jj == 0:
                                continue

                            pad[i+ii, j+jj] += flash
            if (pad[1:-1, 1:-1] > 9).sum() == 0:
                print(pad[1:-1, 1:-1])
                break

        print(flashes)


def dump(intensity_sets):
    for i, s in enumerate(intensity_sets):
        b = [bug.pt for bug in s]
        print(i, sorted(b))

def handle_flasher(bug, new_i_sets):
    for nb in bug.neighbors:
        for idx, s in enumerate(new_i_sets):
            if s is nb.set and idx < len(new_i_sets)-1:
                s.remove(nb)
                new_s = new_i_sets[idx+1]
                new_s.add(nb)
                nb.set = new_s
                if idx == len(new_i_sets) - 2:
                    handle_flasher(nb, new_i_sets)
                break


def solve3(text):
    N = len(text)
    bugs = [[Bug(i, j) for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            bugs[i][j].neighbors = []
            for ii in range(-1, 2):
                for jj in range(-1, 2):
                    if ii == 0 and jj == 0:
                        continue
                    if i + ii < 0 or i + ii >= N:
                        continue
                    if j + jj < 0 or j + jj >= N:
                        continue
                    bugs[i][j].neighbors.append(bugs[i+ii][j+jj])

    intensity_sets = [set() for i in range(11)]
    for i in range(N):
        line = [int(k) for k in text[i]]
        for j in range(N):
            intensity_sets[line[j]].add(bugs[i][j])
            bugs[i][j].set = intensity_sets[line[j]]


    day = 0
    while True:
        day += 1
        # First move everyone up
        new_i_sets = [set() for i in range(11)]
        for i in range(10):
            new_i_sets[i+1] = intensity_sets[i]


        # Then handle neighbors of flashers
        for bug in list(new_i_sets[10]):
            handle_flasher(bug, new_i_sets)


        # Then zero out flashers
        new_i_sets[0] = new_i_sets[10]
        new_i_sets[10] = set()
        intensity_sets = new_i_sets
        if len(intensity_sets[0]) == 100:
            print(day)
            break


test = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n")

solve3(test)

#sys.exit()

text = get_day(11)
solve3(text)
