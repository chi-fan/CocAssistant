import time
from recycleTimer import recycleTimer

def buildEvent() :
    print("build")

def collectEvent() :
    print("collect")

def donateEvent():
    print("donate")

def recycleEvent(interval, function) :
    time = recycleTimer(interval, function)
    time.start()

if __name__ == "__main__":
    print("_" * 100 + "\n")
    print(" " * 40 + "吃饭和island的coc辅助工具")
    print("_" * 100)
    recycleEvent(5, buildEvent)
    recycleEvent(6, collectEvent)
    recycleEvent(1, donateEvent)

    #ctrl + c 无法关闭子进程，待思考




