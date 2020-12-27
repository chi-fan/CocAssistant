# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import QueueHandler, QueueListener

ThisPath = os.path.dirname(os.path.realpath(__file__))
LogFile = os.path.join(ThisPath, '../temp/cocAssistant.log')

def initLogging(queue) :
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            filename=LogFile,
            filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
        datefmt='%I:%M:%S'
    )
    console.setFormatter(formatter)
    LOGGING = logging.getLogger("CocAssistant")
    LOGGING.addHandler(console)

    mqueue = QueueHandler(queue)
    LOGGING.addHandler(mqueue)

def getLogger(loggingName) :
    LOGGING = logging.getLogger(loggingName)
    return LOGGING

if __name__ == "__main__" :
    initLogging()
