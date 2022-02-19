import csv
import heapq
import random
import numpy
import copy
import sys

#@adeline please fill in these functions:
import numpy as np


def heuristic(b):
     #move vector and row vector
    #w = weightVector(b) #weight vector
    d1 = diag1Vector(b) #diag1 vector
    d2 = diag2Vector(b) #diag2 vector

   # print("move vector: ", v)
    #print("weight vector: ", w)
    #print("d1 vector: ", d1)
   # print("d2 vector: ", d2)

    hc = 0

    for i in range(size):
        for j in range(1, size - i):
            if b[i] == b[j + i]:
                hc = hc + w[i] + w[j + i]
            if d1[i] == d1[i + j]:
                hc = hc + w[i] + w[j + i]
            if d2[i] == d2[i + j]:
                hc = hc + w[i] + w[j + i]
    #print("hc: ", hc)
    return hc

def cost(base,new):
    b = base
    n = new
    #w = weightVector(base)

    #print("Base: ", base)
    #print("new: ", new)

    #print("b: ", b)
    #print("n: ", n)

    moveCost = np.absolute(np.array(b) - np.array(n))
    #print("Move cost: ", moveCost)
   # print("w^2: ", np.square(np.array(w)))
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
    #print("Move vector: ", x)
    return x

def weightVector(b):
    x = []
    for i in range(size):
        for j in range(size):
            if b[j][i] != 0:
                x.append(int(b[j][i]))
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

def mvToBoard(mv):
    string = ""
    for i in range(size):
        for j in range(size):
            if mv[i] == j:
                string = string + " " +str(w[i]) + " "
            else:
                string = string + " 0 "
            if j == size - 1:
                string = string + "\n"
    return string



# ' Wrapper for a HeapQ, mainly provides an "exists" function that tells wheteher a board exists in queue
class queueTools:
    def __init__(self):
        self.h = []

    def add(self, p, item):
        heapq.heappush(self.h, (p, item))

    def get(self):
        return heapq.heappop(self.h)

    def len(self):
        return len(self.h)


#Main code
greedy = int(sys.argv[1])

size = 0
w = []
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
    print(range(size))
    w = weightVector(array)
    print(w)

array = moveVector(array)

frontier = queueTools()
closed = queueTools() #maybe delete
solution = (-1,array)
closedList = []
# add 1st node
est_cost = 0+heuristic(array)
frontier.add(est_cost, array)
closedList.append(getBoardString(array))

# while not solved
while frontier.len():
# open lowest cost
    print("get")
    b = frontier.get();
    if b is None:
        print("Search over")
        exit()
    if solution[0] != -1 and (b[0] > solution[0] or greedy == 1):
        print("Search complete\n")
        if greedy == 1:
            print("Greedy search")
            print("Cost: " + str(cost(array,solution[1])) + "\n")
        else:
            print("A* search")
            print("Greedy: "+str(sys.argv[1]))
            print("Cost: "+str(solution[0])+"\n")
        print("Solution position vector:\n"+str(solution[1]))
        stringSol = mvToBoard(solution[1])
        print(stringSol)
        text_file = open("HeavyQBoards/ANSWER.txt", "w")
        n = text_file.write(stringSol)
        text_file.close()

        #np.savetxt("HeavyQBoards/ANSWER.csv", stringSol, fmt='%i', delimiter=',')
        exit()
    openBoard = b[1]
    print(b);
    #print(frontier.exists(b))
    # switch it to closed
    closed.add(b[0], [b[1]])

    n=0
    n2=0
    # Generate successors - I think this works well (or at least passably, not 100% sure), except that the comparison is always false , not actually checking array elements
    for i in range(0,size):#each column
        pos = 0
        val = 0
        pos = openBoard[i]
        val = w[i];
        for j in range(0,size): #each row
            if j == pos:
                continue
            successor = copy.deepcopy(openBoard)
            successor[i] = j
            n=n+1
            #print("SUC "+str(n)+" " +str(successor))
            sucString = getBoardString(successor)
            if not sucString in closedList:#Works now
                closedList.append(sucString)
                n2 = n2+1
                h = heuristic(successor)
                c = 0
                if greedy != 1:
                    #print("A*")
                    c = cost(array, successor)
                print("h: "+str(h)+" c: "+str(c))
                if h == 0:
                    print("FOUND")
                    #Replace solution if cheaper
                    if solution[0] == -1 or c<solution[0]:
                        solution = (c, successor)
                else:
                    est_cost = c + h
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


#<<<<<<< HEAD
# def solveQueens(self, n: int) -> List[List[str]]:
#     col = set()
#     posDiag = set()  # (r + c)
#     negDiag = set()  # (r - c)
#
#
# res = []
# board = [["."] * n for i in range(n)]
#
#
# def backtrack(r):
#     if r == n:
#         copy = ["".join(row) for row in board]
#         res.append(copy)
#         return
#
#         for c in range(n):
#             if c in col or (r + c) in posDiag or (r - c) in negDiag:
#                 continue
#
#             col.add(c)
#             posDiag.add(r + c)
#             negDiag.add(r - c)
#             board[r][c] = "Q"
#
#             backtrack(r + 1)
#
#             col.remove(c)
#             posDiag.remove(r + c)
#             negDiag.remove(r - c)
#             board[r][c] = "Q"
#     backtrack(0)
#     return res
# =======
# def solveQueens(self, n: int) -> list[list[str]]:
#     col = set()
#     posDiag = set()  # (r + c)
#     negDiag = set()  # (r - c)
#
#
# res = []
# board = [["."] * n for i in range(n)]
#
#
# def backtrack(r):
#     if r == n:
#         copy = ["".join(row) for row in board]
#         res.append(copy)
#         return
#
#         for c in range(n):
#             if c in col or (r + c) in posDiag or (r - c) in negDiag:
#                 continue
#
#             col.add(c)
#             posDiag.add(r + c)
#             negDiag.add(r - c)
#             board[r][c] = "Q"
#
#             backtrack(r + 1)
#
#             col.remove(c)
#             posDiag.remove(r + c)
#             negDiag.remove(r - c)
#             board[r][c] = "Q"
#     backtrack(0)
#     return res
# >>>>>>> main
