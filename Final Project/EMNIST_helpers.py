from torchvision.utils import make_grid
import matplotlib.pyplot as plt


def to_char(num):
    if num < 10:
        return str(num)
    elif num < 36:
        return chr(num+55)
    else:
        return chr(num+61)


def to_index(char):
    if ord(char) < 59:
        return ord(char)-48
    elif ord(char) < 95:
        return ord(char)-55
    else:
        return ord(char)-61


def show_example(data):
    img, label = data
    plt.title("Character: ("+to_char(label)+")")
    plt.imshow(img[0], cmap="gray")
    plt.show()


def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(make_grid(images, nrow=20).permute(1, 2, 0))
        break
