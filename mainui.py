from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)

from canvas import Canvas
from camera import Camera
from output import Output


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)


class MainUi(QMainWindow):
    """This is the class that provides the main ui of the application"""

    def __init__(self):
        """View initializer."""
        super().__init__()
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

        # Create ui
        self.createMenu()
        self.createTitle()

        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(QHLine())
        self.mainLayout.addSpacing(5)

        self.bodyLayout = QHBoxLayout()
        self.createInput(self.bodyLayout)
        self.bodyLayout.addSpacing(5)
        self.bodyLayout.addWidget(QVLine())
        self.bodyLayout.addSpacing(5)
        self.createOutput(self.bodyLayout)
        self.bodyLayout.addStretch()
        self.mainLayout.addLayout(self.bodyLayout)

        self.setFixedSize(640, 490)

    def createMenu(self):
        self.file = self.menuBar().addMenu("File")
        self.file.addAction("Exit", self.close)
        self.inputSelector = self.menuBar().addMenu("Input Device")

    def createTitle(self):
        # create the title
        layout = QHBoxLayout()

        title = QLabel("Handwritten Digit Classifier")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 20px;")
        layout.addWidget(title)

        layout.addStretch()

        self.instButton = QPushButton("Instructions")
        self.instButton.clicked.connect(self.showInst)
        layout.addWidget(self.instButton)

        self.mainLayout.addLayout(layout)

    def createInput(self, parent):
        # create the left input side
        layout = QVBoxLayout()

        # create input title
        title = QHBoxLayout()
        title.addWidget(QLabel("Input"))
        self.modeButton = QComboBox()
        self.modeButton.addItems(["Handwriting", "Webcam"])
        title.addWidget(self.modeButton)
        layout.addLayout(title)

        self.stack = QStackedLayout()
        self.createCanvas(self.stack)
        self.createCamera(self.stack)

        layout.addLayout(self.stack)
        parent.addLayout(layout)

    def createCanvas(self, stack):
        # create the input canvas
        layout = QVBoxLayout()
        self.canvas = Canvas()
        layout.addWidget(self.canvas)

        buttonLayout = QHBoxLayout()
        self.clearButton = QPushButton("Clear")
        buttonLayout.addWidget(self.clearButton, 1)

        self.randomButton = QPushButton("MNIST")
        buttonLayout.addWidget(self.randomButton, 1)

        self.sigmaSlider = QSlider(Qt.Horizontal)
        self.sigmaSlider.setMinimum(20)
        self.sigmaSlider.setMaximum(150)
        self.sigmaLabel = QLabel("Sigma")
        sigmaLayout = QVBoxLayout()
        sigmaLayout.addWidget(self.sigmaLabel)
        sigmaLayout.addWidget(self.sigmaSlider)
        buttonLayout.addLayout(sigmaLayout, 0)

        layout.addLayout(buttonLayout)

        canvasPage = QWidget()
        canvasPage.setLayout(layout)
        stack.addWidget(canvasPage)

    def createCamera(self, stack):
        # create the input canvas
        layout = QVBoxLayout()
        self.camera = Camera()
        layout.addWidget(self.camera)
        layout.addStretch()

        controlLayout = QGridLayout()

        self.threshLabel = QLabel("Threshold")
        controlLayout.addWidget(self.threshLabel, 0, 0)
        self.threshSlider = QSlider(Qt.Horizontal)
        self.threshSlider.setMinimum(50)
        self.threshSlider.setMaximum(255)
        controlLayout.addWidget(self.threshSlider, 1, 0)

        self.zoomLabel = QLabel("Zoom")
        controlLayout.addWidget(self.zoomLabel, 0, 1)
        self.zoomSlider = QSlider(Qt.Horizontal)
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(99)
        controlLayout.addWidget(self.zoomSlider, 1, 1)

        layout.addLayout(controlLayout)

        canvasPage = QWidget()
        canvasPage.setLayout(layout)
        stack.addWidget(canvasPage)

    def createOutput(self, parent):
        # create the right output side
        layout = QVBoxLayout()

        title = QHBoxLayout()
        title.addWidget(QLabel("Output"))
        self.modelButton = QComboBox()
        title.addWidget(self.modelButton)
        layout.addLayout(title)

        self.output = Output()
        self.output.setFrameShape(QFrame.Box)
        layout.addWidget(self.output)

        layout.addWidget(QLabel("Information Summary"))

        self.infoFrame = QLabel()
        self.infoFrame.setFrameShape(QFrame.Box)
        self.infoFrame.setAlignment(Qt.AlignTop)
        # self.infoFrame.setMinimumSize(300, 207)
        layout.addWidget(self.infoFrame)

        layout.addStretch()
        parent.addLayout(layout)

    def showInst(self):
        """Show the insructions dialog."""
        instDlg = QDialog(self)
        instDlg.setWindowTitle("Instructions")
        instDlg.layout = QVBoxLayout()
        inst = """
        - select model in output section
        - canvas mode:
            - draw a digit using the mouse or touchscreen
            - load a random MNIST digit
            - clear the canvas
            - ctrl-click to drag
            - shift-click to erase
            - adjust sigma to change blurring
        - camera mode:
            - scan a digit using a webcam
            - adjust threshold and zoom to isolate digit
            - select camera from menu
        """
        text = QLabel(inst, instDlg)
        instDlg.layout.addWidget(text)
        instDlg.setFixedSize(400, 250)
        instDlg.exec()
