import requests
import numpy as np

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')

def solve(text):
    calls = [int(k) for k in text[0].split(',')]
    boards = []
    curr_board = []
    for row in text[2:]:
        if len(row) > 0:
            add = [int(k) for k in row.split() if len(k) > 0]
            curr_board.append(add)
            assert(len(add) == 5)

        if len(curr_board) == 5:
            b = np.array(curr_board)
            boards.append(np.dstack([b, np.zeros_like(b)]))
            curr_board = []

    alive = set([k for k in range(len(boards))])
    for call in calls:
        # print(f"CALL: {call}")
        for idx, board in enumerate(boards):
            if idx not in alive:
                continue

            # Mark the call
            loc = np.where(board[:, :, 0] == call)
            board[:, :, 1][loc] = 1

            # print(board[:, :, 0])
            # print(board[:, :, 1])
            # print()

            # Check for victory
            cols, rows = board[:, :, 1].sum(axis=0), board[:, :, 1].sum(axis=1)
            if 5 in cols or 5 in rows:
                if len(alive) == 1:
                    print(cols, rows)
                    unmarked = 1 - board[:, :, 1]
                    score = (unmarked * board[:, :, 0]).sum()
                    print(score, call)
                    print(score * call)
                    break
                else:
                    alive.remove(idx)
        else:
            continue

        break

test1 = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".split('\n')

solve(test1)

text = get_day(4)
solve(text)
