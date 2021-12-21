import requests
import sys

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    pts = set()

    for line in text:
        if ',' in line:
            x, y = [int(k) for k in line.split(',')]
            pts.add((x,y))

        if 'fold' in line:
            trimmed = line.replace('fold along ', '')
            axis, val = trimmed.split('=')
            val = int(val)

            for pt in list(pts):
                x, y = pt

                if axis == 'x' and x > val:
                    pts.remove(pt)
                    x2 = 2*val - x
                    pts.add((x2, y))

                if axis == 'y' and y > val:
                    pts.remove(pt)
                    y2 = 2*val - y
                    pts.add((x, y2))

    # Make our grid by getting max x and y
    mx = max(pts)[0]
    my = max(pts, key=lambda x: x[1])[1]

    grid = [['.' for j in range(mx+1)] for i in range(my+1)]

    for pt in pts:
        x, y = pt
        grid[y][x] = '#'

    strings = [''.join(row) for row in grid]
    print('\n'.join(strings))


test = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split("\n")

solve(test)


text = get_day(13)
solve(text)
