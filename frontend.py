import sys
import numpy as np
from functools import partial
from tensorflow import keras
from keras.models import load_model

from PyQt5 import QtGui, QtWidgets, QtCore, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QComboBox,
    QDialog,
)

from mainui import MainUi


class Controller:
    """This is the class that provides the actions that happen when a signal is received"""

    def __init__(self, view, model):
        """Controller initializer."""
        self.view = view
        self.model = model
        # Connect signals and slots
        self.connectSignals()

        self.predict()

    def connectSignals(self):
        self.view.modelButton.addItems(self.model.modelList)
        self.view.modelButton.currentIndexChanged.connect(self.model.changeModel)
        self.view.modelButton.currentIndexChanged.connect(self.predict)

        self.view.canvas.mouseReleased = self.predict
        self.view.randomButton.clicked.connect(self.view.canvas.setToMnist)
        self.view.randomButton.clicked.connect(self.predict)

        self.view.clearButton.clicked.connect(self.view.canvas.clear)
        self.view.clearButton.clicked.connect(self.predict)

    def predict(self):
        confidence = self.model.predict([self.view.canvas.grid])
        self.view.output.setConfidence(confidence)
        prediction = np.argmax(confidence)
        percent = confidence[prediction] * 100

        text = ""
        text += f"Digit: {prediction} \n"
        text += f"Confidence: {percent:.2f} \n"
        text += f"------------------------------------ \n"
        text += f"Model: {self.model.model} \n"

        self.view.infoFrame.setText(text)


class Model:
    def __init__(self):
        self.modelList = ["CNN", "SVM", "KNN", "MLP"]
        self.model = self.modelList[0]

        self.loadModels()

    def loadModels(self):
        self.cnn = load_model("cnn.h5")

    def changeModel(self, index):
        self.model = self.modelList[index]
        print(f"Model changed to {self.model}")

    def predict(self, grid):
        if self.model == "CNN":
            prediction = self.cnn.predict(np.array(grid).reshape(1, 28, 28))[0]
        elif self.model == "SVM":
            prediction = np.zeros(10)
        return prediction


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = MainUi()
    view.show()
    model = Model()
    Controller(view, model)
    # Execute calculator's main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
