import csv
import heapq
import random
import numpy
import copy
import sys
import time
import math

def attacks(b):
    numAttacks = 0
    for i in range(size):
        x0 = b[i][0]
        y0 = b[i][1]
        for x in range(x0+1,size):
            if (x,y0) in b:
                numAttacks+=1
                #print("row")
        for y in range(y0+1, size):
            if (x0, y) in b:
                numAttacks += 1
                #print("col")
        for d in range(1, size):
            if (x0+d, y0+d) in b:
                numAttacks += 1
                #print("d+ "+str(x0+d)+ " "+str(y0+d))
            if (x0+d, y0-d) in b:
                numAttacks += 1
                #print("d- " + str(x0 + d) + " " + str(y0 - d))

    return numAttacks



# load board
boardArrayXY=[]
boardWeight = []

with open('HeavyQBoards/Test98.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)

    size = len(array)

    for i in range(0, size):
        for j in range(0, size):
            array[i][j] = int(array[i][j])

    print(array)
    print("Size ", size)

    for y in range(0,size):
        for x in range(0, size):
            if array[x][y]!=0:
                boardArrayXY.append((x,y))
                boardWeight.append(array[x][y])
print(boardArrayXY)
print(boardWeight)

solution = (0, attacks(boardArrayXY),boardArrayXY)

start = time.time()
while(time.time()-start < int(sys.argv[1])): #less time elapsed than total
    print("running")
    lastCost = -1
    tempSolution = (0,0,0);
    openBoard = copy.deepcopy(boardArrayXY);
    print(openBoard)
    #random moves here ----
    #---

    while lastCost == -1 or tempSolution[1]-lastCost >= 0:#run while improvements happen
        h = []
        n = 0
        print("Continue")
        lastCost = attacks(openBoard)

        for i in range(0,len(openBoard)):  # each column
            pos = openBoard[i][1]
            for j in range(-int(math.sqrt(size)), int(math.sqrt(size)) + 1):  # each row
                if j == 0 or pos + j == size or pos - j < 0 or ((openBoard[i][0], pos+j) in openBoard):
                    continue
                successor = copy.deepcopy(openBoard)
                successor[i] = (openBoard[i][0], pos + j)
                n = n + 1

                heapq.heappush(h, (attacks(successor), successor))

        print("Successors " + str(n) + " added")
        best = heapq.heappop(h)
        print(best)
        tempSolution = (0, best[0], best[1])
        if solution[1] > tempSolution[1]:
            solution = tempSolution

        openBoard = tempSolution[2]
        print(openBoard)
        print(tempSolution[1])
        print(lastCost)

    print("RESET")

print(attacks(boardArrayXY))
print(solution[1])

#a = [(5,6),(2,3),(4,5)]
#b = (2,4)
#print(b in a)

# ' Wrapper for a HeapQ, mainly provides an "exists" function that tells wheteher a board exists in queue
#class queueTools:
   # def __init__(self):
      #  self.h = []

    #def add(self, p, item):
       # heapq.heappush(self.h, (p, item))

   # def get(self):
       # return heapq.heappop(self.h)

   # def len(self):
#   return len(self.h)