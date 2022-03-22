from NeuralNetwork import NetModel
import torch.nn.functional as F
import torch.optim as optim
import NetworkTrainer as nT
import SanitizeData as sd
import ModelGrapher
import numpy as np
import pickle
import torch
import tqdm
import os


EPOCHS = 10
BATCH_SIZE = 5
neural_network_directory = os.getcwd() + "\\models"

largest_file_number = 0
for name in os.listdir(neural_network_directory):
    file_num = int(name.replace("neural_network_", "").replace(".pkl", ""))
    if file_num > largest_file_number:
        largest_file_number = file_num
file_name = neural_network_directory + "\\neural_network_" + str(largest_file_number + 1) + ".pkl"

# Set the currentDevice to run the network on
if torch.cuda.is_available():
    currentDevice = torch.device("cuda:0")
    print("Running on GPU...\n")
else:
    currentDevice = torch.device("cpu")
    print("Running on CPU...\n")

# Get sanitized training data
print("Sanitizing Data...")
training_data = sd.sanitize_data()
print("Training Data Count: ", len(training_data))
print("Neural Network Input Count: ", len(training_data[0][0]))
print("")

# Create the neural network
model = NetModel().to(currentDevice)
print(f"{model}\n\n")

# Train the neural network
print("Training Network...")
model_trainer = nT.NetTrainer(model, currentDevice, training_data)
model_trainer.train(batch_size=BATCH_SIZE, epochs=EPOCHS)

# Graph the neural network training process
ModelGrapher.create_accuracy_graph()

# Save the neural network model
output = open(file_name, 'wb')
pickle.dump(model, output)