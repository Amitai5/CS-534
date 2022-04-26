from EMNIST_helpers import to_onehot
from numpy import asarray
from PIL import Image
import numpy as np
import pickle
import tqdm
import os

pickle_filename2 = os.getcwd() + "\\data\\EMNIST\\training_dataset.pkl"
pickle_filename = os.getcwd() + "\\data\\EMNIST\\test_dataset.pkl"
train_directory = os.getcwd() + "\\data\\EMNIST\\train_data"
test_directory = os.getcwd() + "\\data\\EMNIST\\test_data"


def load_dataset(augment_data=True, force_reload=False):
    print("\nLoading Datasets...")
    if force_reload or not os.path.exists(pickle_filename2):
        compile_dataset(test_directory, pickle_filename2, augment_data=False)
    if force_reload or not os.path.exists(pickle_filename):
        compile_dataset(train_directory, pickle_filename, augment_data)

    training_data_file = open(pickle_filename, 'rb')
    testing_data_file = open(pickle_filename2, 'rb')
    training_dataset, testing_dataset = pickle.load(training_data_file), pickle.load(testing_data_file)

    print("EMNIST Dataset Training Count: ", len(training_dataset))
    print("EMNIST Dataset Testing Count: ", len(testing_dataset))
    print("\n")
    return training_dataset, testing_dataset


def compile_dataset(directory, filename, augment_data):
    dataset = []
    for image_label in tqdm.tqdm(os.listdir(directory)):
        current_directory = train_directory + "\\" + image_label
        for image_filename in os.listdir(current_directory):
            original_image = Image.open(current_directory + "\\" + image_filename).convert('L')

            images = [original_image]
            if augment_data:
                images.extend(augment_image(original_image))

            for img in images:
                flattened_img = asarray(img, dtype=float).flatten()
                dataset.append([flattened_img, to_onehot(image_label)])

    np.random.shuffle(dataset)
    dataset = dataset[:100000]
    filehandler = open(filename, "wb")
    pickle.dump(np.array(dataset, dtype=object), filehandler)


def augment_image(image):
    images = []
    for rotation in [90, 180, 270]:
        new_img = image.rotate(rotation)
        images.append(new_img)
    return images
