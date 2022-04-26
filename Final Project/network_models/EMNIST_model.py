import torch.nn.functional as F
import torch.nn as nn
import torch


class EMNIST_Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.device = torch.device("cpu")
        self.layer1 = nn.Linear(28*28, 28*28)
        self.layer2 = nn.Linear(28*28, 100)
        self.layer3 = nn.Linear(100, 26)

        self.activ1 = nn.Sigmoid()
        self.activ2 = nn.Sigmoid()
        self.activ3 = nn.Sigmoid()

    def forward(self, inputs):
        inputs = inputs.to(self.device)
        inputs = self.layer1(inputs)
        inputs = self.activ1(inputs)
        inputs = self.layer2(inputs)
        inputs = self.activ2(inputs)
        inputs = self.layer3(inputs)
        inputs = self.activ3(inputs)
        return inputs

    def set_device(self, device):
        self.device = device
        self.to(device)
