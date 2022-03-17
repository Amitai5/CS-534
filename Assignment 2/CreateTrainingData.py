import SearchAlgorithms as sa
import BoardWrite as bw
import numpy as np
import pickle
import tqdm
import os

board_size = 6
gen_data_count = 5
training_data_directory = os.getcwd() + "\\trainingData"

largest_file_number = 0
for name in os.listdir(training_data_directory):
    file_num = int(name.replace("training_data_", "").replace(".pkl", ""))
    if file_num > largest_file_number:
        largest_file_number = file_num
file_name = training_data_directory + "\\training_data_" + str(largest_file_number + 1) + ".pkl"

print("\nBoard Size: " + str(board_size))
print("File Name: " + file_name)
print("\nGenerating " + str(gen_data_count) + " Boards...")

training_data = []
for i in tqdm.tqdm(range(gen_data_count)):
    new_data = []
    new_board = bw.create_board(board_size, False)
    board_solution_cost, _, _ = sa.findSolution(new_board, 0, False)

    new_data.append(new_board)
    new_data.append(board_solution_cost)
    training_data.append(new_data)

output = open(file_name, 'wb')
pickle.dump(training_data, output)