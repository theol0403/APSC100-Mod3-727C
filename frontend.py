import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist

from PyQt5.QtWidgets import QApplication

from mainui import MainUi


class Controller:
    """This class connects the buttons of the UI with model and other parts of the UI"""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connectSignals()
        self.predict()

    def connectSignals(self):
        """Add actions to the UI elements"""
        self.view.modelButton.addItems(self.model.modelList)
        self.view.modelButton.currentIndexChanged.connect(self.model.changeModel)
        self.view.modelButton.currentIndexChanged.connect(self.predict)

        self.view.canvas.mouseReleased = self.predict
        self.view.randomButton.clicked.connect(self.displayMnist)
        self.view.randomButton.clicked.connect(self.predict)

        self.view.clearButton.clicked.connect(self.view.canvas.clear)
        self.view.clearButton.clicked.connect(self.predict)

    def displayMnist(self):
        self.view.canvas.clear()
        rand = np.random.randint(0, len(self.model.test_x))
        self.view.canvas.grid = self.model.test_x[rand].reshape(28, 28)
        self.view.canvas.updateCanvas()

    def predict(self):
        """Predict from the canvas grid using the model and then update the ui with the prediction"""
        confidence = self.model.predict([self.view.canvas.grid])
        self.view.output.setConfidence(confidence)

        # update the information summary
        prediction = np.argmax(confidence)
        percent = confidence[prediction] * 100

        text = ""
        text += f"Digit: {prediction} \n"
        text += f"Confidence: {percent:.2f} \n"
        text += f"------------------------------------ \n"
        text += f"Model: {self.model.model} \n"

        self.view.infoFrame.setText(text)


class Model:
    """This class contains and runs the ML models"""

    def __init__(self):
        self.modelList = ["CNN", "SVM", "KNN", "MLP"]
        self.model = self.modelList[0]

        self.loadModels()

    def loadModels(self):
        (_, _), (self.test_x, _) = mnist.load_data()
        self.test_x = self.test_x / 255.0

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
