import sys
import numpy as np
from functools import partial

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

from canvas import Canvas
from output import Output


class MainUi(QMainWindow):
    """This is the class that provides the main ui of the application"""

    def __init__(self, model):
        """View initializer."""
        super().__init__()
        self.model = model
        # Set some main window's properties
        self.setWindowTitle("Handwritten Digit Recognition")
        # self.setFixedSize(235, 235)

        # set icon
        self.setWindowIcon(QtGui.QIcon("icon.png"))

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
        self.modeButton.addItems(["Handwriting", "Webcam"])
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
        self.canvas.setToImage()

    def createInput(self, parent):
        # create the left input side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Input"))
        self.canvas = Canvas()
        self.canvas.setFrameShape(QFrame.Box)
        layout.addWidget(self.canvas)

        buttonLayout = QHBoxLayout()
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.canvas.clear)
        buttonLayout.addWidget(self.clearButton)

        self.predictButton = QPushButton("Predict")
        self.predictButton.clicked.connect(self.predict)
        buttonLayout.addWidget(self.predictButton)

        self.randomButton = QPushButton("Random")
        self.randomButton.clicked.connect(self.canvas.setToMnist)
        buttonLayout.addWidget(self.randomButton)

        layout.addLayout(buttonLayout)

        parent.addLayout(layout)

    def createOutput(self, parent):
        # create the right output side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Output"))
        self.output = Output()
        self.output.setFrameShape(QFrame.Box)
        layout.addWidget(self.output)

        layout.addWidget(QLabel("Information Summary"))

        self.infoFrame = QLabel()
        self.infoFrame.setFrameShape(QFrame.Box)
        layout.addWidget(self.infoFrame)

        layout.addStretch()
        parent.addLayout(layout)

    def predict(self):
        self.output.setConfidence(self.model.predict([self.canvas.grid]))
