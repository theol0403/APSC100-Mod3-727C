import numpy as np

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


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
            color = QtGui.QColor(0, 0, 0, int(self.confidence[i] * 255))
            painter.setBrush(color)
            painter.setPen(Qt.black)
            painter.drawEllipse(x, cy, self.diam, self.diam)
            if i == np.argmax(self.confidence):
                painter.setPen(Qt.red)
            painter.drawText(
                int(x + self.diam / 2 - self.fontSize / 4),
                int(ty),
                str(i),
            )

        painter.end()
        self.setPixmap(canvas)
