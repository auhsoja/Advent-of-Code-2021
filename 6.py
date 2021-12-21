import requests

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text, days):
    initial_states = [int(k) for k in text.split(',')]

    totals = [0 for i in range(9)]
    for s in initial_states:
        totals[s] += 1

    for _ in range(days):
        new = [0 for i in range(9)]
        new[6] += totals[0]
        new[8] += totals[0]
        for i in range(1, 9):
            new[i - 1] += totals[i]

        totals = new

    print(sum(totals))


test = "3,4,3,1,2"
solve(test, 256)

text = get_day(6)
solve(text[0], 256)
