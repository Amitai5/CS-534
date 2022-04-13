from torch.utils.data import DataLoader, random_split
from torchvision.datasets import EMNIST
import torchvision.transforms as tt
import EMNIST_helpers as helper
import torch


BATCH_SIZE = 400
LEARNING_RATE = 0.01

dataset = EMNIST(root="data\\", split="byclass", download=True, train=True,
                 transform=tt.Compose([
                     lambda img: tt.functional.rotate(img, -90),
                     lambda img: tt.functional.hflip(img),
                     tt.ToTensor()
                 ]))

test_dataset = EMNIST(root="data\\", split="byclass", download=True, train=False,
                      transform=tt.Compose([
                          lambda img: tt.functional.rotate(img, -90),
                          lambda img: tt.functional.hflip(img),
                          tt.ToTensor()
                      ]))

print("EMNIST Dataset Count:", len(dataset) + len(test_dataset))
print("Training Dataset:    ", len(dataset))
print("Testing Dataset:     ", len(test_dataset))

# Set the random seed to get same random split
random_seed = 50
torch.manual_seed(random_seed)

val_size = 50000
train_size = len(dataset) - val_size

# Dividing the dataset into training dataset and validation dataset
train_ds, val_ds = random_split(dataset, [train_size, val_size])

train_dl = DataLoader(train_ds, BATCH_SIZE, shuffle=True, num_workers=4, pin_memory=True)
val_dl = DataLoader(val_ds, BATCH_SIZE*2, num_workers=4, pin_memory=True)