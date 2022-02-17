import csv
import heapq
import random
import numpy

#@adeline please fill in these functions:
def heuristic(b):
    return random.randint(1, 9)

def cost(base,new):
    return random.randint(1, 9)

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

    def isEmpty(self):
        return len(self.h)==0

size = 0
# load board
with open('HeavyQBoards/test.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)

    size = len(array)

    print(array)
    print(size)

frontier = queueTools()
closed = queueTools();
# add 1st node
est_cost = 0+heuristic(array)
frontier.add(est_cost, array)

print(not frontier.isEmpty())

# while not solved
while True:#not (frontier.isEmpty): #no f-cking clue why this doesnt run, when the print above it does
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
        for k in range(0, size):
            if int(openBoard[k][i]) != 0:
                pos = k
                val = openBoard[k][i]
                print("VAL: "+str(val)+" at "+str(k)+" "+str(i))
                break
        for j in range(0,size): #each row
            if j == pos:                continue
            successor = openBoard
            successor[j][i] = val
            successor[pos][i] = 0
            n=n+1
            print("SUC "+str(n)+" " +str(successor))
            if not closed.exists(successor):#this is the part that doesn't work
                n2=n2+1
                est_cost = cost(array, successor) + heuristic(successor)
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
