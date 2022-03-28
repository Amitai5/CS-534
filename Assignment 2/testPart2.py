import SearchAlgorithmsNN
import SearchAlgorithms
import BoardWrite as bw
import numpy as np
import part2
import tqdm

batch_size = 4
max_board_size = 30
part2_time_batch = []
part2_cost_batch = []


def printResults(time_results, cost_results):
    time_result = np.round(np.mean(time_results, axis=0), 4)
    cost_result = np.round(np.mean(cost_results, axis=0), 4)
    cost_results = []
    time_results = []

    print("- " + " Elapsed Time: " + str(time_result) + " sec")
    print("- " + " Cost: " + str(cost_result))


print("Testing...")
for i in range(4, max_board_size):
    for j in range(batch_size):
        test_board = bw.create_board(i, False)
        part2_elapsed_time, part2_cost, _ = part2.findSolution(test_board, False)
        part2_time_batch.append(part2_elapsed_time)
        part2_cost_batch.append(part2_cost)

    print("\nBoard Size: " + str(i))
    printResults(part2_time_batch, part2_cost_batch)
