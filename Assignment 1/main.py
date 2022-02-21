import csvwrite
import numpy as np
import NQueenSolutionPart1

batch_size = 3
board_count = 13


def printResults(name, time_results, branching_results, cost_results):
    branching_result = np.round(np.mean(branching_results, axis=0), 2)
    time_result = np.round(np.mean(time_results, axis=0), 6)
    cost_result = np.round(np.mean(cost_results, axis=0), 6)

    print("- " + name + " Elapsed Time: " + str(time_result) + " sec.")
    print("- " + name + " Branching Factor: " + str(branching_result))
    print("- " + name + " Cost: " + str(cost_result))


print("---------------Test Results---------------")
for i in range(4, board_count + 1):
    print("Board Size: " + str(i))

    astar_time_batch = []
    astar_cost_batch = []
    astar_branching_batch = []

    greedy_time_batch = []
    greedy_cost_batch = []
    greedy_branching_batch = []
    for j in range(0, batch_size):
        csvwrite.create_board_csv(i, "test", False)
        astar_elapsed_time, astar_cost, astar_branching = NQueenSolutionPart1.findSolution(0, False)  # Astar
        astar_branching_batch.append(astar_branching)
        astar_time_batch.append(astar_elapsed_time)
        astar_cost_batch.append(astar_cost)

        greedy_elapsed_time, greedy_cost, greedy_branching = NQueenSolutionPart1.findSolution(1, False)  # Greedy
        greedy_branching_batch.append(greedy_branching)
        greedy_time_batch.append(greedy_elapsed_time)
        greedy_cost_batch.append(greedy_cost)

    printResults("Greedy", greedy_time_batch, greedy_branching_batch, greedy_cost_batch)
    printResults("A*", astar_time_batch, astar_branching_batch, astar_cost_batch)
    print("\n")
