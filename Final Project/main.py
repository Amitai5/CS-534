from EMNIST_model import EMNIST_Net
from EMNIST_data import *
import torch

model = EMNIST_Net(1, 27)
model.load_state_dict(torch.load(os.curdir + "\\results\\emnist\\model.pth"))
model.eval()

img = cv2.imread(os.curdir + "\\test_images\\test.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

results = []
for i in range(0, 8):
    x_index = i * 29
    cropped_img = img[0:28, x_index:x_index+28]

    if not helper.is_image_empty(cropped_img):
        cropped_img = img2tensor(cropped_img)
        result = model(cropped_img)[0]
        result = helper.clean_results(result)
        results.append(result)

