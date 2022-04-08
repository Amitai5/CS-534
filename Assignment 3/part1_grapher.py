import matplotlib.pyplot as plt
from part1_function import rl
import numpy as np
import tqdm
import os

max_time = 1
time_interval = 0.01
default_alpha = 0.67
default_epsilon = 0.20
epsilon_range = [0.01, 0.10, 0.30, 0.60, 0.90]
alpha_range = [0.01, 0.25, 0.50, 0.75, 0.90, 1.00]

for alpha in tqdm.tqdm(alpha_range):
    graph_points_x = np.zeros(round(max_time / time_interval))
    graph_points_y = np.zeros(round(max_time / time_interval))
    scatter_points_x = []
    scatter_points_y = []

    for i in range(1, 5):
        filename = os.getcwd() + "\\testBoards\\grid" + str(i) + ".txt"
        time, rew = rl(filename, time_interval, max_time, alpha, default_epsilon)
        graph_points_x = [x + y for x, y in zip(graph_points_x, time)]
        graph_points_y = [x + y for x, y in zip(graph_points_y, rew)]
        scatter_points_x.extend(time)
        scatter_points_y.extend(rew)

    graph_points_y = [x / 4 for x in graph_points_y]
    graph_points_x = [x / 4 for x in graph_points_x]
    plt.plot(graph_points_x, graph_points_y, label="Ɛ = " + str(alpha))
    plt.scatter(scatter_points_x, scatter_points_y, s=12, alpha=0.15)

plt.title("Comparing Alpha Values")
plt.xlabel("Time (sec)")
plt.ylabel("Reward")
plt.legend()
plt.show()