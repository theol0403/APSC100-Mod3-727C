import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import draw

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import pyqtSignal, Qt, QThread


class Canvas(QLabel):
    grid_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)

        self.dim = 300
        self.pixel = 28
        self.scale = self.dim / self.pixel

        self.sigma = 0.6
        self.boost = 3

        self.last_x, self.last_y, self.text_x = None, None, None

        self.setPixmap(QtGui.QPixmap(self.dim, self.dim))
        self.setFixedSize(self.dim, self.dim)
        self.clear()

    def clear(self):
        self.grid_draw = np.zeros((self.pixel, self.pixel))
        self.grid = np.zeros((self.pixel, self.pixel))
        self.updateCanvas()

    def setGrid(self, grid):
        self.grid = grid
        self.updateCanvas()

    def updateCanvas(self):
        canvas = self.pixmap()
        canvas.fill(Qt.white)
        painter = QtGui.QPainter(canvas)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                opa = 255 - int(self.grid[j][i] * 255)
                color = QtGui.QColor(opa, opa, opa, 255)
                painter.setPen(color)
                painter.setBrush(color)
                painter.drawRect(
                    int(i * self.scale),
                    int(j * self.scale),
                    int(self.scale),
                    int(self.scale),
                )
        painter.end()
        self.setPixmap(canvas)
        self.grid_signal.emit(self.grid)

    def mouseMoveEvent(self, e):
        # convert the mouse position to grid position
        pos = e.pos()
        x = int(np.floor(pos.x() / self.dim * self.pixel))
        y = int(np.floor(pos.y() / self.dim * self.pixel))
        x = np.clip(x, 0, self.pixel - 1)
        y = np.clip(y, 0, self.pixel - 1)
        if self.last_x is None:
            self.last_x = x
            self.last_y = y
            return

        # set the grid value
        rr, cc = draw.line(self.last_x, self.last_y, x, y)
        if e.modifiers() & Qt.ControlModifier:
            self.grid_draw[cc, rr] = 0
        else:
            self.grid_draw[cc, rr] = 1

        self.grid = np.clip(
            gaussian_filter(
                self.grid_draw,
                sigma=(self.sigma, self.sigma),
            )
            * self.boost,
            0,
            1,
        )

        self.last_x = x
        self.last_y = y

        self.updateCanvas()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.clear()
