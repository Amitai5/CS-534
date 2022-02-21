import csv
import sys
import time
import math
import copy
import heapq
import numpy as np
import random

boardArrayXY = []
array = []
w = []
nq = 0
n = 0
best = []
elite = []
ss = []

with open('HeavyQBoards/Test98.csv', newline='') as csvfile:
    global n
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)

    size = len(array)
    n = size

    for i in range(0, size):
        for j in range(0, size):
            array[i][j] = int(array[i][j])

    print(array)
    print("Size ", size)

    for y in range(0,size):
        for x in range(0, size):
            if array[x][y]!=0:
                boardArrayXY.append((x,y))
                w.append(array[x][y])
print(boardArrayXY)
print(w)



def geneticAlg(b):
    global array
    global w
    global nq
    global n
    global ss
    global elite

    #n = len(b)
    array = b
    nq = len(w)

    def makeBoardVector(b):
        for i in range(n):
            for j in range(n):
                if b[j][i] != 0:
                    array.append([i, j])
                    w.append(b[j][i])

    #makeBoardVector(b)

    def generateSuccessor(v):
        for x in range(int(math.sqrt(nq))): #generate sqrt(#of queen) queens to try and move
            q = random.randint(0, nq - 1)  # queen to move
            ni = random.randint(0, n - 1)  # new row position
            newCoord = (v[q][0], ni)
            if not (newCoord in v):
                v[q] = newCoord
        return v



    def attacks(b):
        numAttacks = 0
        for i in range(size):
            x0 = b[i][0]
            y0 = b[i][1]
            for x in range(x0 + 1, size):
                if (x, y0) in b:
                    numAttacks += 1
                    # print("row")
            for y in range(y0 + 1, size):
                if (x0, y) in b:
                    numAttacks += 1
                    # print("col")
            for d in range(1, size):
                if (x0 + d, y0 + d) in b:
                    numAttacks += 1
                    # print("d+ "+str(x0+d)+ " "+str(y0+d))
                if (x0 + d, y0 - d) in b:
                    numAttacks += 1
                    # print("d- " + str(x0 + d) + " " + str(y0 - d))

        return numAttacks * 100

    def cost(b1):
        c = 0
        for p in range(0, len(b1)):
            c += abs(b1[p][0] - array[p][0]) * (w[p] ** 2)
            c += abs(b1[p][1] - array[p][1]) * (w[p] ** 2)
        return c

    #starting heuristic cost (for fit calc)
    shc = attacks(array) + cost(array) #cost(array) should be 0


    def fit(v):
        return shc - (attacks(v) + cost(v))


    ss = []  # list of successors
    best = fit(array)
    k = 10  # num successors
    def generateSuccessors(v):
        for i in range(k):  # generate initial successors
            s = generateSuccessor(v) #successor to add
            sf = fit(s) #fit of current successor
            s = (s, sf)
            if not s in ss:
                if sf > best[1]:
                    best = s
                ss.append(s)

    def elite(): #keep the strongest pop
        elite = []
        ss.sort(key=lambda x: x[1])
        for i in range(int(sqrt(len(ss)))):
            elite.append(copy.deepcopy(ss[i]))

    def cull(): #remove the weakest pop
        for i in range(int(len(ss) / 2)):
            ss.remove(-i)

    def scramble(s1, s2):
        random.randint(0, 100)
        p1 = s1[1] / (s1[1] + s2[1])
        p2 = s2[1] / (s1[1] + s2[1])
        for i in range(n):
            r = random.randint(0, 100)
            if(r <= p1):
                swapColumn(s1[0], s2[0], i)
            elif r >= p2:
                mutateCol(s1, col)
                mutateCol(s2, col)

        return s1, s2

    def mutateCol(v, col):
        vs = v[:][col]
        for i in vs:
            ni = random.randint(0, n - 1)  # new row position
            newCoord = (v[q][0], ni)
            if not (newCoord in v):
                i = newCoord



    def recurs(v):
        generateSuccessors(v)
        elite()
        cull()
        for i in range (len(ss)):




    # v1: [i, j] [row, col] [[row1, col1] [row1, col1] [row 2, col2]]
    # swap columns without needing to return, ideally. TODO: check
    def swapColumn(v1, v2, col):
        v3 = copy.deepcopy(v1)
        v4 = copy.deepcopy(v2)
        v1[:, col] = v4[:, col]
        v2[:, col] = v3[:, col]

geneticAlg(boardArrayXY)