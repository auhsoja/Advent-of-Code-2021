import requests

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')

text = get_day(2)
x = 0
z = 0
aim = 0

for line in text:
    comm, val = line.split()
    val = int(val)

    if comm == "forward":
        x += val
        z += aim * val
    elif comm == "down":
        aim += val
    elif comm == "up":
        aim -= val
    else:
        raise ValueError("unexpected command")

print(x * z)

