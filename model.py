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

        self.modelList = ["CNN", "SVM", "KNN", "MLP"]
        self.model = self.modelList[0]

        # lazy-load the models so that frontend loading time is reduced
        self.mnist = None
        self.cnn = None
        self.mlp = None

    def changeModel(self, index):
        self.model = self.modelList[index]
        self.thread.gridUpdated = True
        print(f"Model changed to {self.model}")

    # load the models on demand
    def getMnist(self):
        if self.mnist is None:
            print("Loading MNIST dataset")
            from tensorflow.keras.datasets import mnist

            (_, _), (self.mnist, _) = mnist.load_data()
            self.mnist = self.mnist / 255.0
        return self.mnist

    def getCnn(self):
        if self.cnn is None:
            print("Loading CNN model")
            from tensorflow.keras.models import load_model

            self.cnn = load_model("cnn.h5")
        return self.cnn

    def getMlp(self):
        if self.mlp is None:
            print("Loading MLP model")
            from tensorflow.keras.models import load_model

            self.mlp = load_model("mlp_dropout.h5")
        return self.mlp

    def predict(self, grid):
        if self.model == "CNN":
            prediction = self.getCnn().predict(np.array(grid).reshape(1, 28, 28))[0]
        elif self.model == "SVM":
            prediction = np.zeros(10)
        if self.model == "MLP":
            prediction = self.getMlp().predict(np.array(grid).reshape(1, 28, 28))[0]
        return prediction

    def setGrid(self, grid):
        self.thread.grid = grid
        self.thread.gridUpdated = True
