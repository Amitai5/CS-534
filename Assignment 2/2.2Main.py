import part2
import csvwrite
import numpy as np

time_batch = []
cost_batch = []
branching_batch = []


batch_size = 3
board_count = 12


def printResults(name, time_results, branching_results, cost_results):
    branching_result = np.round(np.mean(branching_results, axis=0), 3)
    time_result = np.round(np.mean(time_results, axis=0), 3)
    cost_result = np.round(np.mean(cost_results, axis=0), 3)

    print("- " + name + " Elapsed Time: " + str(time_result) + " sec.")
    print("- " + name + " Branching Factor: " + str(branching_result))
    print("- " + name + " Cost: " + str(cost_result))


def run():
    elapsed_time, cost, branching = part2.findSolution(True)
    branching_batch.append(branching)
    time_batch.append(elapsed_time)
    cost_batch.append(cost)



print("---------------Test Results---------------")
print("Batch Size: " + str(batch_size) + "\n")

for i in range(4, board_count + 1):
    print("Board Size: " + str(i))
    for j in range(0, batch_size):
        csvwrite.create_board_csv(i, "board.txt", False)
        run()

csvwrite.create_board_csv(15, "board.txt", False)
run()
printResults("Part2", time_batch, branching_batch, cost_batch)
print("")




