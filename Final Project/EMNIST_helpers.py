from torchvision.utils import make_grid
import matplotlib.pyplot as plt
import numpy as np


def to_char(num):
    return chr(num + 65)


def to_index(char):
    if 65 <= ord(char) <= 90:
        return ord(char) - 65
    elif 97 <= ord(char) <= 122:
        return ord(char) - 97


def to_onehot(char):
    idx = to_index(char)
    arr = np.zeros(26)
    arr[idx] = 1
    return arr


def show_example(data):
    img, label = data
    plt.title("Character: (" + to_char(label) + ")")
    plt.imshow(img, cmap="gray")
    plt.show()


def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(make_grid(images, nrow=20).permute(1, 2, 0))
        break
