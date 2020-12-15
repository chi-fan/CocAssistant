# -*- coding: utf-8 -*-

import logging
import argparse
from utils.Logger import initLogging
from utils.PyGui import initWindows
from Constant import AppWindowsName
from android.adb import ADB
from android.javacap import Javacap
from utils import utils
from utils import aircv
LOGGING = logging.getLogger("CocAssistant.main")

def enableGui() :
    initWindows()

def initArgparse() :
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-g", "--GUI", help="enable GUI for this App",
                        action="store_true")
    args = parser.parse_args()
    if args.GUI:
        enableGui()

if __name__ == "__main__" :
    initLogging()
    initArgparse()
    LOGGING.info('*' * 70)
    LOGGING.info(AppWindowsName)
    LOGGING.info('*' * 70)

    instAdb = ADB("127.0.0.1:62001")
    instJavacap = Javacap(instAdb)
    screen = instJavacap.get_frame_from_stream()
    print(len(screen))
    filename="./core/temp/screen.jpg"
    ensure_orientation=True
    quality=10
    max_size=None
    # output cv2 object
    screen = utils.string_2_img(screen)

    aircv.imwrite(filename, screen, quality)