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


class Output(QLabel):
    def __init__(self):
        super().__init__()

        self.width = 300
        self.height = 30
        self.radius = 20

        canvas = QtGui.QPixmap(self.width, self.height)
        canvas.fill(Qt.white)
        self.setPixmap(canvas)

    def setConfidence(self, confidence):
        """Color a grid of 10 circles according to the confidence"""
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        p = painter.pen()

        spacing = int(
            (self.width - len(confidence * self.radius)) / (len(confidence) + 1)
        )

        for i in range(len(confidence)):
            x = i * (self.radius + spacing) + spacing
            y = int((self.height - self.radius) / 2)
            if i == np.argmax(confidence):
                p.setColor(Qt.red)
                p.setWidth(2)
            else:
                p.setColor(Qt.black)
                p.setWidth(1)
            color = QtGui.QColor(0, 0, 0, int(np.power(confidence[i], 3) * 255))
            painter.setPen(p)
            painter.setBrush(color)
            painter.drawEllipse(x, y, self.radius, self.radius)

        painter.end()
        self.setPixmap(canvas)
