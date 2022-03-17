import sys
import numpy as np
from functools import partial
from PIL import Image
from PIL.ImageQt import ImageQt

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

from tensorflow.keras.datasets import mnist

(train_x, train_y), (test_x, test_y) = mnist.load_data()
train_x = train_x / 255.0
test_x = test_x / 255.0


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

    def updateCanvas(self):
        canvas = self.pixmap()
        canvas.fill(Qt.white)
        painter = QtGui.QPainter(canvas)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                color = QtGui.QColor(0, 0, 0, int(self.grid[j][i] * 255))
                painter.fillRect(
                    int(i * self.scale),
                    int(j * self.scale),
                    int(self.scale),
                    int(self.scale),
                    color,
                )
        painter.end()
        self.setPixmap(canvas)

    def mouseMoveEvent(self, e):
        pos = e.pos()
        x = int(np.floor(pos.x() / self.dim * self.pixel))
        y = int(np.floor(pos.y() / self.dim * self.pixel))
        x = np.clip(x, 0, self.pixel - 1)
        y = np.clip(y, 0, self.pixel - 1)
        self.grid[y][x] = 1
        self.updateCanvas()

    def setToImage(self):
        im = Image.open(r"icon.png")
        im = ImageQt(im).copy()
        self.setPixmap(QtGui.QPixmap.fromImage(im))
        # self.layout_plot.addWidget(label)

    def setToMnist(self):
        self.grid = test_x[np.random.randint(len(test_x))].reshape(28, 28).tolist()
        self.updateCanvas()
