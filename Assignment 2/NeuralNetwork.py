import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
import torch


# Create a neural network model
class NetModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(5, 1)
        # self.layer2 = nn.Linear(20, 1)
        # self.layer3 = nn.Linear(8, 1)

        self.activ1 = nn.Sigmoid()
        # self.activ2 = nn.Sigmoid()
        # self.activ3 = nn.ReLU()

    def forward(self, inputs):
        inputs = self.layer1(inputs)
        inputs = self.activ1(inputs)
        # inputs = self.layer2(inputs)
        # inputs = self.activ2(inputs)
        # inputs = self.layer3(inputs)
        # inputs = self.activ3(inputs)
        return inputs
