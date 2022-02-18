import sys
import numpy as np
import random

print( 'Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))

print( 'Size:', str(sys.argv[1]))
print('File:', str(sys.argv[2]))

size = int(sys.argv[1]);

arr = np.zeros((size, size));

for x in range(0, size):
    pos = random.randint(0, size-1)
    weight = random.randint(1, 9)
    print("generated position: "+str(pos)+" and weight "+str(weight))
    arr[pos][x]=weight

print( arr)

np.savetxt("HeavyQBoards/"+str(sys.argv[2])+'.csv', arr, fmt='%i', delimiter=',')