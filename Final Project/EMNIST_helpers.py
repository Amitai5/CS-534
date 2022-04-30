import matplotlib.pyplot as plt
import numpy as np
import torch


def show_example(img, label, predicted):
    img = img.to("cpu")
    label = np.asarray(label.to("cpu"))

    plt.title(f"Character: ({to_char(label)}), Predicted: ({to_char(predicted)})")
    plt.imshow(img.reshape(28, 28), cmap="gray")
    plt.show()


def clean_results(results):
    letter_results = []
    results = results.to("cpu").detach().numpy()
    sorted_results = sorted(range(len(results)), key=lambda i: results[i], reverse=True)

    max_value = results[sorted_results[0]]
    for idx in sorted_results:
        normalized_value = results[idx] / max_value
        if normalized_value > 0.1:
            letter_results.append((normalized_value, to_char(idx)))
    return letter_results


def is_image_empty(img):
    for row in img:
        for pixel in row:
            if pixel != 0:
                return False
    return True


def get_default_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def to_index(one_hot):
    idx = torch.argmax(one_hot, dim=0)
    idx = idx.to("cpu")
    return idx.detach().numpy()


def to_onehot(num):
    arr = np.zeros(27)
    arr[num] = 1
    return arr


def to_char(num):
    return chr(num + 64)