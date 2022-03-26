import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from time import perf_counter


class PredictThread(QThread):
    predict_signal = pyqtSignal(np.ndarray, float)

    def __init__(self, model):
        super().__init__()
        self.run = True
        self.model = model
        self.grid = np.zeros((28, 28))
        self.gridUpdated = True

    def run(self):
        while self.run:
            if self.gridUpdated:
                self.gridUpdated = False
                start_wall = perf_counter()
                confidence = self.model.predict(self.grid)
                end_wall = perf_counter()
                self.predict_signal.emit(confidence, end_wall - start_wall)
            self.usleep(20000)

    def stop(self):
        self.run = False
        self.wait()


class Model:
    """This class contains and runs the ML models"""

    def __init__(self):

        self.thread = PredictThread(self)
        self.thread.start()

        self.kerasModels = ["CNN", "CNN_Augmented", "MLP_Dropout"]
        self.modelList = self.kerasModels + ["SVM", "KNN"]
        self.model = self.modelList[0]

    def changeModel(self, index):
        self.model = self.modelList[index]
        self.thread.gridUpdated = True
        print(f"Model changed to {self.model}")

    # lazy-load the models so that frontend loading time is reduced
    def getKeras(self, name):
        filename = name.lower()
        if not hasattr(self, filename):
            print(f"Loading {name} model")
            from tensorflow.keras.models import load_model

            setattr(self, filename, load_model(f"models/{filename}.h5"))
        return getattr(self, filename)

    def predictKeras(self, name, grid):
        return self.getKeras(name).predict(np.array(grid).reshape(1, 28, 28))[0]

    def predict(self, grid):
        if self.model in self.kerasModels:
            prediction = self.predictKeras(self.model, grid)
        elif self.model == "SVM":
            prediction = np.zeros(10)
        return prediction

    def setGrid(self, grid):
        self.thread.grid = grid
        self.thread.gridUpdated = True

    def getMnist(self):
        if self.mnist is None:
            print("Loading MNIST dataset")
            from tensorflow.keras.datasets import mnist

            (_, _), (self.mnist, _) = mnist.load_data()
            self.mnist = self.mnist / 255.0
        return self.mnist
