import time
import eventQueue as EQ

def buildEvent() :
    print("build")

def collectEvent() :
    print("collect")

def donateEvent():
    print("donate")

if __name__ == "__main__":
    print("_" * 100 + "\n")
    print(" " * 40 + "吃饭和island的coc辅助工具")
    print("_" * 100)
    mainEventQueue = EQ.eventQueue()
    # mainEventQueue.setEvent(5, buildEvent)
    # mainEventQueue.setEvent(6, collectEvent)
    # mainEventQueue.setEvent(10, donateEvent)
    # mainEventQueue.runEvent()


    #ctrl + c 无法关闭子进程，待思考




