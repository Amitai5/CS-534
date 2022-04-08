import matplotlib.pyplot as plt
from part1_function import rl
from time import sleep
import numpy as np
import tqdm
import os

max_time = 1
time_interval = 0.01
default_alpha = 0.67
default_gamma = 0.67
default_epsilon = 0.20
epsilon_range = [0.01, 0.10, 0.30, 0.60, 0.90]
gamma_range = [0.01, 0.25, 0.50, 0.75, 0.90, 1.00]
alpha_range = [0.01, 0.25, 0.50, 0.75, 0.90, 1.00]


def test_param_values(use_sarsa, test_range, param_name, param_symbol):
    print("\nTesting " + param_name + " Values...")
    param_type = param_name.lower()[0]
    sleep(0.5)

    for test_point in tqdm.tqdm(test_range):
        graph_points_x = np.zeros(round(max_time / time_interval))
        graph_points_y = np.zeros(round(max_time / time_interval))
        scatter_points_x = []
        scatter_points_y = []

        for i in range(1, 5):
            filename = os.getcwd() + "\\testBoards\\grid" + str(i) + ".txt"

            alpha = test_point if param_type == "a" else default_alpha
            gamma = test_point if param_type == "g" else default_gamma
            epsilon = test_point if param_type == "e" else default_epsilon
            time, rew = rl(filename, time_interval, max_time, use_sarsa, alpha, epsilon, gamma)

            graph_points_x = [x + y for x, y in zip(graph_points_x, time)]
            graph_points_y = [x + y for x, y in zip(graph_points_y, rew)]
            scatter_points_x.extend(time)
            scatter_points_y.extend(rew)

        graph_points_x = [x / 4 for x in graph_points_x]
        graph_points_y = [x / 4 for x in graph_points_y]
        label_string = param_symbol + " = " + str(test_point)

        plt.plot(graph_points_x, graph_points_y, label=label_string)
        plt.scatter(scatter_points_x, scatter_points_y, s=12, alpha=0.15)

    plt.title("Comparing " + param_name + " Values (" + ("SARSA)" if use_sarsa else "QLearning)"))
    plt.xlabel("Time (sec)")
    plt.ylabel("Reward")
    plt.legend()
    plt.show()


max_time = 0.25
for algo_type in [False, True]:
    test_param_values(algo_type, alpha_range, "Alpha", "α")
    test_param_values(algo_type, gamma_range, "Gamma", "γ")
    test_param_values(algo_type, epsilon_range, "Epsilon", "ε")

max_time = 20
for algo_type in [False, True]:
    test_param_values(algo_type, alpha_range, "Alpha", "α")
    test_param_values(algo_type, gamma_range, "Gamma", "γ")
    test_param_values(algo_type, epsilon_range, "Epsilon", "ε")