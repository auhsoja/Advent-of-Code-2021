import sys
import numpy as np
import itertools
from utils import *


def solve(text):
    table = {}

    p1 = int(text[0].split(": ")[1])-1
    p2 = int(text[1].split(": ")[1])-1

    p1_score = 0
    p2_score = 0

    pos = [p1, p2]
    scores = [p1_score, p2_score]

    roll = 1
    rolls = 0

    while True:
        for i in range(2):
            rolls += 3
            m = 0
            for _ in range(3):
                m += roll
                roll += 1
                if roll > 100:
                    roll = 1

            new_p = (pos[i] + m) % 10
            pos[i] = new_p
            scores[i] += new_p + 1


            if rolls < 30 or max(scores) > 980:
                pass
                #print(f"Player {i+1} rolled {roll} and moved to {new_p+1} for score of {scores[i]}")

            if scores[i] >= 1000:
                break

        else:
            continue
        break

    print(rolls, scores)
    print(rolls * min(scores))


def solve2(text, goal):
    table = {}

    p1 = int(text[0].split(": ")[1])-1
    p2 = int(text[1].split(": ")[1])-1

    p1_score = 0
    p2_score = 0

    pos = [p1, p2]
    scores = [p1_score, p2_score]

    multipliers = defaultdict(int)
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                multipliers[i+j+k] += 1

    def recur(state):
        if state in table:
            return table[state]

        p1, p2, s1, s2, p1_turn = state
        # Check if the other player has won. We will never move
        # if we already won
        if p1_turn:
            if s2 >= goal:
                table[state] = (0, 1)
                return table[state]
        else:
            if s1 >= goal:
                table[state] = (1, 0)
                return table[state]

        res = [0, 0]

        tot = 0
        for roll in range(3, 10):
            player = 1-int(p1_turn)
            curr = state[player]
            curr = (curr+roll)%10

            new_state = [x for x in state]
            new_state[player] = curr
            new_state[player+2] += curr+1
            new_state[-1] = not(p1_turn)
            new_state = tuple(new_state)

            win1, win2 = recur(new_state)
            res[0] += win1 * multipliers[roll]
            res[1] += win2 * multipliers[roll]

        table[state] = res
        return res

    res = recur((p1, p2, 0, 0, True))
    #for state in table:
    #    print(state, table[state])
    print(max(res))


test = """Player 1 starting position: 4
Player 2 starting position: 8""".split("\n")

solve2(test, 21)

#sys.exit()

text = get_day(21)
solve2(text, 21)
