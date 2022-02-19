import csv
import heapq
import random
import numpy
import copy
import sys
import time

def attacks(b):
    numAttacks = 0
    for i in range(size):
        for(b[i][0] in b):

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
    h = []
    print("running")
    for i in boardArrayXY:
        #rows
        print("Rows")
        #cols
        print("Cols")
        #diag


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