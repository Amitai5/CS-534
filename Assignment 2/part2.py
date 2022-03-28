
import csv
import sys
import time
import math
import copy
import heapq
import numpy as np
import BoardWrite
import pandas as pd

# create globals
#from csvwrite import create_board_csv

w = []
array = []
size = -1

# nothing
ws = []
k = -1
rows = [None] * k
d1 = [None] * (k * 2 - 1)
d2 = [None] * (k * 2 - 1)

cmv = [None] * k
cc = 0  # current solution cost


ib = [rows.copy(), d1.copy(), d2.copy(), rows.copy()]  # rows, d1, d2, cols(movevector)
cb = [rows.copy(), d1.copy(), d2.copy(), rows.copy()]  # rows, d1, d2, cols(movevector)

solutions = []
solution = [-1, []]

def cost(base, new):
    global array
    # print(w)

    b = base
    n = new
    moveCost = np.absolute(np.array(b) - np.array(n))
    moveCost = np.multiply(moveCost, np.square(np.array(w)))
    moveCost = moveCost.sum()
    return moveCost

def singleCost(new, q):
    global array
    global w

    mc = np.absolute(array[q] - new)
    mc = mc * np.square(w[q])
    return mc


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

def findSolution(array, should_print):
    global w
    global k
    global rows
    global d1
    global d2
    global size
    global ib
    global cb
    global cmv
    global solution
    global solutions
    global ws

    ws = []

    start_time = time.time()

    size = len(array)
    k = size
    for i in range(0, size):
        for j in range(0, size):
            array[i][j] = int(array[i][j])
    w = weightVector(array)

    rows = [None] * k
    d1 = [None] * (k * 2 - 1)
    d2 = [None] * (k * 2 - 1)

    cmv = [None] * k

    ib = [rows.copy(), d1.copy(), d2.copy(), rows.copy()]  # rows, d1, d2, cols(movevector)
    cb = [rows.copy(), d1.copy(), d2.copy(), rows.copy()]  # rows, d1, d2, cols(movevector)

    solutions = []
    solution = [-1, []]

    array = moveVector(array)
    # w = weightVector(array)

    solve(array)
    # board_string = mvToBoard(solution[1])
    if should_print:
        print("Best solution:\n", solution[1], "\n cost: ", solution[0])
    elapsed_time = time.time() - start_time
    return elapsed_time, cost(array, solution[1]), 0


def solve(mv):
    global array
    global k
    global w
    array = mv
    k = len(mv)

    # print("Board being solved: ")
    # print(mvToBoard(mv))


    # print("K: ", k)

    # print("Weight vector: ", w)

    df = pd.DataFrame()

    df["Position"] = array

    df["Weight"] = w

    df["Queen/Column"] = range(k)

    df = df.sort_values("Weight", 0)

    # print("Df: ", df)

    # for i in range(k):
    for i in df["Queen/Column"]:
        ws.append(i)
        # addPos(i, ib, mv)
    tryNextQueen()

    # print("Finished! Found ", len(solutions), " solutions.")
    # print(solutions)


def nextMove(vms, q):
    if not vms:
        ws.append(q)
        return -1  # out of valid moves for a queen, time to go back
    else:  # valid moves remaining so lets try them
        global cc
        cmv[q] = vms.pop()  # adds row to move vector
        addPos(q)  # adds correlated conflicting rows and diagonals
        csc = singleCost(cmv[q], q)  #current single move cost
        cc = cc + csc  # current move cost
        tryNextQueen()  # tries to place next queen
        # if we are here the next queen ran out of valid moves so it is time to try next position,
        removePos(q)  # removes current placement of queen from the board arrays
        cc = cc - csc
        nextMove(vms, q)  # goes to next valid move for current queen (recursion)


def tryNextQueen():
    if not ws:  # no more queens to try which means all queens have successfully been placed
        # print("found a solution! :")
        # print(mvToBoard(cmv))
        solutions.append(copy.deepcopy(cmv)) #appends current move vector as a solution
        # print(cmv)
        c = cost(array, cmv)
        # print("Cost of solution: ", c)

        if c < solution[0] or solution[0] == -1:
            solution[0] = c
            solution[1] = copy.deepcopy(cmv)
    else:
        q = ws.pop()
        # print(q)
        vms = genValidMoves(q) #valid moves for a queen
        nextMove(vms, q) #will recursively try all moves or return


def addPos(q, arr=cb, moveVector=cmv):
    global cmv
    global cb
    arr = cb
    c = q
    # print("cmv", moveVector, cmv)
    r = cmv[c]
    setR(r, c, c, arr)
    setD1(r, c, c, arr)
    setD2(r, c, c, arr)

    #print(arr)

    # arr[0][moveVector[q]] = q
    # arr[1][q + moveVector[q]] = q
    # arr[2][q - moveVector[q] + (k - 1)] = q


def removePos(q, arr=cb, moveVector=cmv):
    global cb
    global cmv
    arr = cb
    moveVector = cmv
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


def checkValid(r, c):  # row and column of new position for queen in column c
    # print(cb)

    # validCost =

    return cb[0][r] is not None or cb[1][r + c] is not None or cb[2][c - r + (k - 1)] is not None


def genMoves(q):
    moves = []
    cr = array[q]  # current row
    x = -1
    moves.append(cr)
    index = x + cr

    while k > index >= 0 and (singleCost(index, q) + cc < solution[0] or solution[0] == -1):  # expand from initial position
        # print("Current queen: ", q, "\nCurrent Row: ", cr, "\nValid Index: ", index)
        moves.append(index)
        if x > 0:
            x = x + 1
        x = x * - 1
        index = x + cr

    x = x * -1
    index = x + cr


    while k > index >= 0 and (singleCost(index, q) + cc < solution[0] or solution[0] == -1):  # expand to edge
        moves.append(index)
        if x > 0:
            x = x + 1
        else:
            x = x - 1
        index = x + cr

    # return list(range(k))  # basic moves
    return moves  # smart moves


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


# board = [1, 1, 1, 1, 1]

#solve([0, 0, 1, 0, 4])

# print("finished, found ", len(solutions), " solutions")




