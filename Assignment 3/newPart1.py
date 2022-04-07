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
#print('Argument List:', str(sys.argv))

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
timeR = 0

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

    print("Board: \n", Q)

    return grid, s, x

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
    if explore() or not r:
        best = q(s, a)
        for m in moves:
            current = q(s, m)
            if current > best:
                best = current
                a = m
    return a

def explore():
    # random.random() > epsilon
    return timeR < sec / 2 or random.random()


def tryA(a):
    global stay
    global double
    global backwards
    tr = np.array(a)
    if random.random() > P:

        if random.random() > .5:
            tr = tr * 2
            double += 1
        else:
            tr = tr * -1
            backwards += 1
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

    R = rew #cost of movement

    if not notTerminal(s0):
        R += float(board[s0])
        Qnext = 0
        Qmaxfuture = 0

    else:
        a0 = determineAction(s0)
        Qnext = q(s0, a0) #SARSA, value after next action
        aM = determineAction(s0, False)
        Qmaxfuture = q(s0, aM)  # Q-learning, maximum future reward - Q value of next state

    # s1 = takeAction(s, a, True)

    alpha = 0.4 #learning rate - higher means faster
    Qt=Q[s]#Current Q-value
    # s1 = takeAction(s, a, True)


    # a1 = determineAction(s1)


    # Qnext = Q[s1] #next reward estimate - from the Q-value of the square you want to be at
    # Qnext = q(s0, a0)
    # Qnext = q(s1, a1)

    SARSA = False#set to 1 for SARSA, 0 for Q-learning
    if SARSA:
        #SARSA
        Q[s] = Qt + alpha*(R + gamma*Qnext-Qt)
    else:
        #Q learning
        Q[s] = Qt + alpha*(R + gamma*Qmaxfuture-Qt)


def notTerminal(s):
    return board[s] == 0 or board[s] == 'S'


def printArray(arr):
    string = ""
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i, j] != 'X':
                format_float = "{:05.2f}".format(float(arr[i, j]))
                string = string + str(format_float)
            else:
                string += '  X  ' #Extra spaces included for formatting
            string += "\t"
        string = string + "\n"
    print(string)

def printTermArray(arr):
    string = ""
    stringTerm = "Terminal States:"
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if notTerminal((i, j)):
                string += "N"
            else:
                stringTerm+="\t"+str(board[i, j])
                string += "T"
            string += "\t"
        string = string + "\n"
    print(stringTerm)
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
    global timeR
    startTime = time.time()
    # timeR = 0
    while timeR < sec:
        s = startState
        while notTerminal(s):
            a = determineAction(s)
            s0 = takeAction(s, a)
            update(s, a, s0)
            heatmap[s0] += 1
            count = count + 1
            s = s0
        timeR = time.time() - startTime
    print("--------------------------------------------------\nDone\n\nQ:")

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

print("\n--------------------------------------------------\nRunning...\n")
#run learning
rl()
