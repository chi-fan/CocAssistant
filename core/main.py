# # -*- coding: utf-8 -*-

from android.adb import ADB
from android.javacap import Javacap
from utils import utils
from utils import aircv
import cv2
import numpy as np
import sys
import random
from Constant import AppWindowsName
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout
from PySide6.QtCore import QBasicTimer

def cvimgToQPixmap(cvImage):
    cvImage=cv2.resize(src=cvImage,dsize=None,fx=0.2,fy=0.2)
    cvImage=cv2.cvtColor(cvImage,cv2.COLOR_BGR2RGB)
    image = QtGui.QImage(cvImage[:],cvImage.shape[1], cvImage.shape[0], cvImage.shape[1] * 3, QtGui.QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(image)
    return pixmap

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setWindowTitle(AppWindowsName)
        instAdb = ADB("127.0.0.1:62001")
        self.instJavacap = Javacap(instAdb)
        self.labelRemote = QLabel(self)
        self.button = QtWidgets.QPushButton("refreshScreen")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.labelRemote)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)
        #新建一个QTimer对象
        self.timer = QBasicTimer() # QTimer()貌似不行，不知何故？
        self.timer.start(33, self)

    @QtCore.Slot()
    def magic(self):
        self.refreshScreen()

    def refreshScreen(self) :
        # while True :
            screen = self.instJavacap.get_frame_from_stream()
            screen = utils.string_2_img(screen)
            screen = cvimgToQPixmap(screen)
            self.labelRemote.setPixmap(screen)
            # self.labelRemote.repaint()

     # 覆写计时器事件处理函数timerEvent()
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.refreshScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.resize(600, 500)
    widget.show()
    widget.refreshScreen()
    app.exec_()