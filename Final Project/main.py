from EMNIST_model import EMNIST_Net
from SSAlg import sSpellAlg
from EMNIST_data import *
import torch
import sys
import cv2
import os

# Read in the image the user inputted
test_image_path = sys.argv[1]
if not os.path.isfile(test_image_path):
    print("Image file not found...")
    exit(128)

# Validate that the file is an image file
_, file_extension = os.path.splitext(test_image_path)
if file_extension != ".png" and file_extension != ".jpg" and file_extension != ".jpeg":
    print("File was not a supported image file. Supported file types: .jpg .jpeg .png (with no alpha)")
    exit(128)

# Convert the image to black and white
img = cv2.imread(test_image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load in the neural network model
model = EMNIST_Net(1, 26)
model.load_state_dict(torch.load(os.curdir + "\\results\\model.pth"))
model.eval()

results = []
print("\nNetwork Result: ")
letter_count = round(len(img[1]) / 28)

for i in range(0, letter_count):
    x_index = i * 29
    cropped_img = img[0:28, x_index:x_index+28]

    if not helper.is_image_empty(cropped_img):
        cropped_img = img2tensor(cropped_img)
        result = model(cropped_img)[0]
        result = helper.clean_results(result)
        print(f"- Letter #{i + 1}: {result}")
        results.append(result)


word, probability = sSpellAlg(results)

print("\nAlgorithm Result: ")
print(f"- Probability: {probability}")
print(f"- Word: \"{word}\"")