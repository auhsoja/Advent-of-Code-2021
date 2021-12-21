import requests
import math
import sys
from collections import defaultdict
import heapq

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')

def get_day2(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip()


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


def get_bit(byte, i):
    x = (byte & 0x1 << i) >> i
    return x


def packet_version_type(bits):
    v = int(bits[:3], 2)
    t = int(bits[3:6], 2)

    return v, t


def parse_operator(bits, typ):
    l_type = bits[6]

    if l_type == 0:
        length = int(bits[7:22], 2)


def evaluate_literal(bits):
    v, _ = packet_version_type(bits)
    data = bits[6:]
    value = 0
    length = 6
    while True:
        block = data[:5]
        data = data[5:]
        length += 5

        x = int(block[1:], 2)
        value = (value << 4) + x
        if block[0] == '0':
            #print("Literal:", value)
            return (v, value, length)


def evaluate_operator(bits):
    v, t = packet_version_type(bits)
    #print("Version:",t)
    bits = bits[6:]
    length_t = bits[0]
    bits = bits[1:]
    tot_l = 7

    curr = None
    add = lambda x,y: x+y
    times = lambda x,y: x*y
    gt = lambda x,y: int(x>y)
    lt = lambda x,y: int(x<y)
    eq = lambda x,y: int(x==y)
    ops = [add, times, min, max, None, gt, lt, eq]
    op = ops[t]

    if length_t == '0':
        length = int(bits[:15], 2)
        #print(f"Operator packet in length form. Has {length} bits")
        bits = bits[15:]
        tot_l += 15
        while length > 6:
            version, value, l = evaluate(bits)
            if curr is None:
                curr = value
            else:
                curr = op(curr, value)
            v += version
            length -= l
            bits = bits[l:]
            tot_l += l

        return v, curr, tot_l

    else:
        packets = int(bits[:11], 2)
        #print(f"Operator packet in count form. Has {packets} packets")
        bits = bits[11:]
        tot_l += 11
        for p in range(packets):
            version, value, l = evaluate(bits)
            if curr is None:
                curr = value
            else:
                curr = op(curr, value)
            v += version
            tot_l += l
            bits = bits[l:]

        return v, curr, tot_l


def evaluate(bits):
    # Return the packet version, value, and its length
    v, t = packet_version_type(bits)
    #print(f"Evaluating {bits}. Version: {v}")

    #print(f"curr len: {len(bits)}. version: {v}.", end=" ")

    if t == 4:
        #print("found literal")
        return evaluate_literal(bits)

    #print("found operator")
    return evaluate_operator(bits)


def version_sum(bits):
    v, value, l = evaluate(bits)
    return v


def hex2bits(s):
    b = bytes.fromhex(s)
    out = ""
    for byte in b:
        binstr = bin(byte)[2:]
        fill = 8 - len(binstr)
        out += "0"*fill + binstr

    return out


def solve(text):
    bits = hex2bits(text)
    v, value, l = evaluate(bits)
    #print(bits)
    print(value)


#solve("8A004A801A8002F478")
#solve("620080001611562C8802118E34")
#solve("C0015000016115A2E0802F182340")
#solve("A0016C880162017C3686B18A3D4780")
solve("C200B40A82")
solve("04005AC33890")
solve("880086C3E88112")
solve("CE00C43D881120")
solve("D8005AC2A8F0")
solve("F600BC2D8F")
solve("9C005AC2F8F0")
solve("9C0141080250320F1802104A08")


text = get_day2(16)
solve(text)
