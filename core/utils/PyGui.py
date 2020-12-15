from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import sys
import logging
import Constant

LOGGING = logging.getLogger("CocAssistant.GUI")


class Window(QDialog):
    m_lable = None
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle(Constant.AppWindowsName)
        self.resize(600, 400)
        self.input = QLineEdit(self)
        self.input.resize(600, 400)

def initWindows() :
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    initWindows()