import sys

import time

import numpy as np
import pandas as pd
import random
import copy
import os



# The name of the file representing the gridworld
# Reward for each action the agent takes.  You may assume this value is non-positive.
# Gamma, the discount parameter
# How many seconds to run for (can be <1 second)
# P(action succeeds):  the transition model.

# Arg format: name of file, reward for action (non positive), gamma (discount), # of seconds to run, P(action succeeds)
# e.g. grid_sample.txt -.1 .8 5 .8

print('Number of arguments:', len(sys.argv), 'arguments.')

# if wrong parameters input
if len(sys.argv) != 6:
    print("Format: rl.py <filename> <reward> <gamma> <time to learn> <movement probability>")
    exit(1)

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
startTime = 0

# def takeAction(s, a):
#     s

# parameters
alpha = 0.25  # learning rate - higher means faster
epsilon = .1  # chance to explore


# Load the board from the given file
def load_grid(filename):
    global Q
    global heatmap

    filename = os.getcwd() + "\\testBoards\\grid" + filename + ".txt"

    grid = pd.read_csv(filename, delimiter='\t',header=None).to_numpy()
    Q = copy.deepcopy(grid)
    heatmap = copy.deepcopy(grid)
    # qCell = [["a", "b", "c"],
    #          ["d", "e", "f"],
    #          ["g", "h", "i"]]
    qCell = [[10.0, 0.0, 0.0],
             [0.0, 10.0, 10.0],
             [0.0, 10.0, 10.0]]
    qCell = np.array(qCell)

    print(qCell)
    print(type(qCell[0, 0]))

    x = []

    print(grid)


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            heatmap[i][j] = 0
            Q[i][j] = copy.deepcopy(qCell)
            if grid[i][j] == "S":
                s = (i, j)

            elif grid[i][j] == "X":
                x = (i, j)
            else:
                grid[i][j] = int(grid[i][j])

    # print("Board:")
    # printArray(Q)
    return grid, s, x





# possible moves (up,down,left,right)

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Determine if action is within the board's boundaries
def inRange(s, a):
    x = s[0] + a[0]
    y = s[1] + a[1]
    return len(board) > x >= 0 and len(board[0]) > y >= 0


def q(s, a):

    # print("S: ", s)
    # print("A: ", a)


    tr = Q[s][a]  # default, reflected by border or barrier
    # if inRange(s, a):
    #     x = s[0] + a[0]
    #     y = s[1] + a[1]
    #     if Q[x][y] != "X":
    #         tr = Q[x][y]  # not reflected, valid move
    # print("Tr: ", tr)
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
    global timeR
    policy = "g"
    timeR = time.time() - startTime
    if policy == "e":
        return random.random() > epsilon  # policy e (epsilon greedy)
    elif policy == "f":
        return timeR < sec / 2 or random.random() < timeR / sec  # policy f some pretty extreme heavy explore,
        # then gradual towards greedy
    elif policy == "g":
        return random.random() < timeR / sec  # policy g, gradual start high explore, end greedy
    elif policy == "h":
        return timeR < sec/10 or random.random() < .01


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


def takeAction(s, a):  # /* trickier :-) */
    # /* the ONLY PLACE the transition model should appear in your code */
    s0 = copy.deepcopy(s)

    aa = tryA(a)  # actual action to take

    x = s[0] + aa[0]
    y = s[1] + aa[1]

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
    # s = x,y pair
    # s0 = x,y pair
    # a = movement [(1, 0), (-1, 0), (0, 1), (0, -1)]
    global gamma # passed as parameter
    global rew # Parameter - cost of movement

    R = rew  #cost of movement

    if not notTerminal(s0): #if terminal
        R += float(board[s0])
        Qnext = 0
        Qmaxfuture = 0

    else:
        a0 = determineAction(s0)
        Qnext = q(s0, a0) # SARSA, value after next action
        aM = determineAction(s0, False) # Best action to take from S0
        Qmaxfuture = q(s0, aM)  # Q-learning, maximum future reward - Q value of next state


    global alpha # learning rate - higher means faster

    Qt = q(s, a)

    SARSA = False  # set to 1 for SARSA, 0 for Q-learning
    if SARSA:
        #SARSA
        Q[s][a] = float(Qt + alpha*(R + gamma*Qnext-Qt))
        # print(Q[s][a])

    else:
        #Q learning
        Q[s][a] = Qt + alpha*(R + gamma*Qmaxfuture-Qt)


def notTerminal(s):
    return board[s] == 0 or board[s] == 'S'


def printArray(arr):
    string = ""
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i, j] != 'X':
                format_float = "{:2.0f}".format(float(arr[i, j]))
                string = string + str(format_float)
            else:
                string += '  X  ' #Extra spaces included for formatting
            string += "\t"
        string = string + "\n"
    print(string)

def printQ():
    string = ""
    for i in range(len(Q)):
        for j in range(len(Q[0])):
            if notTerminal((i, j)):

                sq = 0
                for m in moves:
                    sq += Q[i, j][m]
                sq = sq / len(moves)
                format_float = "{:05.2f}".format(float(sq))
            else:
                format_float = str(board[i, j]) + "   "
            string += str(format_float) + "\t"
        string += "\n"
    print(string)


def printQMax():
    string = ""
    for i in range(len(Q)):
        for j in range(len(Q[0])):
            if notTerminal((i, j)):

                sq = Q[i, j][moves[0]]
                for m in moves:
                    n = Q[i, j][m]
                    if n > sq:
                        sq = n
                sq = sq / len(moves)
                format_float = "{:05.2f}".format(float(sq))
            else:
                format_float = str(board[i, j]) + "   "
            string += str(format_float) + "\t"
        string += "\n"
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


# Runs learning for the specified time
def rl():
    global count
    global timeR
    global startTime
    startTime = time.time()
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
    printQ()
    print("\nQmax:")
    printQMax()

    print("Heatmap:")
    for i in range(len(heatmap)):
        for j in range(len(heatmap[0])):
            heatmap[i, j] = (heatmap[i, j] / count) * 100
    printArray(heatmap)

    print("Unchanged, Double, Backwards: ", stay, double, backwards) # Count of number of moves that were as intended, 2 spaces forward, or backwards
    printBestMoves()



# Starting code - load file, print the initial board, then run learning
board, startState, my = load_grid(file)

printTermArray(board)

print("\n--------------------------------------------------\nRunning...\n")
# run learning
rl()
