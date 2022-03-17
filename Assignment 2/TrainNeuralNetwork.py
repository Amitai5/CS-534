import numpy as np
import pandas
import tqdm
import os

training_data = []
training_data_directory = os.getcwd() + "\\trainingData"
for name in os.listdir(training_data_directory):
    partial_data = pandas.read_pickle(training_data_directory + "\\" + name)
    for data in partial_data:
        features = []
        board = data[0]
        astar_cost = data[1]

        # Will extract features here

        sanitized_data = [features, astar_cost]
        training_data.append(sanitized_data)


print("\nDataset Size: " + str(len(training_data)))
for data in training_data:
    print(data)