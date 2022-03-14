import csvwrite
import numpy as np
import SearchAlgorithms

astar_time_batch = []
astar_cost_batch = []
astar_branching_batch = []

greedy_time_batch = []
greedy_cost_batch = []
greedy_branching_batch = []

batch_size = 3
board_count = 12
SearchAlgorithms.use_modified_heuristic = True  # Use the better Heuristic for A*


def printResults(name, time_results, branching_results, cost_results):
    branching_result = np.round(np.mean(branching_results, axis=0), 3)
    time_result = np.round(np.mean(time_results, axis=0), 3)
    cost_result = np.round(np.mean(cost_results, axis=0), 3)

    print("- " + name + " Elapsed Time: " + str(time_result) + " sec.")
    print("- " + name + " Branching Factor: " + str(branching_result))
    print("- " + name + " Cost: " + str(cost_result))


def run_both_algos():
    astar_elapsed_time, astar_cost, astar_branching = SearchAlgorithms.findSolution(0, False)  # Astar
    astar_branching_batch.append(astar_branching)
    astar_time_batch.append(astar_elapsed_time)
    astar_cost_batch.append(astar_cost)

    greedy_elapsed_time, greedy_cost, greedy_branching = SearchAlgorithms.findSolution(1, False)  # Greedy
    greedy_branching_batch.append(greedy_branching)
    greedy_time_batch.append(greedy_elapsed_time)
    greedy_cost_batch.append(greedy_cost)


print("---------------Test Results---------------")
print("Batch Size: " + str(batch_size) + "\n")

# for i in range(4, board_count + 1):
#     print("Board Size: " + str(i))
#     for j in range(0, batch_size):
#         csvwrite.create_board_csv(i, "board.txt", False)
#         run_both_algos()

run_both_algos()
printResults("Greedy", greedy_time_batch, greedy_branching_batch, greedy_cost_batch)
printResults("A*", astar_time_batch, astar_branching_batch, astar_cost_batch)
print("")
