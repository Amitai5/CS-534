import sys

import time

import numpy as np
import pandas as pd
import random
import copy



# The name of the file representing the gridworld
# Reward for each action the agent takes.  You may assume this value is non-positive.
# Gamma, the discount parameter
# How many seconds to run for (can be <1 second)
# P(action succeeds):  the transition model.

# Arg format: name of file, reward for action (non positive), gamma (discount), # of seconds to run, P(action succeeds)
# e.g. grid_sample.txt -.1 .2 5 .8

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

file = sys.argv[1]
rew = sys.argv[2]
gamma = sys.argv[3]
sec = sys.argv[4]
P = float(sys.argv[5])
Q = []

def takeAction(s, a):
    s

def load_grid(filename):
    global Q
    grid = pd.read_csv(filename, '\t', header=None).to_numpy()
    Q = copy.deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                s = (i, j)
                Q[i][j] = 0
            elif grid[i][j] == "X":
                x = (i, j)
            else:
                Q[i][j] = int(grid[i][j])
    print("initial Q: \n", Q)

    return grid, s, x

print(load_grid(file))

epsilon = .2

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def inRange(s, a):
    x = s[0] + a[0]
    y = s[1] + a[1]
    return len(board) > x >= 0 and len(board[0]) > y >= 0


def q(s, a):
    tr = Q[s[0]][s[1]]  # default, reflected by border or barrier
    if inRange(s, a):
        x = s[0] + a[0]
        y = s[1] + a[1]
        if Q[x][y] != "X":
            tr = Q[x][y]  # not reflected, valid move
    return tr


def determineAction(s):
    a = random.choice(moves)
    # /* will want to make exploration more complex */
    if random.random() > epsilon:
        best = q(s, a)
        for m in moves:
            current = q(s, m)
            if current > best:
                best = current
                a = m
    return a


def tryA(a):
    tr = np.array(a)
    print("tr: ", tr)
    if random.random() > P:
        if random.random() > .5:
            tr = tr * 2
            # print("forward 2")
        else:
            tr = tr * -1
            # print("back 1")
    return tr[0], tr[1]


def takeAction(s, a):  # /* trickier :-) */
    # /* the ONLY PLACE the transition model should appear in your code */
    s0 = copy.deepcopy(s)
    a = tryA(a)
    print("A: ", a)


def update(s, a, s0):  # /* depends on SARSA vs Q-learning */
    x


def rl():
    while timeRemains:
        s = startState
        while notTerminal(s):
            a = determineAction(s)
            s0 = takeAction(s,a)
            update(s, a, s0)
            s = s0


board, mm, my = load_grid(file)


a = determineAction((0, 0))
print("Action: ", a)
takeAction((0, 0), a)

# print(np.array((1, 0)) * 2)