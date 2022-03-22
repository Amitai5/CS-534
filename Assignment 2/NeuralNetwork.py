import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
import torch


# Create a neural network model
class NetModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(17, 4)
        self.fc2 = nn.Linear(4, 1)

    def forward(self, inputs):
        inputs = F.relu(self.fc1(inputs))
        inputs = self.fc2(inputs)
        return F.relu(inputs)
