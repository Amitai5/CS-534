from ModelGrapher import create_accuracy_graph
from NetworkTrainer import NetTrainer
from EMNIST_model import EMNIST_Net
from EMNIST_data import *
import torch
import os

EPOCHS = 25
BATCH_SIZE = 200
WEIGHT_DECAY = 1E-4
LEARNING_RATE = 5E-5

training_dataset, testing_dataset = load_dataset(BATCH_SIZE)
model = EMNIST_Net(1, 26)

print("\nNeural Network Structure: ")
print(model)
print("\n")

save_path = os.curdir + "\\results\\"
trainer = NetTrainer(model, save_path + "model.log", training_dataset, testing_dataset, LEARNING_RATE, WEIGHT_DECAY)
trainer.train(BATCH_SIZE, EPOCHS)

save_path = os.curdir + "\\results\\"
create_accuracy_graph(save_path + "graph.png")
torch.save(model.state_dict(), save_path + "model.pth")
