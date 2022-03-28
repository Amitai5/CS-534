import numpy as np
import random


def create_board_csv(size, file_name, should_print):
    if should_print:
        print('Size:', str(size))
        print('File:', file_name)
    arr = np.zeros((size, size))

    for x in range(0, size):
        pos = random.randint(0, size - 1)
        weight = random.randint(1, 9)
        if should_print:
            print("generated position: " + str(pos) + " and weight " + str(weight))
        arr[pos][x] = weight
    np.savetxt(file_name, arr, fmt='%i', delimiter=',')