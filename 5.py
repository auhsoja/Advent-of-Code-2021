import requests
import numpy as np

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"


def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')

def sort_key(pt):
    x, y, orientation = pt

    return 2 * x + (1 if orientation == 'H' else 0)


def solve(text):
    pts = []
    for row in text:
        ps = row.split(' -> ')
        p1, p2 = [tuple(int(k) for k in pt.split(',')) for pt in ps]

        if p1[0] == p2[0]:
            # Vertical line
            pts.append(p1+("V"))
            pts.append(p2+("V"))

        else:
            # Horizontal line
            pts.append(p1+("H"))
            pts.append(p2+("H"))

    # Sort the points by x-coordinate, and break ties processing verticals first
    pts.sort(key=sort_key)

    # Sweep over x. For vertical, count intersections. For horizontal, add or remove
    horizontal_heights = {}
    intersections = 0

    for pt in pts:
        x, y, orientation = pt

        if orientation == "V":
            pass

# Note that the grid is 1000x1000, so we can actually construct it
def solve2(text):
    grid = np.zeros((1000, 1000), dtype=np.uint8)
    for row in text:
        ps = row.split(' -> ')
        (x1, y1), (x2, y2) = [tuple(int(k) for k in pt.split(',')) for pt in ps]

        # Handle axis-aligned
        if x1 == x2 or y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            grid[x1:x2+1, y1:y2+1] += 1

        # Handle diagonal
        elif abs(x2-x1) == abs(y2-y1):
            stepx = 1 if x2 >= x1 else -1
            stepy = 1 if y2 >= y1 else -1
            xs = np.arange(x1, x2+stepx, stepx)
            ys = np.arange(y1, y2+stepy, stepy)
            grid[xs, ys] += 1


    print(grid[:10, :10].T)
    print((grid > 1).sum())

test = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split('\n')

solve2(test)
text = get_day(5)
solve2(text)
