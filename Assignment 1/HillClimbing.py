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

    return numAttacks*100


def cost(b1):
    c = 0
    for p in range(0, len(b1)):
        c += abs(b1[p][0]-boardArrayXY[p][0])*boardWeight[p]**2
        c += abs(b1[p][1] - boardArrayXY[p][1]) * boardWeight[p] ** 2
    return c


#Generate string for board
def boardstring(b):
    arr = numpy.zeros((size, size), dtype=int)
    for i in range(0, len(b)):
        arr[b[i][0]][b[i][1]] = boardWeight[i]
        #print(arr)
    return str(arr)


# load board
boardArrayXY = []
boardWeight = []

#parameters for search
minIncrease = 75 #How much the solution must be improved to keep climbing instead of restarting
sideMoves = 1 #how many horizontal moves to make - seems to make it worse, maybe 1 is better, but any larger seems to average worse

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
numBoards = 1
while(time.time()-start < int(sys.argv[1])): #less time elapsed than total
    print("running")
    lastCost = -1
    tempSolution = (0,0,0);
    openBoard = copy.deepcopy(boardArrayXY);

    #random moves here
    nrand = random.randint(0, size-1)#Can tune this paremeter, how many attempts to move a queen
    while nrand>0:
        n = random.randint(0, len(openBoard)-1)
        y = random.randint(0, size-1)
        newCoord = (y, openBoard[n][1])
        if not (newCoord in openBoard):
            nrand -= 1
            openBoard[n] = newCoord
    # Sideways moves
    nrand = sideMoves # Can tune this parameter, how many queens moved sideways
    while nrand > 0:
        n = random.randint(0, len(openBoard) - 1)
        x = random.randint(0, size - 1)
        newCoord = (openBoard[n][1], x)
        if not (newCoord in openBoard):
            nrand -= 1
            openBoard[n] = newCoord

    while lastCost == -1 or lastCost-tempSolution[1] > minIncrease:#run while improvements happen
        h = []
        n = 0
        if(lastCost!=-1):
            print("Continue: gain of "+str(lastCost-tempSolution[1]))
        lastCost = attacks(openBoard)+cost(openBoard)

        for i in range(0,len(openBoard)):  # each column
            pos = openBoard[i][1]
            for j in range(-int(math.sqrt(size)), int(math.sqrt(size)) + 1):  # each row
                if j == 0 or pos + j >= size or pos + j < 0 or ((pos+j, openBoard[i][1]) in openBoard):
                    continue
                successor = copy.deepcopy(openBoard)
                successor[i] = (pos+j, openBoard[i][1])
                n = n + 1
                heapq.heappush(h, (attacks(successor)+cost(successor), successor))

        #print("Successors " + str(n) + " added")
        best = heapq.heappop(h)

        tempSolution = (0, best[0], best[1])
        if solution[1] > tempSolution[1]:
            solution = tempSolution

        openBoard = tempSolution[2]

    print("RESET")
    numBoards += 1

print("COMPLETE")
print("Number of boards climbed: " + str(numBoards))
print("Starting board attacks: "+ str(attacks(boardArrayXY)))
print("Final board cost: "+str(solution[1]))
print(boardArrayXY)
print(solution[2])
print(boardstring(solution[2]))
#print(boardWeight)


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