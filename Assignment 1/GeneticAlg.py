import csv
import sys
import time
import math
import copy
import heapq
import numpy as np
import random

array
w

def geneticAlg(b):
    global array
    global w

    n = leb(b)
    array = []
    w = []
    def makeBoardVector(b):
        for i in range(n):
            for j in range(n):
                if b[j][i] != 0:
                    array.append([i, j])
                    w.append(b[j][i])

    makeBoardVector(b)

    def generateSuccessors(v):
        for x in range(int(sqrt(v.len))):
            i = random.randint(0, n - 1)


    def swapColumn(v1, v2, col):
        for i in range(len(v1)):
            





