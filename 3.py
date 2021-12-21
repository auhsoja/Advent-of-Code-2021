import requests
import numpy as np

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    tot = len(text)
    print(tot)
    counts = np.array([0 for k in range(len(text[0]))])
    arr = np.zeros((tot, len(text[0])), dtype=np.uint8)

    for idx, elt in enumerate(text):
        bit_vec = np.array([int(k) for k in elt])
        arr[idx, :] = bit_vec
        # counts += bit_vec
        # print(f"elt: {elt}\tcurr: {counts}")


    # First find gamma
    curr_arr = arr.copy()
    gamma = None
    eps = None
    for col in range(curr_arr.shape[1]):
        tot = curr_arr[:, col].sum()
        bit_content = 0
        if tot >= float(curr_arr.shape[0]) / 2:
            bit_content = 1

        curr_arr = curr_arr[np.where(curr_arr[:, col] == bit_content)]
        if curr_arr.shape[0] == 1:
            gamma = curr_arr
            break

    # Now find eps
    curr_arr = arr.copy()
    for col in range(curr_arr.shape[1]):
        tot = curr_arr[:, col].sum()
        bit_content = 0
        if tot >= float(curr_arr.shape[0]) / 2:
            bit_content = 1

        curr_arr = curr_arr[np.where(curr_arr[:, col] != bit_content)]
        if curr_arr.shape[0] == 1:
            eps = curr_arr
            break

    print(gamma, eps)

    s1 = ''.join([str(x) for x in np.squeeze(gamma)])
    s2 = ''.join([str(x) for x in np.squeeze(eps)])
    print(s1, s2)

    x1 = int(s1, 2)
    x2 = int(s2, 2)
    print(x1*x2)


print("--------------- TEST 1 --------------")
vals = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010'
]
solve(vals)
print("------------- TEST 1 Done -----------")
text = get_day(3)
solve(text)
