import GeneticAlg
import csvwrite98
import numpy as np
import HillClimbing
from tqdm import tqdm
from matplotlib import pyplot as plt

max_run_times = [0.1, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]


def create_graph(x_axis, x_label, genetics_costs, hillClimb_costs):
    print("Finished!")
    plt.plot(x_axis, genetics_costs, label="Genetics Algorithm")
    plt.plot(x_axis, hillClimb_costs, label="Hill Climbing")
    plt.xlabel(x_label)
    plt.ylabel('Algorithm Cost')
    plt.title('Performance vs Run Time')
    plt.legend()
    plt.show()


print("---------------Test Results---------------\n")
# csvwrite98.create_board_csv(8, "board.txt", False)  # Create board when not given one...

print("Testing HillClimber and Genetics for 2 minutes...")
HillClimbing.findSolution(120, False)
GeneticAlg.geneticAlg(120, False)
create_graph(range(1, 13), "Run Time (10 second intervals)", GeneticAlg.interval_cost_updates, HillClimbing.interval_cost_updates)


print("\nTesting Hill Climbing and Genetics for [0.1, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20] second intervals...")
genetics_costs = []
hillClimb_costs = []
for run_time in tqdm(max_run_times):
    hillClimb_attack, hillClimb_cost = HillClimbing.findSolution(run_time, False)
    hillClimb_costs.append(hillClimb_cost)

    genetics_fitness, genetics_cost = GeneticAlg.geneticAlg(run_time, False)
    genetics_costs.append(genetics_cost)

create_graph(max_run_times, "Run Time (seconds)", genetics_costs, hillClimb_costs)


print("\nTesting largest board given 20 second Time Limit...")
hillClimb_board_size = 10
# csvwrite98.create_board_csv(hillClimb_board_size, "board.txt", False)
_, hillClimb_cost = HillClimbing.findSolution(20, False)
print("Hill Climbing")
print("- Board Size: " + str(hillClimb_board_size))
print("- Cost: " + str(hillClimb_cost))

genetics_board_size = 14
# csvwrite98.create_board_csv(genetics_board_size, "board.txt", False)
_, genetics_cost = GeneticAlg.geneticAlg(20, False)
print("Genetics Algorithm")
print("- Board Size: " + str(genetics_board_size))
print("- Cost: " + str(genetics_cost))
