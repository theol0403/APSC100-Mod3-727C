from keras.models import Sequential, Dense

model = Sequential()
model.add(Dense(16, input_dim=28 * 28, activation="relu"))
model.add(Dense(10, activation="relu"))
model.compile(optimizer="sgd", loss="mse", metrics=["accuracy"])

