from tensorflow import keras
from keras.models import load_model
model = load_model('cnn.h5')

# The following should work but gives an error on my laptop
# model = keras.models.load_model('C:\Users\saadr\Downloads\cnn.h5')