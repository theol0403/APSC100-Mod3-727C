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


class Model:
    """This is the class that provides the business logic for the UI"""

    def __init__(self):
        self.model = load_model("cnn.h5")

    def predict(self, grid):
        """Predict the output of the grid"""
        prediction = self.model.predict(np.array(grid).reshape(1, 28, 28))[0].tolist()
        return prediction


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = MainUi(Model())
    view.show()
    # Execute calculator's main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
