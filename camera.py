import numpy as np
import cv2

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import pyqtSignal, Qt, QThread


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.run = True
        self.pause = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self.run:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.run = False
        self.wait()


class Camera(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)

        self.dim = 300

        self.setPixmap(QtGui.QPixmap(self.dim, self.dim))
        self.setFixedSize(self.dim, self.dim)

    def start(self):
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update)
        # start the thread
        self.thread.start()

    def stop(self):
        self.thread.stop()

    def closeEvent(self, event):
        self.stop()
        event.accept()

    def update(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.readCv(cv_img)
        self.setPixmap(qt_img)

    def readCv(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )
        p = convert_to_Qt_format.scaled(
            self.dim, self.dim, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        return QPixmap.fromImage(p)
