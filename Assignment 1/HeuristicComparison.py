import csvwrite
import numpy as np
import SearchAlgorithms

batch_size = 5
board_count = 9


def printResults(name, time_results, branching_results, cost_results):
    branching_result = np.round(np.mean(branching_results, axis=0), 3)
    time_result = np.round(np.mean(time_results, axis=0), 3)
    cost_result = np.round(np.mean(cost_results, axis=0), 3)

    print("- " + name + " Elapsed Time: " + str(time_result) + " sec.")
    print("- " + name + " Branching Factor: " + str(branching_result))
    print("- " + name + " Cost: " + str(cost_result))


print("---------------Test Results---------------")
print("Batch Size: " + str(batch_size) + "\n")

for i in range(4, board_count + 1):
    print("Board Size: " + str(i))

    astar_time_batch = []
    astar_cost_batch = []
    astar_branching_batch = []

    modified_astar_time_batch = []
    modified_astar_cost_batch = []
    modified_astar_branching_batch = []
    for j in range(0, batch_size):
        csvwrite.create_board_csv(i, "board.txt", False)

        SearchAlgorithms.use_modified_heuristic = False
        astar_elapsed_time, astar_cost, astar_branching = SearchAlgorithms.findSolution(0, False)  # Astar
        astar_branching_batch.append(astar_branching)
        astar_time_batch.append(astar_elapsed_time)
        astar_cost_batch.append(astar_cost)

        SearchAlgorithms.use_modified_heuristic = True
        modified_astar_elapsed_time, modified_astar_cost, modified_astar_branching = SearchAlgorithms.findSolution(0, False)  # Astar
        modified_astar_branching_batch.append(modified_astar_branching)
        modified_astar_time_batch.append(modified_astar_elapsed_time)
        modified_astar_cost_batch.append(modified_astar_cost)

    printResults("A*", astar_time_batch, astar_branching_batch, astar_cost_batch)
    printResults("Modified A*", modified_astar_time_batch, modified_astar_branching_batch, modified_astar_cost_batch)
    print("")