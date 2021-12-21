import requests
import math
import sys

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    '''
    Solve part 1 using Bellman-Ford. This is not fast enough for part 2. See 15_2.py for
    an implementation using Dijkstra's that's sufficient for both parts.
    '''
    M = len(text)
    N = len(text[0])
    costs = []
    for line in text:
        costs.append([int(k) for k in line])

    dist = [1e9 for i in range(M*N)]
    dist[0] = 0
    edges = []

    for i in range(M):
        for j in range(N):
            # For each neighbor, the cost is the value at the neighbor's cell
            if j < N-1:
                edges.append((i*N+j, i*N+j+1, costs[i][j+1]))
            if j > 0:
                edges.append((i*N+j, i*N+j-1, costs[i][j-1]))
            if i > 0:
                edges.append((i*N+j, (i-1)*N+j, costs[i-1][j]))
            if i < M-1:
                edges.append((i*N+j, (i+1)*N+j, costs[i+1][j]))

    while True:
        upd = False
        for (a, b, cost) in edges:
            if dist[a] < 1e9:
                if dist[b] > dist[a] + cost:
                    dist[b] = dist[a] + cost
                    upd = True

        if not upd:
            break
    print(dist[-1])


test = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split("\n")

solve(test)

#sys.exit()

text = get_day(15)
solve(text)
