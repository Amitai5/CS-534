
import csv
import sys
import time
import math
import copy
import heapq
import numpy as np
import BoardWrite

# create globals
#from csvwrite import create_board_csv

w = []
array = []
size = 0

# nothing
ws = []
k = 5
rows = [None] * k
d1 = [None] * (k * 2 - 1)
d2 = [None] * (k * 2 - 1)

cmv = [None] * k


ib = [rows.copy(), d1.copy(), d2.copy(), rows.copy()]  # rows, d1, d2, cols(movevector)
cb = [rows.copy(), d1.copy(), d2.copy(), rows.copy()]  # rows, d1, d2, cols(movevector)

solutions = []
solution = [-1, []]

def cost(base, new):
    global array
    print(w)

    b = base
    n = new
    moveCost = np.absolute(np.array(b) - np.array(n))
    moveCost = np.multiply(moveCost, np.square(np.array(w)))
    moveCost = moveCost.sum()
    return moveCost


def getBoardString(b):
    bString = ""
    for i in b:
        bString = bString + str(i)
    return bString


def moveVector(b):
    x = []
    for i in range(size):
        for j in range(size):
            if b[j][i] != 0:
                x.append(j)
    return x


def weightVector(b):
    x = []
    for i in range(size):
        for j in range(size):
            if b[j][i] != 0:
                x.append(int(b[j][i]))
    return x


def mvToBoard(mv):
    size = k

    for i in range(k):
        w.append(i + 1)

    string = ""
    for i in range(size):
        for j in range(size):
            if mv[j] == i:
                string = string + " " + str(w[j]) + " "
            else:
                string = string + " 0 "
            if j == size - 1:
                string = string + "\n"
    return string


# Wrapper for a HeapQ, mainly provides an "exists" function that tells wheteher a board exists in queue

def findSolution(mv, should_print):
    global w
    global k
    start_time = time.time()

    # load board
    with open('board.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        array = list(reader)
        size = len(array)
        k = size

        for i in range(0, size):
            for j in range(0, size):
                array[i][j] = int(array[i][j])
        w = weightVector(array)

    array = moveVector(array)
    solve(array)
    board_string = mvToBoard(solution[1])
    if should_print:
        print("Best solution:\n", solution[1], "\n cost: ", solution[0])
    elapsed_time = time.time() - start_time
    return elapsed_time, cost(array, solution[1]), 0





def solve(mv):
    global array
    array = mv
    k = len(mv)
    w = range(k)

    print("Board being solved: ")
    print(mvToBoard(mv))



    print("K: ", k)

    print("Weight vector: ", w)

    for i in range(k):
        ws.append(i)
        # addPos(i, ib, mv)
    tryNextQueen()

    print("Finished! Found ", len(solutions), " solutions.")
    print(solutions)


def nextMove(vms, q):
    if not vms:
        ws.append(q)
        return -1  # out of valid moves for a queen, time to go back
    else:  # valid moves remaining so lets try them
        cmv[q] = vms.pop()  # adds row to move vector
        addPos(q)  # adds correlated conflicting rows and diagonals
        tryNextQueen()  # tries to place next queen
        # if we are here the next queen ran out of valid moves so it is time to try next position,
        removePos(q)  # removes current placement of queen from the board arrays
        nextMove(vms, q)  # goes to next valid move for current queen (recursion)


def tryNextQueen():
    if not ws:  # no more queens to try which means all queens have successfully been placed
        print("found a solution! :")
        print(mvToBoard(cmv))
        solutions.append(copy.deepcopy(cmv)) #appends current move vector as a solution
        print(cmv)
        c = cost(array, cmv)

        if c < solution[0] & solution[0] != -1:
            solution[0] = c
            solution[1] = copy.deepcopy(cmv)
    else:
        q = ws.pop()
        vms = genValidMoves(q) #valid moves for a queen
        nextMove(vms, q) #will recursively try all moves or return


def addPos(q, arr=cb, moveVector=cmv):
    c = q
    r = moveVector[c]
    setR(r, c, c, arr)
    setD1(r, c, c, arr)
    setD2(r, c, c, arr)

    #print(arr)

    # arr[0][moveVector[q]] = q
    # arr[1][q + moveVector[q]] = q
    # arr[2][q - moveVector[q] + (k - 1)] = q


def removePos(q, arr=cb, moveVector=cmv):
    c = q
    r = moveVector[c]
    setR(r, c, None, arr)
    setD1(r, c, None, arr)
    setD2(r, c, None, arr)
    # arr[0][moveVector[i]] = None
    # arr[1][i + moveVector[i]] = None
    # arr[2][i - moveVector[i] + (k - 1)] = None


#generate
def genValidMoves(c):
    moves = genMoves(c)
    i = 0
    while i < len(moves):
        r = moves[i]
        if checkValid(r, c):  # if not valid
            moves.pop(i)
        else:
            i = i + 1
    return moves


def checkValid(r, c):
    return cb[0][r] is not None or cb[1][r + c] is not None or cb[2][c - r + (k - 1)] is not None


def genMoves(c):
    moves = []
    x = 0
    # for i in range(k):
    #     if(x == 0):
    #         moves.append(mv[i])
    #     else:
    #         if(mv[i] + x) >= k or mv[i] + x <= 0:
    #             moves.append(mv[i] - (x + 1))
    #             x = x + 1;
    #     x = (x + 1) * -1

    return list(range(k))


def setD1(r, c, to, arr=cb):
    d = r + c
    # print("Row: ", r, "  Column: ", c, "D1: ", d)
    arr[1][d] = to


def setD2(r, c, to, arr=cb):
    d = c - r + (k - 1)
    # print("Row: ", r, "  Column: ", c, "D2: ", d)
    arr[2][d] = to


def setR(r, c, to, arr=cb):
    arr[0][r] = to


board = [1, 1, 1, 1, 1]

#solve([0, 0, 1, 0, 4])

# print("finished, found ", len(solutions), " solutions")




