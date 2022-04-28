import matplotlib.pyplot as plt
import numpy as np
import torch


def show_example(img, label, predicted):
    img = img.to("cpu")
    label = np.asarray(label.to("cpu"))

    plt.title(f"Character: ({to_char(label)}), Predicted: ({to_char(predicted)})")
    plt.imshow(img.reshape(28, 28), cmap="gray")
    plt.show()


def get_default_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def to_char(num):
    return chr(num + 64)


def to_index(one_hot):
    idx = torch.argmax(one_hot, dim=0)
    idx = idx.to("cpu")
    return idx.detach().numpy()


def to_onehot(num):
    arr = np.zeros(27)
    arr[num] = 1
    return arr