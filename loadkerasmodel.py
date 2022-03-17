from tensorflow import keras
from tensorflow.keras.datasets import mnist
from keras.models import load_model
import numpy as np

(train_x, train_y), (test_x, test_y) = mnist.load_data()

model = load_model("cnn.h5")

grid = np.zeros((28, 28))

print(grid.shape)
print(test_x.shape)

print(model.predict(grid.reshape(1, 28, 28)))
