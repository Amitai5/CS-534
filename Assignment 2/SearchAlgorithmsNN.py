import os
import csv
import sys
import time
import math
import copy
import heapq
import torch
import pandas
import numpy as np
import statistics

model_file = os.getcwd() + "\\models\\neural_network_1.pkl"
neural_network = pandas.read_pickle(model_file)
neural_network.to("cpu")
size = 0
w = []


# Use the neural network here
def heuristic(b):
    global size  # size of board MUST BE 6 as is it is written now
    global w  # weights of queens
    features = []
    # I pull the features from the boards here - you can use these for the NN
    # Create features, first 12 are row of queen in column, weight of queen in row
    totalWeight = 0
    totalAttackWeight = 0
    numAttQueens = 0
    heaviestAttacking = 0

    # add each position to feature list (1st 12) - 1D board here
    board = mvTo2DBoard(b)
    for i in range(len(board)):
        for j in range(len(board)):
            # features.append(board[j][i]/9)
            totalWeight += board[j][i]

    rowPos = b
    for i in range(len(board)):
        myRow = rowPos[i]
        # check for attacks
        for j in range(i + 1, 6):
            if rowPos[j] == myRow or rowPos[j] == myRow + (j - i) or rowPos[j] == myRow - (j - i):
                numAttQueens += 1
                heaviestAttacking = max(heaviestAttacking, board[myRow][i], board[rowPos[j]][j])
                totalAttackWeight += board[myRow][i] + board[rowPos[j]][j]

    # Add last 5 derived features
    features.append(totalAttackWeight / totalWeight)
    features.append(numAttQueens)
    features.append(statistics.stdev(b))
    features.append(heaviestAttacking)
    features.append(totalWeight)

    sanitized_features = torch.Tensor(features)

    with torch.no_grad():
        result = neural_network.forward(sanitized_features).detach().numpy()
    return round(result[0] * 712) * (numAttQueens != 0)


def heuristic2(b):
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
    global size
    global w

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


def mvTo2DBoard(mv):
    global size
    global w

    counter = 0
    board = np.zeros((6, 6), dtype=float)
    for i in mv:
        board[i][counter] = w[counter]
        counter += 1
    return board


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


def findSolution(array, use_nn, should_print):
    start_time = time.time()
    heuristic_times = []
    is_greedy = False
    total_opened = 0
    total_added = 0
    global size
    global w

    # load board
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
            return elapsed_time, cost(array, solution[1]), heuristic_times

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
                    h_start_time = time.time_ns()
                    if use_nn:
                        h = heuristic(successor)
                    else:
                        h = heuristic2(successor)
                    heuristic_times.append(time.time_ns() - h_start_time)

                    if should_print:
                        print("Heuristic: ", h)
                        print("Heuristic2: ", heuristic2(successor))
                        print("")
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
            # print("Successors " + str(n) + " added " + str(n2) + " new nodes")
        # If solved exit
        # break
