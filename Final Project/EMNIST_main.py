import torch

from ModelGrapher import create_accuracy_graph
from NetworkTrainer import NetTrainer
from EMNIST_model import EMNIST_Net
import EMNIST_helpers as helper
import EMNIST_data

EPOCHS = 8
BATCH_SIZE = 100
LEARNING_RATE = 1E-3

training_dataset, testing_dataset = EMNIST_data.load_dataset(BATCH_SIZE)
model = EMNIST_Net(1, 27)

trainer = NetTrainer(model, training_dataset, testing_dataset, LEARNING_RATE)
trainer.train(BATCH_SIZE, EPOCHS)

create_accuracy_graph()

for data in testing_dataset:
    img, label = data
    predicted_idx = helper.to_index(model(img)[0])
    helper.show_example(img[0], label[0], predicted_idx)
