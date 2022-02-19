import csv
import sys
import time
import copy
import heapq
import numpy as np


def heuristic(b):
    # w = weightVector(b) #weight vector
    d1 = diag1Vector(b)  # diag1 vector
    d2 = diag2Vector(b)  # diag2 vector
    hc = 0

    for i in range(size):
        for j in range(1, size - i):
            if b[i] == b[j + i]:
                hc = hc + w[i] + w[j + i]
            if d1[i] == d1[i + j]:
                hc = hc + w[i] + w[j + i]
            if d2[i] == d2[i + j]:
                hc = hc + w[i] + w[j + i]
    return hc


def cost(base, new):
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
    d1 = []
    for i in range(size):
        d1.append(i - mv[i])
    return d1


def diag2Vector(mv):
    d2 = []
    for i in range(size):
        d2.append(i + mv[i])
    return d2


def mvToBoard(mv):
    string = ""
    for i in range(size):
        for j in range(size):
            if mv[i] == j:
                string = string + " " + str(w[i]) + " "
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


# Main code
greedy = int(sys.argv[1])
start_time = time.time()

size = 0
w = []

# load board
with open('HeavyQBoards/test.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    array = list(reader)
    size = len(array)

    for i in range(0, size):
        for j in range(0, size):
            array[i][j] = int(array[i][j])

    print("Size ", size)
    w = weightVector(array)
    print("Weight Vector: ", w)

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
    if b is None:
        print("Search over")
        exit()
    if solution[0] != -1 and (b[0] > solution[0] or greedy == 1):
        print("Search Complete...")
        print("\n\n---------------Search Results---------------")
        print("Board Size: ", size)
        board_string = mvToBoard(solution[1])
        print("Board: \n" + board_string + "\n")

        if greedy == 1:
            print("Greedy search")
            print("Cost: " + str(cost(array, solution[1])) + "\n")
        else:
            print("A* search")
            print("Cost: " + str(solution[0]))

        elapsed_time = time.time() - start_time
        print("Time Elapsed: " + str(round(elapsed_time, 5)) + " sec.")
        text_file = open("HeavyQBoards/ANSWER.txt", "w")
        n = text_file.write(board_string)
        text_file.close()
        exit()
    openBoard = b[1]

    # switch it to closed
    closed.add(b[0], [b[1]])
    n2 = 0
    n = 0

    # Generate successors
    for i in range(0, size):  # each column
        pos = 0
        val = 0
        pos = openBoard[i]
        val = w[i]
        for j in range(0, size):  # each row
            if j == pos:
                continue
            successor = copy.deepcopy(openBoard)
            successor[i] = j
            n = n + 1
            sucString = getBoardString(successor)
            if not sucString in closedList:  # Works now
                closedList.append(sucString)
                n2 = n2 + 1
                h = heuristic(successor)
                c = 0
                if greedy != 1:
                    c = cost(array, successor)
                if h == 0:
                    print("FOUND")
                    if solution[0] == -1 or c < solution[0]:  # Replace solution if cheaper
                        solution = (c, successor)
                else:
                    est_cost = c + h
                    frontier.add(est_cost, successor)

    print("Successors " + str(n) + " added " + str(n2) + " new nodes")
    # If solved exit
    # break
