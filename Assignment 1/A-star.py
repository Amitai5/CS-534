import csv
import heapq
import random
import numpy

#@adeline please fill in these functions:
import numpy as np


def heuristic(b):
    v = moveVector(b) #move vector and row vector
    w = weightVector(b) #weight vector
    d1 = diag1Vector(v) #diag1 vector
    d2 = diag2Vector(v) #diag2 vector

    print("move vector: ", v)
    print("weight vector: ", w)
    print("d1 vector: ", d1)
    print("d2 vector: ", d2)

    hc = 0

    for i in range(size):
        for j in range(size - i):
            if v[i] == v[j + i]:
                hc = hc + w[i] + w[j + i]
            if d1[i] == d1[i + j]:
                hc = hc + w[i] + w[j + i]
            if d2[i] == d2[i + j]:
                hc = hc + w[i] + w[j + i]
    print("hc: ", hc)
    return hc

def cost(base,new):
    b = moveVector(base)
    n = moveVector(new)
    w = weightVector(base)

    moveCost = np.absolute(np.array(b) - np.array(n))
    moveCost = moveCost * w
    moveCost = moveCost.sum()

    return moveCost

def getBoardString(b):
    mv = moveVector(b)
    bString = ""
    for i in mv:
        bString = bString + str(i)
    return bString

def moveVector(b):
    x = []
    for i in range(size):
        for j in range(size):
            if b[j][i] != 0:
                x.append(j)
    #print("Move vector: ", x)
    return x

def weightVector(b):
    x = []
    for i in range(size):
        for j in range(size):
            if b[i][j] != 0:
                x.append(int(b[i][j]))
    #print(x)
    return x

def diag1Vector(mv):
    d1 = []
    for i in range(size):
        d1.append(i - mv[i])
    #print(d1)
    return d1

def diag2Vector(mv):
    d2 = []
    for i in range(size):
        d2.append(i + mv[i])
    #print(d2)
    return d2


# ' Wrapper for a HeapQ, mainly provides an "exists" function that tells wheteher a board exists in queue
class queueTools:
    def __init__(self):
        self.h = []

    def add(self, p, item):
        heapq.heappush(self.h, (p, item))

    def get(self):
        return heapq.heappop(self.h)

    #Yes, I copied this from stackoverflow: https://stackoverflow.com/questions/18181818/python-priority-queue-checking-to-see-if-item-exists-without-looping
    #and it doesnt work, need to figure out a reasonable check
    def exists(self, item):
        return item in (x[1] for x in self.h)

    def len(self):
        return len(self.h)

size = 0
# load board
with open('HeavyQBoards/test.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)
    #array = int(array)



    size = len(array)

    for i in range(0, size):
        for j in range(0, size):
            array[i][j] = int(array[i][j])
            print(array[i][j])

    print(array)
    print("Size ", size)

frontier = queueTools()
closed = queueTools();
closedList = [];
# add 1st node
est_cost = 0+heuristic(array)
frontier.add(est_cost, array)
closedList.append(getBoardString(array))

print(frontier.len())

# while not solved
while frontier.len():
# open lowest cost
    print("get")
    b = frontier.get();
    openBoard = b[1]
    print(b);
    print(frontier.exists(b))
    # switch it to closed
    closed.add(b[0], [b[1]])

    n=0
    n2=0
    # Generate successors - I think this works well (or at least passably, not 100% sure), except that the comparison is always false , not actually checking array elements
    for i in range(0,size):#each column
        print("arr"+str(i))
        pos = 0
        val = 0
        for k in range(0, size-1):
            if int(openBoard[k][i]) != 0:
                pos = k
                val = openBoard[k][i]
                #print("VAL: "+str(val)+" at "+str(k)+" "+str(i))
                break
        for j in range(0,size-1): #each row
            if j == pos:
                continue
            successor = openBoard
            successor[j][i] = val
            successor[pos][i] = 0
            n=n+1
            print("SUC "+str(n)+" " +str(successor))
            sucString = getBoardString(successor)
            if not sucString in closedList:#this is the part that doesn't work
                closedList.append(sucString)
                n2=n2+1
                h = heuristic(successor);
                if(h==0):
                    exit();
                est_cost = cost(array, successor) + h
                frontier.add(est_cost, successor)

    print("Successors "+str(n)+" added "+str(n2))
    # If solved exit
    # break

# Test code
# q.put( (10, 4) )
# q.put( (10, 2) )
# q.put( (1, 3) )
# q.put( (2, 6) )
# while not q.empty():
#   print(q.get())


def solveQueens(self, n: int) -> List[List[str]]:
    col = set()
    posDiag = set()  # (r + c)
    negDiag = set()  # (r - c)


res = []
board = [["."] * n for i in range(n)]


def backtrack(r):
    if r == n:
        copy = ["".join(row) for row in board]
        res.append(copy)
        return

        for c in range(n):
            if c in col or (r + c) in posDiag or (r - c) in negDiag:
                continue

            col.add(c)
            posDiag.add(r + c)
            negDiag.add(r - c)
            board[r][c] = "Q"

            backtrack(r + 1)

            col.remove(c)
            posDiag.remove(r + c)
            negDiag.remove(r - c)
            board[r][c] = "Q"
    backtrack(0)
    return res
