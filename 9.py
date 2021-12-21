import requests
import numpy as np

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    arr = np.zeros((len(text), len(text[0])))
    basins = []
    for i, line in enumerate(text):
        arr[i, :] = [int(k) for k in line]

    padded = np.pad(arr, ((1, 1), (1, 1)), 'constant', constant_values=(100, 100))
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            i2 = i+1
            j2 = j+1
            i_shift = (1, -1, 0, 0)
            j_shift = (0, 0, 1, -1)
            neighbors = [padded[i2+x, j2+y] for (x, y) in zip(i_shift, j_shift)]
            if padded[i2, j2] < min(neighbors):
                basins.append((i2, j2))

    sizes = []
    i_shift = (1, -1, 0, 0)
    j_shift = (0, 0, 1, -1)
    for basin in basins:
        if basin == (3, 3):
            log=True
        else:
            log=False
        visited = set([basin])
        in_base = set()
        to_visit = [basin]
        while len(to_visit) != 0:
            curr = to_visit.pop(0)
            ic, jc = curr
            # need all smaller neighbors to be in basin to be in basin
            neigh = [(ic+x, jc+y) for (x, y) in zip(i_shift, j_shift)]
            low_neigh = [nb for nb in neigh if padded[nb] < padded[curr]]
            bad = [nb for nb in low_neigh if nb not in in_base]
            if len(bad) == 0:
                # This point is in the basin. Add and explore
                in_base.add(curr)
                for p in neigh:
                    if p not in in_base and padded[p] < 9:
                        visited.add(p)
                        to_visit.append(p)
        if log:
            print(sorted(list(in_base)))
        sizes.append(len(in_base))

    a,b,c = sorted(sizes)[-3:]
    print(a,b,c)
    print(a*b*c)


test = """2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n")

solve(test)

text = get_day(9)
solve(text)
