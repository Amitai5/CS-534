import sys
import random
import numpy as np


def create_board_csv(size, file_name, should_print):
    if should_print:
        print('Size:', str(size))
        print('File:', file_name)

    arr = np.zeros((size, size))
    for x in range(0, size):
        pos = random.randint(0, size - 1)
        weight = random.randint(1, 9)
        arr[pos][x] = weight

        if should_print:
            print("generated position: " + str(pos) + " and weight " + str(weight))

    # num extra queens
    extra = int(size / 8)
    if should_print:
        print("Extra: " + str(extra))

    while extra > 0:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        weight = random.randint(1, 9)
        if arr[x][y] == 0:  # if valid empty space, add new queen
            arr[x][y] = weight
            extra -= 1

    if should_print:
        print(arr)

    np.savetxt("HeavyQBoards/" + file_name, arr, fmt='%i', delimiter=',')
