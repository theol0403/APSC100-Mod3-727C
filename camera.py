import numpy as np
import cv2

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import pyqtSignal, Qt, QThread


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, camera):
        super().__init__()
        self.run = True
        self.pause = True
        self.camera = camera

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.camera.camera)
        if not cap.isOpened():
            print("Cannot open camera")
            return
        while self.run:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        self.run = False
        self.wait()


class Camera(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)

        self.dim = 300

        canvas = QtGui.QPixmap(self.dim, self.dim)
        canvas.fill(Qt.black)
        self.setPixmap(canvas)
        self.setFixedSize(self.dim, self.dim)

        # search for cameras
        self.findCameras()
        self.camera = self.cameras[0]

        self.thread = None

    def start(self):
        # create the video capture thread
        self.thread = VideoThread(self)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update)
        # start the thread
        self.thread.start()

    def stop(self):
        if self.thread:
            self.thread.stop()
            self.thread = None

    def restart(self):
        self.stop()
        self.start()

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

    def findCameras(self):
        """Returns a list of available cameras using opencv"""
        self.cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.cameras.append(i)
            cap.release()

    def listCameras(self):
        return ["Camera " + str(i) for i in self.cameras]

    def setCamera(self, i):
        self.camera = self.cameras[i]
