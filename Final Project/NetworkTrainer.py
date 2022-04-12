import torch.optim as optim
import torch.nn as nn
from tqdm import tqdm
import numpy as np
import torch
import time
import sys


class NetTrainer:
    def __init__(self, model, device, train_data, test_data, lr=0.001):
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.loss_function = nn.L1Loss()

        train_x = torch.Tensor([i[0] for i in train_data])
        train_y = torch.Tensor([i[1] for i in train_data])
        test_x = torch.Tensor([i[0] for i in test_data])
        test_y = torch.Tensor([i[1] for i in test_data])

        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y

        self.device = device
        self.model = model

    def fwd_pass(self, x, y, train=False):
        if train:
            self.model.zero_grad()

        x, y = x.to(self.device), y.to(self.device)
        outputs = self.model(x)

        matches = [torch.argmax(i) == torch.argmax(j) for i, j in zip(outputs, y)]
        acc = matches.count(True) / len(matches)
        loss = self.loss_function(outputs, y)

        if train:
            loss.backward()
            self.optimizer.step()
        return acc, loss

    def testModel(self):
        random_start = np.random.randint(len(self.test_x) - self.testSize)
        x, y = self.test_x[random_start:random_start + self.testSize], self.test_y[random_start:random_start + self.testSize]
        with torch.no_grad():
            acc, loss = self.fwd_pass(x.view(-1, 5), y.view(-1, 1))
        return acc, loss

    def train(self, batch_size=100, epochs=4):
        print("Training Parameters: ")
        print(f"Epoch Count: {epochs},\tBatch Size: {batch_size}\n")

        with open("model.log", "r+") as log_file:
            log_file.truncate(0)

            for epoch in range(epochs):
                for i in tqdm(range(0, len(self.train_x), batch_size), file=sys.stdout):
                    batch_x = self.train_x[i:i + batch_size].view(-1, 5).to(self.device)
                    batch_y = self.train_y[i:i + batch_size].view(-1, 1).to(self.device)

                    acc, loss = self.fwd_pass(batch_x, batch_y, train=True)

                # Logging the test data
                val_acc, val_loss = self.testModel()
                log_file.write(f"{round(time.time(), 3)},{round(float(acc), 2)},"
                               f"{round(float(loss), 4)},{round(float(val_acc), 2)},{round(float(val_loss), 4)}\n")

                print(f"Epoch: {epoch + 1}, \tLoss: {loss},\tVal-Accuracy: {val_acc}\n")
                print(f"Epoch: {epoch + 1}, \tLoss: {loss},\tVal-Accuracy: {val_acc}\n")
