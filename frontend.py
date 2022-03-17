import sys
import numpy as np

from PyQt5.QtWidgets import QApplication

from mainui import MainUi


class Controller:
    """This class connects the buttons of the UI with model and other parts of the UI"""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connectSignals()

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
        mnist = self.model.getMnist()
        rand = np.random.randint(0, len(mnist))
        self.view.canvas.grid = mnist[rand].reshape(28, 28)
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

        # lazy-load the models so that frontend loading time is reduced
        self.mnist = None
        self.cnn = None

    def changeModel(self, index):
        self.model = self.modelList[index]
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

    def predict(self, grid):
        if self.model == "CNN":
            prediction = self.getCnn().predict(np.array(grid).reshape(1, 28, 28))[0]
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
