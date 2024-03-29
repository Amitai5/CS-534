import csv
import sys
import time
import math
import copy
import heapq
import numpy as np
import random


interval_cost_updates = []
boardArrayXY = []
array = []
w = []
nq = 0
n = 0
best = []
elite = []
ss = []
k = 0
size = 0


def geneticAlg(run_time, should_print):
    global interval_cost_updates
    global array
    global w
    global nq
    global n
    global size
    global ss
    global elite
    global best
    global k

    interval_cost_updates = []
    boardArrayXY = []
    array = []
    w = []
    nq = 0
    n = 0
    best = []
    elite = []
    ss = []
    k = 0
    size = 0

    def makeBoardVector(b):
        for i in range(n):
            for j in range(n):
                if b[j][i] != 0:
                    array.append([i, j])
                    w.append(b[j][i])

    # makeBoardVector(b)

    def generateSuccessor(v):
        s = copy.deepcopy(v)
        for x in range(int(math.sqrt(nq))):  # generate sqrt(#of queen) queens to try and move
            q = random.randint(0, nq - 1)  # queen to move
            ni = random.randint(0, n - 1)  # new row position
            newCoord = [ni, s[q][1]]
            if not (newCoord in s):
                s[q] = newCoord
        return s

    def attacks(b):
        size = n
        numAttacks = 0
        for i in range(n):
            x0 = b[i][0]
            y0 = b[i][1]
            z = int(x0) + 1
            for x in range(z, n):
                if (x, y0) in b:
                    numAttacks += 1
                    # print("row")
            for y in range(y0 + 1, n):
                if [x0, y] in b:
                    numAttacks = numAttacks + 1
                    # print("col")
            for d in range(1, n):
                if [x0 + d, y0 + d] in b:
                    numAttacks = numAttacks + 1
                    # print("d+ "+str(x0+d)+ " "+str(y0+d))
                if [x0 + d, y0 - d] in b:
                    numAttacks = numAttacks + 1
                    # print("d- " + str(x0 + d) + " " + str(y0 - d))
        # print(numAttacks)

        return numAttacks * 100

    def moveCost(v):
        c = 0
        for p in range(0, len(v)):
            c = c + abs(v[p][0] - array[p][0]) * (w[p] ** 2)
            c = c + abs(v[p][1] - array[p][1]) * (w[p] ** 2)
        return c

    def cost(v):
        return attacks(v) + moveCost(v)

    def fit(v):
        return 0 - cost(v)

    def generateSuccessors(v):
        global best
        for i in range(k):  # generate initial successors
            s = generateSuccessor(v)  # successor to add
            sf = fit(s)  # fit of current successor
            s = [s, sf]
            if s not in ss:
                if sf > best[1]:
                    if should_print:
                        print("initial new best found: ", sf)
                    best = copy.deepcopy(s)
                ss.append(s)

    def setElite():  # keep the strongest org
        global best
        global elite
        elite = []
        # sortFit(ss)
        # print("About to sort")
        # print(ss)
        ss.sort(key=lambda x: x[1], reverse=True)
        # print(ss)
        if ss[0][1] > best[1]:
            best = copy.deepcopy(ss[0])
            if should_print:
                print("New best fit: ", best[1])

        for i in range(int(math.sqrt(len(ss)))):
            elite.append(copy.deepcopy(ss[i]))

        if should_print:
            print(elite)
            print(best)

    def cull():  # remove the weakest pop
        for i in range(int(len(ss) / k)):
            if len(ss) != 0:
                ss.pop(-1)

    def checkElite(s):
        s[1] = fit(s[0])
        # print("elite: ", elite)
        if s[1] > elite[-1][1]:
            elite.insert(0, copy.deepcopy(s))

    def sortFit(arr):
        return 0

    def swapColumn(v1, v2, col):
        # v3 = copy.deepcopy(v1)
        # v4 = copy.deepcopy(v2)
        # print(col)
        # print("v1: ", v1, "\nv2: ", v2)
        v1c = []
        v2c = []
        v1c.append(v1[:][col])
        v2c.append(v2[:][col])
        # print("v1c: ", v1c, "\nv2c: ", v2c)
        for i in range(len(v1c)):
            ti = copy.deepcopy(v1c[i])
            ind = v1.index(v1c[i])
            v1[ind] = copy.deepcopy(v2c[i])
            v2[ind] = copy.deepcopy(ti)
        # print("v1: ", v1, "\nv2: ", v2)

    def scramble(s1, s2):
        random.randint(0, 100)
        p1 = s1[1] / (s1[1] + s2[1]) * 100
        p2 = s2[1] / (s1[1] + s2[1]) * 100
        for i in range(n):
            r = random.randint(0, 100)
            if (r <= p1):
                swapColumn(s1[0], s2[0], i)
            elif r >= p2:
                # print("yo")
                mutateCol(s1[0], i)
                mutateCol(s2[0], i)
            checkElite(s1)
            checkElite(s2)
        s1[1] = fit(s1[0])
        s2[1] = fit(s2[0])

        return s1, s2

    def mutateCol(v, col):
        vs = []
        vs.append(v[:][col])
        for i in vs:
            ni = random.randint(0, n - 1)  # new row position
            newCoord = [ni, i[1]]
            if not (newCoord in v):
                i = newCoord

    def vToBoard(v):
        string = ""
        for i in range(n):
            for j in range(n):
                if [i, j] in v:
                    string = string + " " + str(w[v.index([i, j])]) + " "
                else:
                    string = string + " 0 "
                if j == n - 1:
                    string = string + "\n"
        return string

    def checkRealClose():
        m = 0
        for i in range(len(elite)):
            m = m + elite[i][1]
        m = m / len(elite)
        if (m - best[1]) / best[1] < .1 and should_print:
            print("I think we real close")
            print(best[1])
            return True
        else:
            return False


    def recurs():
        global k
        global ss

        setElite()
        cull()
        for i in range(k):
            s1, s2 = random.choices(ss, k=2)
            scramble(s1, s2)
        ss = ss + elite

    with open('board.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        array = list(reader)
        size = len(array)
        n = size

        for i in range(0, size):
            for j in range(0, size):
                array[i][j] = int(array[i][j])

        if should_print:
            print(array)
            print("Size ", size)

        for y in range(0, size):
            for x in range(0, size):
                if array[x][y] != 0:
                    boardArrayXY.append([x, y])
                    w.append(array[x][y])

    # n = len(b)
    array = boardArrayXY
    nq = len(w)
    # starting heuristic cost (for fit calc)
    shc = attacks(array) + moveCost(array)  # cost(array) should be 0
    ss = []  # list of successors
    best = [array, fit(array)]
    ss.append(best)
    k = (n ** 2)  # num successors
    global startk
    startk = copy.deepcopy(k)
    generateSuccessors(array)
    start = time.time()

    has_hit = False
    while time.time() - start < run_time:
        if int(time.time() - start) % 10 == 0 and not has_hit:
            interval_cost_updates.append(cost(best[0]))
            has_hit = True
        elif int(time.time() - start) % 10 != 0 and has_hit:
            has_hit = False
        recurs()

    if should_print:
        print("Finished")
        print(best)
        print("Initial fit: ", fit(array))
        print("Final fit: ", best[1])
        print("Final move cost: ", cost(best[0]))
        print(vToBoard(best[0]))
    return best, cost(best[0])
