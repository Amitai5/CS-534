from torchvision.utils import make_grid
import matplotlib.pyplot as plt
import numpy as np
import torch


def show_example(img, label, predicted):
    img = img.to("cpu")
    label = np.asarray(label.to("cpu"))

    plt.title(f"Character: ({to_char(label)}), Predicted: ({to_char(predicted)})")
    plt.imshow(img.reshape(28, 28), cmap="gray")
    plt.show()


def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(make_grid(images, nrow=20).permute(1, 2, 0))
        break


def get_default_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def to_char(num):
    if num < 10:
        return str(num)
    elif num < 36:
        return chr(num+55)
    else:
        return chr(num+61)


def to_index(one_hot):
    idx = torch.argmax(one_hot, dim=0)
    idx = idx.to("cpu")
    return idx.detach().numpy()


def to_onehot(num):
    arr = np.zeros(62)
    arr[num] = 1
    return arr