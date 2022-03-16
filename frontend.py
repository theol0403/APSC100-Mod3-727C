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
    QDialog,
)


class MainUi(QMainWindow):
    """This is the class that provides the main ui of the application"""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("Handwritten Digit Recognition")
        # self.setFixedSize(235, 235)
        
        # set icon
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # Set the central widget and the general layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Create layouts
        self.createMenu()
        self.createTitle()

        self.bodyLayout = QHBoxLayout()
        self.createInput(self.bodyLayout)
        self.createOutput(self.bodyLayout)
        self.mainLayout.addLayout(self.bodyLayout)

    def createMenu(self):
        self.file = self.menuBar().addMenu("&File")
        self.file.addAction("&Exit", self.close)
        self.inputSelector = self.menuBar().addMenu("&Input Device")
        self.inputSelector.addAction("&Camera 1", self.close)

    def createTitle(self):
        # create the title with the two buttons
        layout = QHBoxLayout()

        title = QLabel("Handwritten Digit Classifier")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 20px;")
        layout.addWidget(title)

        self.instButton = QPushButton("Instructions")
        self.instButton.clicked.connect(self.showInst)
        layout.addWidget(self.instButton)

        self.modeButton = QComboBox()
        self.canvas = Canvas()
        self.modeButton.addItems(["Handwriting", "Webcam"])
        self.modeButton.currentIndexChanged.connect(self.canvas.changeBlack)
        
        layout.addWidget(self.modeButton)

        self.modelButton = QComboBox()
        self.modelList = ["CNN", "SVM", "KNN", "MLP"]
        self.modelButton.addItems(self.modelList)
        self.modelButton.currentIndexChanged.connect(self.changeModel)
        layout.addWidget(self.modelButton)

        layout.addStretch()

        self.mainLayout.addLayout(layout)
        self.mainLayout.addSpacing(20)

    def showInst(self):
        instDlg = QDialog(self)
        instDlg.setWindowTitle("Instructions")
        instDlg.layout = QVBoxLayout()
        text = QLabel("These are the instructions", instDlg)
        instDlg.layout.addWidget(text)
        instDlg.setFixedSize(300, 300)
        instDlg.exec()

    def changeModel(self, index):
        print(self.modelList[index])

    def createInput(self, parent):
        # create the left input side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Input"))
        self.canvas.setFrameShape(QFrame.Box)
        layout.addWidget(self.canvas)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.canvas.clear)
        layout.addWidget(self.clearButton)

        parent.addLayout(layout)

    def createOutput(self, parent):
        # create the right output side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Output"))
        self.output = Output()
        self.output.setFrameShape(QFrame.Box)
        self.output.setConfidence(confidence)
        layout.addWidget(self.output)

        layout.addWidget(QLabel("Information Summary"))

        self.infoFrame = QLabel()
        self.infoFrame.setFrameShape(QFrame.Box)
        self.infoFrame.setMinimumSize(200, 100)
        layout.addWidget(self.infoFrame)

        layout.addStretch()
        parent.addLayout(layout)


class Canvas(QLabel):
    def __init__(self):
        super().__init__()

        self.dim = 300
        self.pixel = 28
        self.scale = self.dim / self.pixel

        self.setPixmap(QtGui.QPixmap(self.dim, self.dim))
        self.clear()

    def clear(self):
        self.grid = np.zeros((self.pixel, self.pixel))
        self.updateCanvas()

    def changeBlack(self):
        self.grid = np.zeros((self.pixel, self.pixel))
        canvas.fill(QtGui.Qt.red)
        self.updateCanvas()

    def updateCanvas(self):
        canvas = self.pixmap()
        canvas.fill(QtGui.Qt.white)
        painter = QtGui.QPainter(canvas)
        painter.setBrush(Qt.black)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    painter.drawRect(
                        i * self.scale,
                        j * self.scale,
                        self.scale,
                        self.scale,
                    )
        painter.end()
        self.setPixmap(canvas)

    def mouseMoveEvent(self, e):
        pos = e.position()
        x = int(np.floor(pos.x() / self.dim * self.pixel))
        y = int(np.floor(pos.y() / self.dim * self.pixel))
        x = np.clip(x, 0, self.pixel - 1)
        y = np.clip(y, 0, self.pixel - 1)
        self.grid[x][y] = 1
        self.updateCanvas()


class Output(QLabel):
    def __init__(self):
        super().__init__()

        self.width = 300
        self.height = 30
        self.radius = 20

        canvas = QtGui.QPixmap(self.width, self.height)
        canvas.fill(QtGui.Qt.white)
        self.setPixmap(canvas)

    def setConfidence(self, confidence):
        """Color a grid of 10 circles according to the confidence"""
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        p = painter.pen()

        spacing = (self.width - len(confidence * self.radius)) / (len(confidence) + 1)

        for i in range(len(confidence)):
            x = i * (self.radius + spacing) + spacing
            y = (self.height - self.radius) / 2
            if i == np.argmax(confidence):
                p.setColor(Qt.red)
                p.setWidth(2)
            else:
                p.setColor(Qt.black)
                p.setWidth(1)
            color = QtGui.QColor(0, 0, 0, np.power(confidence[i], 3) * 255)
            painter.setPen(p)
            painter.setBrush(color)
            painter.drawEllipse(x, y, self.radius, self.radius)

        painter.end()
        self.setPixmap(canvas)


class Controller:
    """This is the class that provides the actions that happen when a signal is received"""

    def __init__(self, view, model):
        """Controller initializer."""
        self.view = view
        self.model = model
        # Connect signals and slots
        self.connectSignals()

    def connectSignals(self):
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


confidence = [0.4, 0, 0, 0.6, 0, 0.3, 0.99, 0, 0.5, 0]

if __name__ == "__main__":
    main()
