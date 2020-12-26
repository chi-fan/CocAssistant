# # -*- coding: utf-8 -*-

from utils.Logger import getLogger, initLogging
from GUI.MainWindows import MyWidget
from PySide6.QtWidgets import QApplication
from BLL.LoggingToGui import LoggingToGui
from Constant import AppWindowsName
import queue
from BLL.Execute import Execute
from BLL.ScreenFrame import ScreenFrame
from BLL.QtUtils import SendLoggingToQt
import numpy as np

LOGGING = getLogger("CocAssistant.Main")

if __name__ == "__main__" :
    myQueue = queue.Queue(100)
    initLogging(myQueue)
    m_sendLoggingToQt = SendLoggingToQt()
    m_LoggingToGui = LoggingToGui(myQueue, m_sendLoggingToQt)
    m_LoggingToGui.start()
    m_execute = Execute(m_sendLoggingToQt)

    m_sendLoggingToQt2 = SendLoggingToQt()
    screenFrame = ScreenFrame(m_sendLoggingToQt2)

    app = QApplication([])
    widget = MyWidget()

    m_sendLoggingToQt2.sendLogging[np.ndarray].connect(widget.refreshScreen)

    m_sendLoggingToQt.sendLogging.connect(widget.showTextInTextBrowser)
    widget.sendSendExecute.connect(m_execute.execture)
    widget.resize(600, 500)
    widget.show()
    LOGGING.info("*" * 50)
    LOGGING.info(AppWindowsName)
    LOGGING.info("*" * 50)

    screenFrame.start()

    app.exec_()
