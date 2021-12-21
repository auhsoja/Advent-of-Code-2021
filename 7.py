import requests
import numpy as np

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    vals = np.array([int(k) for k in text.split(',')])
    m = vals.mean()
    best1 = np.ceil(m)
    best2 = np.floor(m)

    loss1 = (vals - best1)**2 + abs(vals - best1)
    loss1 = loss1.sum() / 2

    loss2 = (vals - best2)**2 + abs(vals - best2)
    loss2 = loss2.sum() / 2

    print(min(loss1, loss2))


test = "16,1,2,0,4,2,7,1,2,14"
solve(test)

text = get_day(7)
solve(text[0])
