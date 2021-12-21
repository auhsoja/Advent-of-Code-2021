import requests
import math
import sys

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text, steps):
    rules = {}
    start = text[0]

    for line in text[2:]:
        k, v = line.split(" -> ")
        rules[k] = v

    curr = start
    digraphs = {}
    for i in range(len(curr)-1):
        s = curr[i:i+2]

        if s in digraphs:
            digraphs[s] += 1
        else:
            digraphs[s] = 1

    for step in range(steps):
        dg_new = {}
        for ab, v in rules.items():
            if ab in digraphs:
                count = digraphs[ab]

                s1 = ab[0] + v
                s2 = v + ab[1]

                if s1 not in dg_new:
                    dg_new[s1] = 0
                if s2 not in dg_new:
                    dg_new[s2] = 0

                dg_new[s1] += count
                dg_new[s2] += count

        digraphs = dg_new


    cnts = {}
    for ab, cnt in digraphs.items():
        a, b = ab
        if a not in cnts:
            cnts[a] = 0
        if b not in cnts:
            cnts[b] = 0

        cnts[a] += cnt
        cnts[b] += cnt

    vals = []
    for a, cnt in cnts.items():
        vals.append(math.ceil(cnt / 2))

    print(max(vals) - min(vals))



test = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split("\n")

solve(test, 40)

#sys.exit()

text = get_day(14)
solve(text, 40)
