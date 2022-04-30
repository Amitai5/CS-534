from ModelGrapher import create_accuracy_graph
from NetworkTrainer import NetTrainer
from EMNIST_model import EMNIST_Net
from EMNIST_data import *
import torch
import os

EPOCHS = 16
BATCH_SIZE = 100
LEARNING_RATE = 1E-3

training_dataset, testing_dataset = load_dataset(BATCH_SIZE)
model = EMNIST_Net(1, 27)

trainer = NetTrainer(model, training_dataset, testing_dataset, LEARNING_RATE)
trainer.train(BATCH_SIZE, EPOCHS)

save_path = os.curdir + "\\results\\emnist\\"
create_accuracy_graph(save_path + "graph.png")
torch.save(model.state_dict(), save_path + "model.pth")
