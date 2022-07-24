import os

from DeviceDataLoader import DeviceDataLoader
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import EMNIST
import EMNIST_helpers as helper


def load_dataset(batch_size):
    print("\nLoading Datasets...")
    save_location = os.curdir + "\\data\\"
    training_dataset = EMNIST(root=save_location, split="letters", download=True, train=True,
                              transform=transforms.Compose([
                                  lambda img: transforms.functional.rotate(img, -90),
                                  lambda img: transforms.functional.hflip(img),
                                  transforms.ToTensor()
                              ]))

    testing_dataset = EMNIST(root=save_location, split="letters", download=True, train=False,
                             transform=transforms.Compose([
                                 lambda img: transforms.functional.rotate(img, -90),
                                 lambda img: transforms.functional.hflip(img),
                                 transforms.ToTensor()
                             ]))

    print("Total No of Images in EMNIST-Letters dataset:", len(training_dataset) + len(testing_dataset))
    print("No of images in Training dataset:    ", len(training_dataset))
    print("No of images in Testing dataset:     ", len(testing_dataset))
    print("")

    training_dataset = DataLoader(training_dataset, batch_size, shuffle=True)
    testing_dataset = DataLoader(testing_dataset, batch_size, shuffle=True)

    device = helper.get_default_device()
    test_dataloader = DeviceDataLoader(testing_dataset, device)
    training_dataloader = DeviceDataLoader(training_dataset, device)
    return training_dataloader, test_dataloader


def img2tensor(image):
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    return transform(image).reshape(1, 1, 28, 28)
