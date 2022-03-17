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
        self.height = 60
        self.diam = 20
        self.fontSize = 20

        canvas = QtGui.QPixmap(self.width, self.height)
        self.setPixmap(canvas)

        self.confidence = np.zeros(10)
        self.redraw()

    def setConfidence(self, confidence):
        self.confidence = confidence
        self.redraw()

    def redraw(self):
        canvas = self.pixmap()
        canvas.fill(Qt.white)
        painter = QtGui.QPainter(canvas)
        p = painter.pen()

        font = painter.font()
        font.setPixelSize(self.fontSize)
        painter.setFont(font)

        spacing = int(
            (self.width - len(self.confidence) * self.diam) / (len(self.confidence) + 1)
        )

        for i in range(len(self.confidence)):
            x = i * (self.diam + spacing) + spacing
            cy = int((self.height - self.diam) / (3 / 2)) + 4
            ty = int((self.height) / (3 / 1)) + 4
            if i == np.argmax(self.confidence):
                p.setColor(Qt.red)
                p.setWidth(2)
            else:
                p.setColor(Qt.black)
                p.setWidth(1)
            color = QtGui.QColor(0, 0, 0, int(self.confidence[i] * 255))
            painter.setPen(p)
            painter.setBrush(color)
            painter.drawEllipse(x, cy, self.diam, self.diam)
            painter.drawText(
                int(x + self.diam / 2 - self.fontSize / 4),
                int(ty),
                str(i),
            )

        painter.end()
        self.setPixmap(canvas)
