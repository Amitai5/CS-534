from network_models.EMNIST_model import EMNIST_Net
from ModelGrapher import create_accuracy_graph
from EMNIST_data import load_dataset
from NetworkTrainer import NetTrainer
import EMNIST_helpers as helper
from PIL import Image
import numpy as np
import torch

EPOCHS = 8
BATCH_SIZE = 40
LEARNING_RATE = 0.05

training_dataset, testing_dataset = load_dataset(augment_data=True, force_reload=False)

model = EMNIST_Net()
trainer = NetTrainer(model, training_dataset, LEARNING_RATE)
trainer.train(BATCH_SIZE, EPOCHS)
create_accuracy_graph()

image_data = testing_dataset[10][0]
x = torch.Tensor(np.array(image_data))
result = model.forward(x).to("cpu")
result = result.detach().numpy()
letter = helper.to_char(max(np.where(result == max(result))[0]))
print(result)
print(letter)

img_data = np.reshape(image_data, (28, 28))
img = Image.fromarray(img_data, 'L')
img.show()