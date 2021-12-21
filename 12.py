import requests
import sys

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def find_paths(curr_v, start, terminal, visited, edges, id_big, count, small):
    # Mark visited if small. Then explore each neighbor
    if not id_big[curr_v]:
        visited.add(curr_v)

    # Explore the neigbors
    for nb in edges[curr_v]:
        if nb == terminal:
            if len(small) == 0:
                count[0] += 1
            elif small[0] in visited:
                count[0] += 1

            # If we never revisited a small guy,
            # then we did not gain any new paths by allowing revisits
        elif nb not in visited:
            find_paths(nb, start, terminal, visited, edges, id_big, count, small)

    # Finish with this vertex
    if curr_v in visited:
        visited.remove(curr_v)

    # Repeat the procedure allowing the curr vertex to be revisited
    if not id_big[curr_v] and len(small) == 0 and curr_v != start:
        pass
    else:
        return

    small.append(curr_v)

    # Explore the neigbors
    for nb in edges[curr_v]:
        if nb == terminal:
            # This cannot add a new path
            pass

        elif nb not in visited:
            find_paths(nb, start, terminal, visited, edges, id_big, count, small)

    small.pop()


def solve(text):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    big = set(alpha)
    small = set(alpha.lower())

    # DFS
    vertices = set()
    str_to_id = {}
    id_to_str = []
    id_to_is_big = []
    edges = []
    paths = [0]
    small = []
    visited = set()

    for line in text:
        (a, b) = line.split("-")
        for v in (a, b):
            if v not in vertices:
                vertices.add(v)
                str_to_id[v] = len(id_to_str)
                id_to_str.append(v)
                id_to_is_big.append(set(v) <= big)
                edges.append([])

        edges[str_to_id[a]].append(str_to_id[b])
        edges[str_to_id[b]].append(str_to_id[a])

    find_paths(str_to_id['start'], str_to_id['start'], str_to_id['end'], visited, edges, id_to_is_big, paths, small)
    print(paths[0])


test = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n")

solve(test)

test = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split("\n")

solve(test)


text = get_day(12)
solve(text)
