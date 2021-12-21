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


def parse(s):
    stack = []
    nums = "0123456789"
    for c in s:
        if c in nums:
            stack.append(Tree(int(c)))

        elif c == ']':
            r = stack.pop()
            l = stack.pop()
            new = Tree(None)
            new.left = l
            new.right = r
            l.p = new
            r.p = new
            stack.append(new)

    return stack[0]


def red(t):
    while True:
        if explode(t):
            continue
        if split(t):
            continue

        break

    return t


def search(t, d=0):
    if t == None:
        return None

    if t.left is not None:
        f = search(t.left, d+1)
        if f is not None:
            return f

    if t.value is not None and d >= 5:
        return t

    if t.right is not None:
        f = search(t.right, d+1)
        if f is not None:
            return f

    return None


def search_split(t):
    if t == None:
        return None

    if t.left is not None:
        f = search_split(t.left)
        if f is not None:
            return f

    if t.value is not None and t.value >= 10:
        return t

    if t.right is not None:
        f = search_split(t.right)
        if f is not None:
            return f

    return None


def leftmost(t):
    curr = t
    while curr.left != None:
        curr = curr.left

    return curr


def rightmost(t):
    curr = t
    while curr.right != None:
        curr = curr.right

    return curr


def rsib(t):
    # Find leftmost to the right if exists
    curr = t.p
    prev = t

    while True:
        if curr is None:
            return None
        if prev is curr.right:
            curr, prev = curr.p, prev.p
        else:
            break

    # Now curr holds something to right of t
    return leftmost(curr.right)



def lsib(t):
    # Find rightmost to the left if exists
    curr = t.p
    prev = t

    while True:
        if curr is None:
            return None
        if prev is curr.left:
            curr, prev = curr.p, prev.p
        else:
            break

    # Now curr holds something to left of t
    return rightmost(curr.left)



def explode(t):
    deep = search(t)
    if deep is None:
        return False

    deep = deep.p

    l = lsib(deep)
    r = rsib(deep)

    if l is not None:
        l.value += deep.left.value
    if r is not None:
        r.value += deep.right.value

    deep.right = None
    deep.left = None
    deep.value = 0
    return True


def split(t):
    deep = search_split(t)

    if deep is None:
        return False

    l = Tree(deep.value // 2)
    l.p = deep

    r = Tree(deep.value // 2 + deep.value % 2)
    r.p = deep

    deep.left = l
    deep.right = r
    deep.value = None
    return True


def solve(text):
    curr = None
    for line in text:
        t = parse(line)
        if curr is None:
            curr = red(t)

        else:
            new = Tree(None)
            new.left = curr
            new.right = t
            curr.p = new
            t.p = new
            curr = red(new)

    print(mag(curr))


def solve2(text):
    opts = []
    best = 0
    curr = Tree(None)
    for line in text:
        t = parse(line)
        opts.append(t)

    for i in range(len(opts)):
        for j in range(len(opts)):
            if i == j:
                continue

            l = opts[i].copy()
            r = opts[j].copy()
            curr.left = l
            curr.right = r
            l.p = curr
            r.p = curr
            curr = red(curr)
            m = mag(curr)
            if m > best:
                best = m
                print(l)
                print(r)

            curr = Tree(None)

    print(best)


def mag(t):
    if t.value is not None:
        return t.value

    return mag(t.left)*3+mag(t.right)*2



test = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".split("\n")

test = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split("\n")
solve2(test)


#sys.exit()

text = get_day(18)
solve2(text)
