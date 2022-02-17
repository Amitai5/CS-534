import csv
import queue
import heapq

#@adeline please fill in these functions:
def heuristic(b):
    return 4

def cost(base,new):
    return 0

# ' Wrapper for a HeapQ, mainly provides an "exists" function that tells wheteher a board exists in queue
class queueTools:
    def __init__(self):
        self.h = []

    def add(self, p, item):
        heapq.heappush(self.h, (p, item))

    def get(self):
        return heapq.heappop(self.h)

    def exists(self, item):
        return item in (x[1] for x in self.h)


# load board
with open('HeavyQBoards/test.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    array = list(reader)

    size = len(array)

    print(array)
    print(size)

frontier = queueTools()
# add 1st node
cost = 0+heuristic(array)
frontier.add(cost, array)

# while not solved
# while True:
# open lowest cost
b = frontier.get()[1];
print(b);
print(frontier.exists(b))
# switch it to closed


# Generate successors
# for i in range(1,size):
# total est = getMoveCost(array,successor)+heuristic(successor)
# print(i,array[i][i]);

# If solved exit
# break

# Test code
# q.put( (10, 4) )
# q.put( (10, 2) )
# q.put( (1, 3) )
# q.put( (2, 6) )
# while not q.empty():
#   print(q.get())
