
import csv
import sys
import time
import math
import copy
import heapq
import numpy as np

# create globals
from csvwrite import create_board_csv

use_modified_heuristic = False
size = 0
w = []


def heuristic(b):
    global size
    global w

    # w = weightVector(b) #weight vector
    d1 = diag1Vector(b)  # diag1 vector
    d2 = diag2Vector(b)  # diag2 vector
    hc = 0

    for i in range(size):
        for j in range(i + 1, size):
            if b[i] == b[j]:
                hc +=1;
            if d1[i] == d1[j]:
                hc +=1;
            if d2[i] == d2[j]:
                hc +=1;
    if use_modified_heuristic:
        return hc * math.sqrt(size)
    return hc


def cost(base, new):
    global size
    global w

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


def diag1Vector(mv):
    global size
    global w

    d1 = []
    for i in range(size):
        d1.append(i - mv[i])
    return d1


def diag2Vector(mv):
    global size
    global w

    d2 = []
    for i in range(size):
        d2.append(i + mv[i])
    return d2


def mvToBoard(mv):
    size = k
    w = []
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
class queueTools:
    def __init__(self):
        self.h = []

    def add(self, p, item):
        heapq.heappush(self.h, (p, item))

    def get(self):
        return heapq.heappop(self.h)

    def len(self):
        return len(self.h)


def findSolution(is_greedy, should_print):
    start_time = time.time()
    total_opened = 0
    total_added = 0
    global size
    global w

    # load board
    with open('board.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        array = list(reader)
        size = len(array)

        for i in range(0, size):
            for j in range(0, size):
                array[i][j] = int(array[i][j])
        w = weightVector(array)

    array = moveVector(array)
    frontier = queueTools()
    closed = queueTools()  # maybe delete
    solution = (-1, array)
    closedList = []

    # add 1st node
    est_cost = 0 + heuristic(array)
    frontier.add(est_cost, array)
    closedList.append(getBoardString(array))

    # while not solved
    while frontier.len():
        b = frontier.get()
        total_opened += 1
        if b is None:
            if should_print:
                print("Search over")
            return -1
        if solution[0] != -1 and (b[0] > solution[0] or is_greedy == 1):
            board_string = mvToBoard(solution[1])
            elapsed_time = time.time() - start_time
            if should_print:
                print("Search Complete...")
                print("\n\n---------------Search Results---------------")
                print("Board Size: ", size)
                print("Board: \n" + board_string + "\n")
                if is_greedy == 1:
                    print("Greedy search")
                    print("Cost: " + str(cost(array, solution[1])) + "\n")
                else:
                    print("A* search")
                    print("Cost: " + str(solution[0]))
                print("Time Elapsed: " + str(round(elapsed_time, 5)) + " sec.")

            text_file = open("ANSWER.txt", "w")
            n = text_file.write(board_string)
            text_file.close()
            return elapsed_time, cost(array, solution[1]), (total_opened / total_added) * math.pow(size, 2)

        openBoard = b[1]
        closed.add(b[0], [b[1]])
        n2 = 0  # num succ adding
        n = 0  # num solutions

        # Generate successors
        for i in range(0, size):  # each column
            total_added += 1
            pos = 0
            val = 0
            pos = openBoard[i]
            val = w[i]
            for j in range(-int(math.sqrt(size)), int(math.sqrt(size)) + 1):  # each row
                if j == 0 or pos + j >= size or pos + j < 0:
                    continue
                successor = copy.deepcopy(openBoard)
                successor[i] = pos + j

                n = n + 1
                sucString = getBoardString(successor)
                if not sucString in closedList:
                    closedList.append(sucString)
                    n2 = n2 + 1
                    h = heuristic(successor)
                    c = 0
                    if is_greedy != 1:
                        c = cost(array, successor)
                    if h == 0:
                        if should_print:
                            print("FOUND")
                        if solution[0] == -1 or c < solution[0]:  # Replace solution if cheaper
                            solution = (c, successor)
                    else:
                        frontier.add(c + h, successor)
        if should_print:
            print("Successors " + str(n) + " added " + str(n2) + " new nodes")
        # If solved exit
        # break


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


def solve(mv):
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
        solutions.append(cmv.copy) #appends current move vector as a solution
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

solve([0, 0, 1, 0, 4])

for i in solutions:
    #print(mvToBoard(i))
    print("yo\n")
print("finished, found ", len(solutions), " solutions")




