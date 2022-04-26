import torch.optim as optim
import torch.nn as nn
from tqdm import tqdm
import numpy as np
import torch
import time
import sys


class NetTrainer:
    def __init__(self, model, training_data, lr):
        self.model = model
        self.loss_function = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr, weight_decay=1e-4)

        x = []
        y = []
        for data in training_data:
            x.append(data[0])
            y.append(data[1])

        x = torch.Tensor(np.array(x))
        y = torch.Tensor(np.array(y))

        # Reserve 10% of our data for validation
        testing_percent = 0.1
        training_size = int(len(x) * testing_percent)
        self.testSize = int((len(x) - training_size) / 10)

        self.train_x = x[:-training_size]
        self.train_y = y[:-training_size]

        self.test_x = x[-training_size:]
        self.test_y = y[-training_size:]

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.model.set_device(self.device)

    def fwd_pass(self, x, y, train=False):
        if train:
            self.model.zero_grad()
        outputs = self.model(x)

        matches = []
        for i in range(len(outputs)):
            calculated_onehot = outputs[i].to("cpu")
            calculated_onehot = calculated_onehot.detach().numpy()

            actual_onehot = y[i].to("cpu")
            actual_onehot = actual_onehot.detach().numpy()

            calculated_idx = max(np.where(calculated_onehot == max(calculated_onehot))[0])
            actual_idx = np.where(actual_onehot == max(actual_onehot))[0]
            matches.append(bool(calculated_idx == actual_idx))

        acc = matches.count(True) / len(matches)
        loss = self.loss_function(outputs, y)

        if train:
            loss.backward()
            self.optimizer.step()
        return acc, loss

    def testModel(self):
        random_start = np.random.randint(len(self.test_x) - self.testSize)
        x, y = self.test_x[random_start:random_start + self.testSize], self.test_y[random_start:random_start + self.testSize]
        x, y = x.to(self.device), y.to(self.device)
        with torch.no_grad():
            acc, loss = self.fwd_pass(x, y)
        return acc, loss

    def train(self, batch_size=100, epochs=4):
        print("Training Parameters: ")
        print(f"Epoch Count: {epochs},\tBatch Size: {batch_size}\n")

        with open("model.log", "r+") as log_file:
            log_file.truncate(0)

            for epoch in range(epochs):
                for i in tqdm(range(0, len(self.train_x), batch_size), file=sys.stdout):
                    batch_x = self.train_x[i:i + batch_size].to(self.device)
                    batch_y = self.train_y[i:i + batch_size].to(self.device)

                    acc, loss = self.fwd_pass(batch_x, batch_y, train=True)

                # Logging the test data
                val_acc, val_loss = self.testModel()
                log_file.write(f"{round(time.time(), 3)},{round(float(acc), 2)},"
                               f"{round(float(loss), 4)},{round(float(val_acc), 2)},{round(float(val_loss), 4)}\n")

                print(f"Epoch: {epoch + 1}, \tVal-Loss: {val_loss},\tVal-Accuracy: {val_acc},\tTrain-Accuracy: {acc}\n")
