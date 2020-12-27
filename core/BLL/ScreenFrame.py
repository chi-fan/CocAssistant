# -*- coding: utf-8 -*-
from android.adb import ADB
from android.javacap import Javacap
import threading
from utils import utils, aircv
from utils.Logger import getLogger
from error import DeviceConnectionError
from .QtUtils import SendLoggingToQt
from threading import Timer

LOGGING = getLogger("CocAssistant.ScreenFrame")

class ScreenFrame (object) :
    def __init__(self, sendLoggingToQt) :
        instAdb = ADB("127.0.0.1:62001")
        self.instJavacap = Javacap(instAdb)
        self.sendLoggingToQt = sendLoggingToQt

    def start(self) :
        self._thread = Timer(0.01, self._monitor)
        self._thread.start()

    def stop(self) :
        self._thread.cancel()
        self._thread = None

    def _monitor(self):
        screen = self.getFrame()
        screen = utils.string_2_img(screen)
        # aircv.imwrite(".\\temp\\screen.jpg", screen, 10)
        if not self.sendLoggingToQt.stop :
            self.sendLoggingToQt.sendLogArray(screen)
            self.start()

    def getFrame(self, stop = None) :
        try :
            screen = self.instJavacap.get_frame_from_stream(stop)
        except StopIteration :
            LOGGING.info("disconnect device")
        else :
            return screen
