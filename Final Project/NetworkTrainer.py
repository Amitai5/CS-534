import EMNIST_helpers as helper
import torch.optim as optim
import torch.nn as nn
from tqdm import tqdm
import numpy as np
import torch
import time


class NetTrainer:
    def __init__(self, model, log_file, train_dataloader, test_dataloader, lr, weight_decay):
        self.optimizer = optim.Adam(model.parameters(), lr, weight_decay=weight_decay)
        self.loss_function = nn.CrossEntropyLoss()
        self.device = helper.get_default_device()
        self.training_data = train_dataloader
        self.testing_data = test_dataloader
        self.model = model.to(self.device)
        self.weight_decay = weight_decay
        self.log_file = log_file
        self.learning_rate = lr

    def fwd_pass(self, x, y, train=False):
        if train:
            self.model.zero_grad()
        outputs = self.model(x)

        matches = []
        for i in range(len(outputs)):
            actual_idx = np.asarray(y[i].to("cpu"))
            predicted_idx = helper.to_index(outputs[i])
            matches.append(bool(predicted_idx == actual_idx))

        acc = matches.count(True) / len(matches)
        loss = self.loss_function(outputs, y)

        if train:
            loss.backward()
            self.optimizer.step()
        return acc, loss

    @torch.no_grad()
    def testModel(self):
        batch_acc = []
        batch_loss = []

        print("\nTesting Model...")
        time.sleep(0.1)  # Solves PyCharm console printing bug

        for data in tqdm(self.testing_data):
            x, y = data
            acc, loss = self.fwd_pass(x, y)
            batch_loss.append(loss)
            batch_acc.append(acc)

        return np.average(batch_acc), np.average(np.array(batch_loss, dtype=float))

    def train(self, batch_size=100, epochs=4):
        print("Training Parameters: ")
        print(f"Epoch Count: {epochs},\tBatch Size: {batch_size}")
        print(f"Learning Rate: {self.learning_rate}, \tWeight Decay: {self.weight_decay}\n")
        torch.cuda.empty_cache()

        with open(self.log_file, "r+") as log_file:
            log_file.truncate(0)

            for epoch in range(epochs):
                print("Training Epoch...")
                time.sleep(0.1)  # Solves PyCharm console printing bug

                for data in tqdm(self.training_data):
                    x, y = data
                    acc, loss = self.fwd_pass(x, y, train=True)

                # Logging the test data
                val_acc, val_loss = self.testModel()
                log_file.write(f"{epoch + 1},{round(float(acc), 3)},"
                               f"{round(float(loss), 4)},{round(float(val_acc), 3)},{round(float(val_loss), 4)}\n")

                print(f"Epoch: {epoch + 1}, \tVal-Loss: {round(val_loss, 4)},\tVal-Accuracy: {round(val_acc, 3) * 100}%,\tTrain-Accuracy: {round(acc, 3) * 100}%\n")
                time.sleep(0.1)  # Solves PyCharm console printing bug
