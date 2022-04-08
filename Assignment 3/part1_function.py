import numpy as np
import pandas as pd
import random
import time
import copy

P = 0.7  # Blocked value
rew = -0.1  # Standard Value
gamma = 0
alpha = 0
epsilon = 0
is_sarsa = False

Q = []
stay = 0
term = []
count = 0
double = 0
heatmap = []
board = None
backwards = 0
moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_grid(filename):
    global Q
    global heatmap

    grid = pd.read_csv(filename, delimiter='\t',header=None).to_numpy()
    Q = copy.deepcopy(grid)
    heatmap = copy.deepcopy(grid)
    qCell = [[10.0, 0.0, 0.0],
             [0.0, 10.0, 10.0],
             [0.0, 10.0, 10.0]]
    qCell = np.array(qCell)


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
    return grid, s, x


def inRange(s, a):
    x = s[0] + a[0]
    y = s[1] + a[1]
    return len(board) > x >= 0 and len(board[0]) > y >= 0

def q(s, a):
    tr = Q[s][a]  # default, reflected by border or barrier
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
    return random.random() > epsilon
    # return timeR < sec / 2 or random.random() <


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
    global gamma #passed as parameter
    global is_sarsa
    global rew

    R = rew #cost of movement

    if not notTerminal(s0): #if terminal
        R += float(board[s0])
        Qnext = 0
        Qmaxfuture = 0

    else:
        a0 = determineAction(s0)
        Qnext = q(s0, a0) #SARSA, value after next action
        aM = determineAction(s0, False)
        Qmaxfuture = q(s0, aM)  # Q-learning, maximum future reward - Q value of next state
    Qt = q(s, a)

    if is_sarsa:
        #SARSA
        Q[s][a] = float(Qt + alpha*(R + gamma*Qnext-Qt))
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
                format_float = "{:05.2f}".format(float(arr[i, j]))
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


def rl(filename, interval, sec, sarsa, a, e, g):
    global Q
    global rew
    global stay
    global term
    global board
    global count
    global alpha
    global gamma
    global double
    global heatmap
    global epsilon
    global is_sarsa
    global backwards

    Q = []
    stay = 0
    term = []
    count = 0
    alpha = a
    gamma = g
    double = 0
    epsilon = e
    heatmap = []
    backwards = 0
    is_sarsa = sarsa

    x = []
    y = []
    y_hat = 0
    terminal_count = 1

    board, start_state, my = load_grid(filename)
    start_time = time.time()
    last_save = start_time

    while time.time() - start_time < sec:
        s = start_state
        while notTerminal(s):
            a = determineAction(s)
            s0 = takeAction(s, a)
            update(s, a, s0)
            count = count + 1
            heatmap[s0] += 1
            y_hat += rew
            s = s0

            actual_interval = time.time() - last_save
            if actual_interval > interval:
                x.append(time.time() - start_time)
                y.append(y_hat / terminal_count)
                last_save = time.time()

        terminal_count += 1
        y_hat += board[s]
    return x, y
