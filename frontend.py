import sys
from functools import partial

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
        self._createTitle()

        self._bodyLayout = QHBoxLayout()
        self._createInput(self._bodyLayout)
        self._createOutput(self._bodyLayout)
        self._mainLayout.addLayout(self._bodyLayout)

    def _createTitle(self):
        # create the title with the two buttons
        layout = QHBoxLayout()

        title = QLabel("Handwritten Digit Classifier")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 20px;")
        layout.addWidget(title)

        self._instButton = QPushButton("Instructions")
        layout.addWidget(self._instButton)

        self._modeButton = QPushButton("Mode")
        layout.addWidget(self._modeButton)

        self._mainLayout.addLayout(layout)
        self._mainLayout.addSpacing(20)

    def _createInput(self, parent):
        # create the left input side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Input"))
        self._inputFrame = QFrame()
        self._inputFrame.setFrameShape(QFrame.Box)
        self._inputFrame.setMinimumSize(200, 200)
        layout.addWidget(self._inputFrame)

        self._clearButton = QPushButton("Clear")
        layout.addWidget(self._clearButton)

        parent.addLayout(layout)

    def _createOutput(self, parent):
        # create the right output side
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Output"))
        self._outputFrame = QFrame()
        self._outputFrame.setFrameShape(QFrame.Box)
        self._outputFrame.setMinimumSize(200, 50)
        layout.addWidget(self._outputFrame)

        layout.addWidget(QLabel("Information Summary"))

        self._infoFrame = QFrame()
        self._infoFrame.setFrameShape(QFrame.Box)
        self._infoFrame.setMinimumSize(200, 100)
        layout.addWidget(self._infoFrame)

        layout.addStretch()
        parent.addLayout(layout)


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


if __name__ == "__main__":
    main()