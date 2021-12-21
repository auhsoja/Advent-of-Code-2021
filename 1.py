import requests

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"


def get_day(n: int):
    r = requests.get(
        f'https://adventofcode.com/2021/day/{n}/input',
        cookies={'session': cookie}
    )
    return r.text.strip()


text = get_day(1)
print(len(text.split('\n')))

arr = [int(x) for x in text.split('\n') if len(x) > 0]

a1 = iter(arr)
a2 = iter(arr)
a3 = iter(arr)
next(a2)
next(a3)
next(a3)

incs = 0
prev = None

for trio in zip(a1, a2, a3):
    if prev is not None and sum(trio) > prev:
        incs += 1

    print(trio, sum(trio), prev, incs)
    prev = sum(trio)

print(incs)
