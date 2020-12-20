# # -*- coding: utf-8 -*-

from utils.Logger import getLogger, initLogging
from GUI.MainWindows import MyWidget
from PySide6.QtWidgets import QApplication
from BLL.LoggingToGui import LoggingToGui, sendLoggingToQt
from Constant import AppWindowsName
import queue

LOGGING = getLogger("CocAssistant.Main")
myQueue = queue.Queue(100)

if __name__ == "__main__" :
    initLogging(myQueue)
    m_sendLoggingToQt = sendLoggingToQt()
    m_LoggingToGui = LoggingToGui(myQueue, m_sendLoggingToQt)
    m_LoggingToGui.start()
    app = QApplication([])
    widget = MyWidget()
    m_sendLoggingToQt.sendLogging.connect(widget.showTextInTextBrowser)
    widget.resize(600, 500)
    widget.show()
    LOGGING.info("*" * 50)
    LOGGING.info(AppWindowsName)
    LOGGING.info("*" * 50)
    app.exec_()