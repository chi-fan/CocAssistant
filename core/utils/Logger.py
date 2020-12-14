import logging
import os
ThisPath = os.path.dirname(os.path.realpath(__file__))
LogFile = os.path.join(ThisPath, '../temp/cocAssistant.log')
# from Constant import LogFile

def initLogging() :
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            encoding='utf-8',
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

if __name__ == "__main__" :
    initLogging()

