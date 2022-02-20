import csvwrite
import numpy as np
import NQueenSolutionPart1

batch_size = 3
max_board_size = 9

print("---------------Test Results---------------")

for i in range(7, max_board_size + 1):
    csvwrite.create_board_csv(i, "test", False)
    print("Board Size: " + str(i))

    astar_batch = []
    greedy_batch = []
    for j in range(0, batch_size):
        astar_elapsed_time = NQueenSolutionPart1.findSolution(0, False)  # Astar
        if type(astar_elapsed_time) != float:
            astar_elapsed_time = 0
        astar_batch.append(astar_elapsed_time)

        greedy_elapsed_time = NQueenSolutionPart1.findSolution(1, False)  # Greedy
        if type(greedy_elapsed_time) != float:
            greedy_elapsed_time = 0

        greedy_batch.append(greedy_elapsed_time)

    greedy_result = np.round(np.mean(greedy_batch, axis=0), 6)
    print("Greedy Elapsed Time: " + str(greedy_result) + " sec.")
    astar_result = np.round(np.mean(astar_batch, axis=0), 6)
    print("A* Elapsed Time: " + str(astar_result) + " sec. \n")
