import requests
import math
import sys
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

def rd(n):
    # 10 -> 1. 19->1. 28->1. 37->1
    if n >= 37:
        return n-36
    if n >= 28:
        return n-27
    if n >= 19:
        return n-18
    if n>= 10:
        return n-9
    return n


def solve(text):
    M = len(text)
    N = len(text[0])
    costs = []
    for line in text:
        costs.append([int(k) for k in line])

    dist = [1e9 for i in range(M*N)]
    dist[0] = 0
    edges = []

    ROW = N*5
    for k in range(5):
        for l in range(5):
            for i in range(M):
                for j in range(N):
                    # For each neighbor, the cost is the value at the neighbor's cell
                    curr = k*ROW*M + i*ROW + l*N+j

                    if j > 0:
                        edges.append((curr, curr-1, rd(costs[i][j-1]+k+l)))
                    elif j == 0 and l > 0:
                        edges.append((curr, curr-1, rd(costs[i][-1]+k+l-1)))

                    if j < N-1:
                        edges.append((curr, curr+1, rd(costs[i][j+1]+k+l)))
                    elif j == N-1 and l < 4:
                        edges.append((curr, curr+1, rd(costs[i][0]+k+l+1)))

                    if i > 0:
                        edges.append((curr, curr-ROW, rd(costs[i-1][j]+k+l)))
                    elif i == 0 and k > 0:
                        edges.append((curr, curr-ROW, rd(costs[-1][j]+k+l-1)))

                    if i < M-1:
                        edges.append((curr, curr+ROW, rd(costs[i+1][j]+k+l)))
                    elif i == M-1 and k < 4:
                        edges.append((curr, curr+ROW, rd(costs[0][j]+k+l+1)))


    print(bin_heap_dijkstras(edges, 0, 25*M*N-1))


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


text = get_day(15)
solve(text)
