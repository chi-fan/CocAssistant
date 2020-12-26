from utils.Logger import getLogger
from PySide6.QtCore import QObject, Signal, Slot
from .LoggingToGui import SendLoggingToQt
import subprocess

LOGGING = getLogger("CocAssistant.Execute")

class Execute(QObject) :

    def __init__(self, m_sendLogging) :
        self._sendLogging = m_sendLogging

    @Slot(str)
    def execture(self, text = None) :
        LOGGING.info('hello ' + text)

