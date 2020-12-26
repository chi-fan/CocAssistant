from PySide6.QtCore import QObject, Signal, Slot
import numpy as np

class SendLoggingToQt(QObject) :
    sendLogging = Signal((str,), (bytes,), (np.ndarray))

    def sendLog(self, text) :
        self.sendLogging.emit(text)

    def sendLogBytes(self, text) :
        self.sendLogging[bytes].emit(text)

    def sendLogArray(self, text) :
        self.sendLogging[np.ndarray].emit(text)
