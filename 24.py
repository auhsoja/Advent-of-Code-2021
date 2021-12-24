import sys
import numpy as np
import itertools
from utils import *
from z3 import *


# The function that gets repeated. I did not find this myself.
# Credit to the Advent of Code redditors (specifically u/i_have_no_biscuits)
def repeated(z, w, p0, p1, p2):
    return If(
        (z % 26 + p1) != w,
        (z / p0) * 26 + w + p2,
        (z / p0)
    )


# Sanity check run a program and return z register
def run(data, lines):
    assert(len(data) == 14)
    state = defaultdict(int)
    idx = 0
    for i, line in enumerate(lines):
        cmd, var = line.split()[:2]
        if cmd == "inp":
            state[var] = int(data.pop(0))
        else:
            val = line.split()[2]
            if val in "wxyz":
                val = state[val]
            else:
                val = int(val)

            if cmd == "add":
                state[var] += val
            elif cmd == "mul":
                state[var] *= val
            elif cmd == "div":
                state[var] //= val
            elif cmd == "mod":
                state[var] %= val
            elif cmd == "eql":
                state[var] = int(state[var] == val)

    return state['z']


def solve_day(text):
    names = []
    inmap = {}
    solver = Solver()
    sols = []
    curr_z = 0

    # Loop through each block (they repeat)
    for idx in range(0, len(text), 18):
        # Get only the params that matter
        offsets = [4, 5, 15]
        p1, p2, p3 = [int(text[idx+offset].split()[-1]) for offset in offsets]

        i = idx // 18
        w_name = f"w_{i+1}"
        curr_w = Int(w_name)
        inmap[w_name] = curr_w
        solver.add(1 <= curr_w, curr_w <= 9)
        names.append(w_name)

        # Apply the repeated function
        res = repeated(curr_z, curr_w, p1, p2, p3)
        curr_z = Int(f"z_{i+1}")
        solver.add(curr_z == res)

    solver.add(curr_z == 0)
    print(names)

    while True:
        s = solver.check()

        # No more solutions, exit
        if str(s) == "unsat":
            break

        # Save the current solution
        m = solver.model()
        settings = [str(m[inmap[n]]) for n in names]
        sols.append(int("".join(settings)))

        # Disallow the current solution
        constr = True
        for n, v in zip(names, settings):
            constr = And(inmap[n] == int(v), constr)

        solver.add(Not(constr))

    print(max(sols))
    print(min(sols))


text = get_day(24)
solve_day(text)
