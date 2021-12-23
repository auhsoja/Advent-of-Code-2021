import sys
import numpy as np
import itertools
from utils import *


HALL_L = 11

step_costs = {
    'A':1, 'B':10, 'C':100, 'D':1000
}

dests = {'A':2, 'B':4, 'C':6, 'D':8}

pts = [(i, 0) for i in range(11)]
for x in range(2, 10, 2):
    pts += [(x, j) for j in range(1, 5)]

def neighbors(state):
    '''
    Find all states reachable in 1 step from the current state and their costs
    '''
    mapping = {pt: '.' for pt in pts}
    for agent, (x, y) in state:
        mapping[(x,y)] = agent

    # Make sure no two agents have same state
    assert(len(set(mapping.values())) == 17)

    nb = []
    for idx, (agent, (x, y)) in enumerate(state):
        cost = step_costs[agent[0]]
        a = agent[0]

        if x == dests[a]:
            # To be non-blocking, everyone below must be correct
            for y2 in range(y+1, 5):
                if mapping[(x, y2)][0] != a:
                    # incorrect
                    break
            else:
                # Everything looks good, don't move
                continue


        # This agent is not in their proper place; try moving

        if y > 0:
            # In a room. Check if we're blocked
            blocked = False
            for y2 in range(1, y):
                if mapping[(x, y2)] != '.':
                    # We're blocked
                    blocked = True

            if blocked:
                continue

            # In a room and not blocked
            for sign in range(2):
                sign = 2*sign - 1
                for dx in range(1, 9):
                    dx = dx * sign
                    xf = x + dx

                    if xf in dests.values():
                        # Do not stop in front of a room
                        continue

                    if xf < 0 or xf > 10:
                        break
                    if mapping[(xf, 0)] != '.':
                        break

                    # Found a new reachable state! Append to nbs
                    move_cost = cost * abs(dx) + cost * y
                    new_state = (*state[:idx], (agent, (xf, 0)), *state[idx+1:])
                    nb.append((new_state, move_cost))

            continue

        if y > 0:
            continue

        # We now know that we are in the hallway. Check if dest room is reachable
        dest_x = dests[a]
        dest_y = 0
        can_enter = True
        for y2 in range(1, 5):
            occ = mapping[(dest_x, y2)]
            if occ == '.':
                dest_y += 1
            elif occ[0] != a:
                can_enter = False

        if not can_enter:
            continue


        sgn = (dest_x - x) // abs(dest_x - x)
        for i in range(x+sgn, dest_x, sgn):
            if mapping[(i, 0)] != '.':
                break
        else:
            move_cost = cost * abs(dest_x - x) + cost * dest_y
            new_state = (*state[:idx], (agent, (dest_x, dest_y)), *state[idx+1:])
            nb.append((new_state, move_cost))

    return nb


def done(state):
    for agent, (x, y) in state:
        a = agent[0]
        if x != dests[a] or y == 0:
            return False
    return True


def dijkstras(state_i):
    '''
    Find shortest path from x to y using Dijkstra's Algorithm with a binary heap
    '''

    graph = defaultdict(dict)


    distance_costs = defaultdict(lambda: float("inf"))
    distance_costs[state_i] = 0
    min_dist = [(0,state_i)]
    visited = set()
    finishes = []

    while min_dist:

        current_dist, current = heapq.heappop(min_dist)
        if current in visited:
            continue
        visited.add(current)

        if done(current):
            finishes.append((current_dist, current))

        nb = neighbors(current)

        for neighbour, cost in nb:
            if neighbour in visited:
                continue
            checking_dist = current_dist + cost
            if checking_dist < distance_costs[neighbour]:
                distance_costs[neighbour] = checking_dist
                #print(checking_dist, neighbour)
                heapq.heappush(min_dist, (checking_dist, neighbour))

    print(min(finishes))

    return None


def parse_room(lines):
    state = {}
    lines = lines[:3] + ["  #D#C#B#A#  ", "  #D#B#A#C#  "] + lines[3:]
    next_id = {x:1 for x in "ABCD"}
    for i in range(2, 6):
        for idx, c in enumerate(lines[i]):
            if c in "ABCD":
                state[c+str(next_id[c])] = (idx-1, i-1)
                next_id[c] += 1

    state_imm = tuple((k,v) for k,v in state.items())
    return state_imm


def solve(text):
    state = parse_room(text)
    dijkstras(state)



test = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".split("\n")


solve(test)

#sys.exit()

text = get_day(23)
solve(text)
