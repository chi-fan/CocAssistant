# -*- coding: utf-8 -*-

import logging
import argparse
from utils.Logger import initLogging
from utils.PyGui import initWindows
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
    LOGGING.info("CocAssistant -- 部落冲突辅助 by chifan and HoneyGump\n")
    LOGGING.info('*' * 70)
