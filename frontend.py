import sys
import numpy as np
from functools import partial

from PySide6 import QtGui, QtWidgets, QtCore, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
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
)


class MainUi(QMainWindow):
    """This is the class that provides the main ui of the application"""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("Handwritten Digit Recognition")
        # self.setFixedSize(235, 235)

        # Set the central widget and the general layout
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self._mainLayout = QVBoxLayout()
        self._centralWidget.setLayout(self._mainLayout)

        # Create layouts
        self._createMenu()
        self._createTitle()

        self._bodyLayout = QHBoxLayout()
        self._createInput(self._bodyLayout)
        self._createOutput(self._bodyLayout)
        self._mainLayout.addLayout(self._bodyLayout)

    def _createMenu(self):
        self.file = self.menuBar().addMenu("&File")
        self.file.addAction("&Exit", self.close)
        self.inputSelector = self.menuBar().addMenu("&Input Device")
        self.inputSelector.addAction("&Camera 1", self.close)

    def _createTitle(self):
        # create the title with the two buttons
        layout = QHBoxLayout()

        title = QLabel("Handwritten Digit Classifier")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 20px;")
        layout.addWidget(title)

        self._instButton = QPushButton("Instructions")
        layout.addWidget(self._instButton)

        self._modeButton = QComboBox()
        self._modeButton.addItems(["Handwriting", "Webcam"])
        layout.addWidget(self._modeButton)

        self._modelButton = QComboBox()
        self._modelButton.addItems(["CNN", "SVM", "KNN", "MLP"])
        layout.addWidget(self._modelButton)

        self._mainLayout.addLayout(layout)
        self._mainLayout.addSpacing(20)

    def _createInput(self, parent):
        # create the left input side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Input"))
        self._canvas = Canvas()
        self._canvas.setFrameShape(QFrame.Box)
        layout.addWidget(self._canvas)

        self._clearButton = QPushButton("Clear")
        self._clearButton.clicked.connect(self._canvas.clear)
        layout.addWidget(self._clearButton)

        parent.addLayout(layout)

    def _createOutput(self, parent):
        # create the right output side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Output"))
        self._output = Output()
        self._output.setFrameShape(QFrame.Box)
        self._output.setConfidence(confidence)
        layout.addWidget(self._output)

        layout.addWidget(QLabel("Information Summary"))

        self._infoFrame = QLabel()
        self._infoFrame.setFrameShape(QFrame.Box)
        self._infoFrame.setMinimumSize(200, 100)
        layout.addWidget(self._infoFrame)

        layout.addStretch()
        parent.addLayout(layout)


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        canvas = QtGui.QPixmap(300, 300)
        canvas.fill(QtGui.Qt.white)
        self.setPixmap(canvas)

        self.last_x, self.last_y = None, None

    def clear(self):
        canvas = self.pixmap()
        canvas.fill(QtGui.Qt.white)
        self.setPixmap(canvas)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        p = painter.pen()
        p.setWidth(4)
        p.setColor(Qt.black)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.setPixmap(canvas)

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class Output(QLabel):
    def __init__(self):
        super().__init__()

        self._width = 300
        self._height = 30
        self._radius = 20

        canvas = QtGui.QPixmap(self._width, self._height)
        canvas.fill(QtGui.Qt.white)
        self.setPixmap(canvas)

    def setConfidence(self, confidence):
        """Color a grid of 10 circles according to the confidence"""
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        p = painter.pen()

        spacing = (self._width - len(confidence * self._radius)) / (len(confidence) + 1)

        for i in range(len(confidence)):
            x = i * (self._radius + spacing) + spacing
            y = (self._height - self._radius) / 2
            if i == np.argmax(confidence):
                p.setColor(Qt.red)
                p.setWidth(2)
            else:
                p.setColor(Qt.black)
                p.setWidth(1)
            color = QtGui.QColor(0, 0, 0, np.power(confidence[i], 3) * 255)
            painter.setPen(p)
            painter.setBrush(color)
            painter.drawEllipse(x, y, self._radius, self._radius)

        painter.end()
        self.setPixmap(canvas)


class Controller:
    """This is the class that provides the actions that happen when a signal is received"""

    def __init__(self, view, model):
        """Controller initializer."""
        self._view = view
        self._model = model
        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):
        pass


class Model:
    """This is the class that provides the business logic for the UI"""

    def __init__(self):
        pass


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = MainUi()
    view.show()
    # Create instances of the model and the controller
    Controller(view, Model())
    # Execute calculator's main loop
    sys.exit(app.exec())


confidence = [0.4, 0, 0, 0.8, 0, 0.3, 0.99, 0, 0.5, 0]

if __name__ == "__main__":
    main()
