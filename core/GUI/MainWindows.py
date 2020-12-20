# # -*- coding: utf-8 -*-
import sys
import random
from android.adb import ADB
from android.javacap import Javacap
from utils import utils, aircv
from Constant import AppWindowsName
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import QBasicTimer
from utils.Logger import getLogger

LOGGING = getLogger("CocAssistant.MainWindows")

class MyWidget(QtWidgets.QWidget) :
    sendSendExecute = QtCore.Signal(str)
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setWindowTitle(AppWindowsName)
        instAdb = ADB("127.0.0.1:62001")
        self.instJavacap = Javacap(instAdb)
        self.layout = QtWidgets.QVBoxLayout()

        self.labelRemote = QLabel(self)
        self.layout.addWidget(self.labelRemote)

        self.textShow = QTextBrowser(self)
        self.layout.addWidget(self.textShow)

        self.textInput = QLineEdit(self)
        self.textInput.returnPressed.connect(self.inputText)
        self.layout.addWidget(self.textInput)

        self.setLayout(self.layout)
        self.timer = QBasicTimer()
        self.timer.start(33, self)
        self.refreshScreen()

    @QtCore.Slot()
    def showTextInTextBrowser(self, text = None) :
        self.textShow.append(text)

    @QtCore.Slot()
    def inputText(self) :
        self.sendSendExecute.emit(self.textInput.text())

    def refreshScreen(self) :
        screen = self.instJavacap.get_frame_from_stream()
        screen = utils.string_2_img(screen)
        screen = utils.cvimgToQPixmap(screen)
        self.labelRemote.setPixmap(screen)
        self.labelRemote.repaint()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.refreshScreen()

if __name__ == "__main__" :
    app = QApplication([])
    widget = MyWidget()
    widget.resize(600, 500)
    widget.show()
    app.exec_()