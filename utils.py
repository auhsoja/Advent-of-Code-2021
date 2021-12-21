import requests
import math
from collections import defaultdict
import heapq

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def bin_heap_dijkstras(times, x, y):

    graph = defaultdict(dict)

    for src, dest, cost in times:
        graph[src][dest] = cost

    distance_costs = {i: float("inf") for i in range(len(graph.keys()))}
    distance_costs[x] = 0
    min_dist = [(0,x)]
    visited = set()

    while min_dist:

        current_dist, current = heapq.heappop(min_dist)
        if current in visited:
            continue
        visited.add(current)

        for neighbour in graph[current]:
            if neighbour in visited:
                continue
            checking_dist = current_dist + graph[current][neighbour]
            if checking_dist < distance_costs[neighbour]:
                distance_costs[neighbour] = checking_dist
                heapq.heappush(min_dist, (checking_dist, neighbour))

    if len(visited) != len(distance_costs):
        return -1
    return distance_costs[y]


def neighbors(i, j, M, N):
    out = []
    if i > 0:
        out.append((i-1, j))
    if i < M-1:
        out.append((i+1, j))
    if j > 0:
        out.append((i, j-1))
    if j < N-1:
        out.append((i, j+1))

    return out


class Tree():
    def __init__(self, v):
        self.value = v
        self.left = None
        self.right = None
        self.p = None

    def __str__(self):
        if self.value is not None:
            return str(self.value)

        l = str(self.left)
        r = str(self.right)

        return f"[{l},{r}]"

    def copy(self):
        if self.value is not None:
            return Tree(self.value)

        out = Tree(None)
        l = self.left.copy()
        r = self.right.copy()
        l.p = out
        r.p = out
        out.left = l
        out.right = r
        return out


