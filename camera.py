import numpy as np

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame


class Camera(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)

        self.dim = 300

        self.setPixmap(QtGui.QPixmap(self.dim, self.dim))
        self.clear()
