import requests
import math
import sys
from collections import defaultdict
import heapq
import time

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip()

raw = get_day(17)
print(raw)
a = raw.split('=')
x1,x2 = a[1][:-3].split('..')
y1,y2 = a[2].split('..')
x1,x2,y1,y2 = int(x1),int(x2),int(y1),int(y2)


def step(pos,vel):
    x,y=pos
    vx,vy=vel
    maxy = 0
    while x<=x2+1 and y1-1<=y:
        x,y = x + vx , y + vy
        if maxy<y: maxy = y
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True,(x,y),maxy

        vx = vx-1 if vx>0 else 0
        vy -= 1
        #print(x,y,vx,vy)
    return False,(0,0),maxy

result = 0
velValues = set()
for x in range(300):
    for y in range(-130,120):
        hit, pos, maxy = step((0,0),(x,y))
        if hit:
            #print(hit,x,y,maxy)
            if maxy > result: result = maxy
            velValues.add((x,y))
print('part1',result)
print('part2',len(velValues))
