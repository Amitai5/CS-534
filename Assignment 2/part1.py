import SearchAlgorithmsNN
import SearchAlgorithms
import BoardWrite as bw
import numpy as np
import tqdm

astar_time_batch = []
astar_cost_batch = []
astar_heuristic_times_batch = []

m_astar_time_batch = []
m_astar_cost_batch = []
m_astar_heuristic_times_batch = []

nn_astar_time_batch = []
nn_astar_cost_batch = []
nn_astar_heuristic_times_batch = []

batch_size = 30
board_size = 6
board_count = 12


print("\nTesting Parameters:")
print("Board Size: " + str(board_size))
print("Batch Size: " + str(batch_size) + "\n")


def printResults(name, time_results, heuristic_times, cost_results):
    heuristic_time = np.round(np.mean(heuristic_times, axis=0) / 1000, 3)
    time_result = np.round(np.mean(time_results, axis=0), 3)
    cost_result = np.round(np.mean(cost_results, axis=0), 3)

    print("- " + name + " Heuristic Calculation Time: " + str(heuristic_time) + " μs")
    print("- " + name + " Elapsed Time: " + str(time_result) + " sec")
    print("- " + name + " Cost: " + str(cost_result))


def run_algos(test_board):
    nn_astar_elapsed_time, nn_astar_cost, nn_astar_heuristic_times = SearchAlgorithmsNN.findSolution(test_board, True, False)
    nn_astar_heuristic_times_batch.append(np.mean(nn_astar_heuristic_times, axis=0))
    nn_astar_time_batch.append(nn_astar_elapsed_time)
    nn_astar_cost_batch.append(nn_astar_cost)

    m_astar_elapsed_time, m_astar_cost, m_astar_heuristic_times = SearchAlgorithms.findSolution(test_board, False, False)
    m_astar_heuristic_times_batch.append(np.mean(m_astar_heuristic_times, axis=0))
    m_astar_time_batch.append(m_astar_elapsed_time)
    m_astar_cost_batch.append(m_astar_cost)

    astar_elapsed_time, astar_cost, astar_heuristic_times = SearchAlgorithmsNN.findSolution(test_board, False, False)
    astar_heuristic_times_batch.append(np.mean(astar_heuristic_times, axis=0))
    astar_time_batch.append(astar_elapsed_time)
    astar_cost_batch.append(astar_cost)


print("Testing...")
for i in tqdm.tqdm(range(0, batch_size)):
    board = bw.create_board(6, False)
    run_algos(board)

print("\n---------------Test Results---------------")
printResults("A* (Neural Network)", nn_astar_time_batch, nn_astar_heuristic_times_batch, nn_astar_cost_batch)
print("")
printResults("A* (Modified)", m_astar_time_batch, m_astar_heuristic_times_batch, m_astar_cost_batch)
print("")
printResults("A*", astar_time_batch, astar_heuristic_times_batch, astar_cost_batch)
print("")