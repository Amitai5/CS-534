import SearchAlgorithmsNN
import BoardWrite as bw
import numpy as np

astar_time_batch = []
astar_cost_batch = []
astar_branching_batch = []

nn_astar_time_batch = []
nn_astar_cost_batch = []
nn_astar_branching_batch = []

batch_size = 3
board_size = 6
board_count = 12


def printResults(name, time_results, branching_results, cost_results):
    branching_result = np.round(np.mean(branching_results, axis=0), 3)
    time_result = np.round(np.mean(time_results, axis=0), 3)
    cost_result = np.round(np.mean(cost_results, axis=0), 3)

    print("- " + name + " Elapsed Time: " + str(time_result) + " sec.")
    print("- " + name + " Branching Factor: " + str(branching_result))
    print("- " + name + " Cost: " + str(cost_result))


def run_both_algos(test_board):
    nn_astar_elapsed_time, nn_astar_cost, nn_astar_branching = SearchAlgorithmsNN.findSolution(test_board, True, False)
    nn_astar_branching_batch.append(nn_astar_branching)
    nn_astar_time_batch.append(nn_astar_elapsed_time)
    nn_astar_cost_batch.append(nn_astar_cost)

    astar_elapsed_time, astar_cost, astar_branching = SearchAlgorithmsNN.findSolution(test_board, False, False)
    astar_branching_batch.append(astar_branching)
    astar_time_batch.append(astar_elapsed_time)
    astar_cost_batch.append(astar_cost)


print("---------------Test Results---------------")
print("Batch Size: " + str(batch_size) + "\n")

for i in range(4, board_count + 1):
    print("Board Size: " + str(i))
    for j in range(0, batch_size):
        board = bw.create_board(6, False)
        run_both_algos(board)

printResults("A* (Neural Network)", nn_astar_time_batch, nn_astar_branching_batch, nn_astar_cost_batch)
printResults("A*", astar_time_batch, astar_branching_batch, astar_cost_batch)
print("")