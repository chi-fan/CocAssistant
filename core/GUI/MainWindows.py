# # -*- coding: utf-8 -*-
import sys
import random
from Constant import AppWindowsName
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import QBasicTimer
from utils.Logger import getLogger
from utils import utils
import numpy as np

LOGGING = getLogger("CocAssistant.MainWindows")

class MyWidget(QtWidgets.QWidget) :
    sendSendExecute = QtCore.Signal(str)
    signalStop = QtCore.Signal()
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setWindowTitle(AppWindowsName)
        self.layout = QtWidgets.QVBoxLayout()
        self.labelRemote = QLabel(self)
        self.layout.addWidget(self.labelRemote)

        self.textShow = QTextBrowser(self)
        self.layout.addWidget(self.textShow)

        self.textInput = QLineEdit(self)
        self.textInput.returnPressed.connect(self.inputText)
        self.layout.addWidget(self.textInput)

        self.setLayout(self.layout)
        LOGGING.info("GUI start")

    @QtCore.Slot()
    def showTextInTextBrowser(self, text = None) :
        self.textShow.append(text)

    @QtCore.Slot(str)
    def inputText(self) :
        self.sendSendExecute.emit(self.textInput.text())

    @QtCore.Slot(np.ndarray)
    def refreshScreen(self, screen) :
        screen = utils.cvimgToQPixmap(screen)
        self.labelRemote.setPixmap(screen)
        self.labelRemote.repaint()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.refreshScreen()

    def closeEvent(self, event) :
        self.signalStop.emit()

if __name__ == "__main__" :
    app = QApplication([])
    widget = MyWidget()
    widget.resize(600, 500)
    widget.show()
    app.exec_()