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
# e.g. grid_sample.txt -.1 .8 5 .8

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

file = sys.argv[1]
rew = float(sys.argv[2])
gamma = float(sys.argv[3])
sec = float(sys.argv[4])
P = float(sys.argv[5])

print("File name: ", file)
print("Reward: ", rew)
print("Gamma: ", gamma)
print("Time(seconds): ", sec)
print("P(success): ", P)

Q = []
heatmap = []
count = 0
stay = 0
double = 0
backwards = 0

term = []

# def takeAction(s, a):
#     s

def load_grid(filename):
    global Q
    global heatmap

    grid = pd.read_csv(filename, delimiter='\t',header=None).to_numpy()
    Q = copy.deepcopy(grid)
    heatmap = copy.deepcopy(grid)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            heatmap[i][j] = 0
            if grid[i][j] == "S":
                s = (i, j)
                Q[i][j] = 0
            elif grid[i][j] == "X":
                x = (i, j)
            else:
                Q[i][j] = int(grid[i][j])
                grid[i][j] = int(grid[i][j])

    print("initial Q: \n", Q)
    # heatmap = [0] * len(grid[0])
    # heatmap = [heatmap] * len(grid)

    print("heatmap: \n", heatmap)

    return grid, s, x

print(load_grid(file))

epsilon = .2

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def inRange(s, a):
    x = s[0] + a[0]
    y = s[1] + a[1]
    return len(board) > x >= 0 and len(board[0]) > y >= 0


def q(s, a):
    tr = Q[s]  # default, reflected by border or barrier
    if inRange(s, a):
        x = s[0] + a[0]
        y = s[1] + a[1]
        if Q[x][y] != "X":
            tr = Q[x][y]  # not reflected, valid move
    return tr


def determineAction(s, r=True):

    a = random.choice(moves)
    # /* will want to make exploration more complex */
    if random.random() > epsilon or not r:
        best = q(s, a)
        for m in moves:
            current = q(s, m)
            if current > best:
                best = current
                a = m
    return a


def tryA(a):
    global stay
    global double
    global backwards
    tr = np.array(a)
    # print("tr: ", tr)
    # print("P: ", P)
    if random.random() > P:

        if random.random() > .5:
            tr = tr * 2
            double += 1
            # print("forward 2")
        else:
            tr = tr * -1
            backwards += 1
            # print("back 1")
    else:
        stay += 1
    return tr[0], tr[1]


def takeAction(s, a, bool=False):  # /* trickier :-) */
    # /* the ONLY PLACE the transition model should appear in your code */
    s0 = copy.deepcopy(s)
    if not bool:
        aa = tryA(a)  # actual action to take
    else:
        aa = a
    x = s[0] + aa[0]
    y = s[1] + aa[1]
    # print("aa: ", aa)
    if aa[0] == 2 or aa[1] == 2 or aa[0] == -2 or aa[1] == -2:
        x1 = s[0] + a[0]
        y1 = s[1] + a[1]
        if inRange(s, a) and board[x1][y1] != 'X':
            s0 = (x1, y1)
            if inRange(s, aa) and board[x][y] != 'X':
                s0 = (x, y)
    elif inRange(s, aa) and board[x][y] != 'X':
        s0 = (x, y)
    return s0


def update(s, a, s0):  # /* depends on SARSA vs Q-learning */
    #s = x,y pair
    #s0 = x,y pair
    #a = movement [(1, 0), (-1, 0), (0, 1), (0, -1)]
    global gamma #passed as parameter
    global rew

    R = rew

    if not notTerminal(s):
        print(board[s])
        R += board[s]

    alpha = 0.5 #learning rate - higher means faster
    Qt=Q[s]#Current Q-value
    # s1 = takeAction(s, a, True)

    a0 = determineAction(s0)


    # Qnext = Q[s1] #next reward estimate - from the Q-value of the square you want to be at
    # Qnext = q(s0, a0)
    Qnext = q(s0, a0)
    Qmaxfuture = Qnext #need to calcualte for Q-learning, maximum future reward - currently estimate for testing

    SARSA = 1#set to 1 for SARSA, 2 for Q-learning - I think SARSA should run, but Q-learning is not fully implemented
    if SARSA:
        #SARSA
        Q[s] = Qt + alpha*(R + gamma*Qnext-Qt)
    else:
        #Q learning
        Q[s[0]][s[1]] = Qt + alpha*(rew + gamma*Qmaxfuture-Qt)


def notTerminal(s):
    # print("nt: ", board[s])
    # if(board[s] == 'X'):
    #     print("Board(s): ", board[s], "\nSomething is wrong")
    return board[s] == 0 or board[s] == 'S'


def printArray(arr):
    string = ""
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i, j] != 'X':
                string = string + str(np.round(float(arr[i, j]), 2))
            else:
                string += str(arr[i, j])
            string += "\t"
        string = string + "\n"
    print(string)

def printTermArray(arr):
    string = ""
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if notTerminal((i, j)):
                string = string + "N"
            else:
                print(board[i, j])
                string += "T"
            string += "\t"
        string = string + "\n"
    print(string)


def printBestMoves():
    string = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i, j] == 0 or board[i, j] == 'S':
                a = determineAction((i, j), False)
                c = ""
                if a == (1, 0):
                    c = "v"
                elif a == (-1, 0):
                    c = "^"
                elif a == (0, 1):
                    c = ">"
                elif a == (0, -1):
                    c = "<"
                else:
                    c = "broke"
            else:
                c = str(board[i, j])
            string += "\t" + c + "\t"
        string += "\n"
    print(string)




def rl():
    global count
    startTime = time.time()
    while time.time() - startTime < sec:
        s = startState
        while notTerminal(s):
            a = determineAction(s)
            s0 = takeAction(s, a)
            update(s, a, s0)
            heatmap[s0] += 1
            count = count + 1
            s = s0
            # print("Q: \n", Q)
        # print("Term reached at ", s)
    print("Q:")

    printArray(Q)
    print("Heatmap:")
    for i in range(len(heatmap)):
        for j in range(len(heatmap[0])):
            heatmap[i, j] = (heatmap[i, j] / count) * 100
    printArray(heatmap)
    print("Stay, Double, Backwards: ", stay, double, backwards)
    printBestMoves()




board, startState, my = load_grid(file)

printTermArray(board)




rl()





# a = determineAction((0, 0))
# print("Action: ", a)
# print("s0: ", takeAction((0, 0), a))

# print("Bool: ", notTerminal((0,1)))


# print("bool: ", a.contains(0))

# print(np.array((1, 0)) * 2)