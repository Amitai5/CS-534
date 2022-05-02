import torch.nn as nn


def conv_block(in_channels, out_channels):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
              nn.BatchNorm2d(out_channels),
              nn.ReLU(inplace=True)]
    return nn.Sequential(*layers)


class EMNIST_Net(nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.conv1 = conv_block(in_channels, 64)
        self.conv2 = conv_block(64, 128)
        self.conv3 = conv_block(128, 256)

        self.pool_layer = nn.MaxPool2d(2)
        self.classifier = nn.Sequential(nn.MaxPool2d(7),
                                        nn.Flatten(),
                                        nn.Dropout(0.5),
                                        nn.Linear(1024, num_classes))

    def forward(self, inputs):
        inputs = self.conv1(inputs)
        inputs = self.conv2(inputs)
        inputs = self.conv3(inputs)
        inputs = self.pool_layer(inputs)
        inputs = self.classifier(inputs)
        return inputs
