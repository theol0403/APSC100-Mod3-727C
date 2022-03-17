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
        painter.setBrush(Qt.black)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    painter.drawRect(
                        int(i * self.scale),
                        int(j * self.scale),
                        int(self.scale),
                        int(self.scale),
                    )
        painter.end()
        self.setPixmap(canvas)

    def mouseMoveEvent(self, e):
        pos = e.pos()
        x = int(np.floor(pos.x() / self.dim * self.pixel))
        y = int(np.floor(pos.y() / self.dim * self.pixel))
        x = np.clip(x, 0, self.pixel - 1)
        y = np.clip(y, 0, self.pixel - 1)
        self.grid[x][y] = 1
        self.updateCanvas()
