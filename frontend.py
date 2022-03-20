import sys
import numpy as np

from PyQt5.QtWidgets import QApplication

from mainui import MainUi
from model import Model


class Controller:
    """This class connects the buttons of the UI with model and other parts of the UI"""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connectSignals()
        self.index = 0

    def connectSignals(self):
        """Add actions to the UI elements"""
        self.view.modeButton.currentIndexChanged.connect(self.switchPage)

        self.view.clearButton.clicked.connect(self.view.canvas.clear)
        self.view.randomButton.clicked.connect(self.displayMnist)

        self.view.modelButton.addItems(self.model.modelList)
        self.view.modelButton.currentIndexChanged.connect(self.model.changeModel)

        self.view.cameraButton.addItems(self.view.camera.listCameras())
        self.view.cameraButton.currentIndexChanged.connect(self.view.camera.setCamera)
        self.view.cameraButton.currentIndexChanged.connect(self.view.camera.restart)

        self.view.threshSlider.valueChanged.connect(self.view.camera.setThresh)
        self.view.threshSlider.valueChanged.connect(self.updateSliders)
        self.view.threshSlider.setValue(self.view.camera.thresh)
        self.view.zoomSlider.valueChanged.connect(self.view.camera.setZoom)
        self.view.zoomSlider.valueChanged.connect(self.updateSliders)
        self.view.zoomSlider.setValue(self.view.camera.zoom)

        self.view.canvas.grid_signal.connect(self.model.setGrid)
        self.view.camera.grid_signal.connect(self.model.setGrid)
        self.model.thread.predict_signal.connect(self.setPrediction)

        self.view.closeEvent = self.stop

        self.updateSliders()

    def switchPage(self):
        self.index = self.view.modeButton.currentIndex()
        self.view.stack.setCurrentIndex(self.index)
        if self.index == 0:
            self.view.camera.stop()
        elif self.index == 1:
            self.view.camera.start()

    def displayMnist(self):
        mnist = self.model.getMnist()
        rand = np.random.randint(0, len(mnist))
        self.view.canvas.setGrid(mnist[rand].reshape(28, 28))

    def setPrediction(self, confidence, time_wall):
        self.view.output.setConfidence(confidence)

        # update the information summary
        prediction = np.argmax(confidence)
        percent = confidence[prediction] * 100

        text = ""
        text += f"Digit: {prediction} \n"
        text += f"Confidence: {percent:.2f}% \n"
        text += f"Processing Time: {time_wall*1000:.0f} ms \n"
        text += f"------------------------------------ \n"
        text += f"Model: {self.model.model} \n"

        self.view.infoFrame.setText(text)

    def updateSliders(self):
        self.view.threshLabel.setText(f"Threshold: {self.view.threshSlider.value()}")
        self.view.zoomLabel.setText(f"Zoom: {self.view.zoomSlider.value()}")

    def stop(self, e):
        self.model.thread.stop()
        self.view.camera.stop()


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    # Show the calculator's GUI
    view = MainUi()
    view.show()
    model = Model()
    controller = Controller(view, model)
    # Execute calculator's main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
