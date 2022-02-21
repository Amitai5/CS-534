import GeneticAlg
import csvwrite98
import numpy as np
import HillClimbing

batch_size = 3
board_size = 5
max_run_times = [0.1, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]


def printResults(name, board_counts, board_attacks, cost_results):
    board_attack_result = np.round(np.mean(board_attacks, axis=0), 3)
    cost_result = np.round(np.mean(cost_results, axis=0), 3)

    print("- " + name + " Board Attacks: " + str(board_attack_result))
    print("- " + name + " Cost: " + str(cost_result))


print("---------------Test Results---------------")
print("Batch Size: " + str(batch_size))
print("Board Size: " + str(board_size) + "\n")

for run_time in max_run_times:
    print("Run-Time: " + str(run_time) + " sec.")

    hillClimb_costs = []
    hillClimb_attacks = []
    hillClimb_board_counts = []

    genetics_costs = []
    genetics_fitnesses = []
    for j in range(0, batch_size):
        csvwrite98.create_board_csv(board_size, "board.txt", False)

        hillClimb_attack, hillClimb_cost = HillClimbing.findSolution(run_time, board_size, False)
        hillClimb_attacks.append(hillClimb_attack)
        hillClimb_costs.append(hillClimb_cost)

        genetics_fitness, genetics_cost = GeneticAlg.geneticAlg(run_time, board_size, False)
        genetics_fitnesses.append(genetics_fitness)
        genetics_costs.append(genetics_cost)

    printResults("Hill Climbing", hillClimb_board_counts, hillClimb_attacks, hillClimb_costs)

    genetics_fitness_result = np.round(np.mean(genetics_fitnesses, axis=0), 3)
    genetics_cost_result = np.round(np.mean(genetics_costs, axis=0), 3)
    print("- Genetics Fitness: " + str(genetics_fitness_result))
    print("- Genetics Cost: " + str(genetics_cost_result) + "\n")
