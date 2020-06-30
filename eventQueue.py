import threading

class eventQueue() :
    my_eventList = []
    lock = None
    def __init__(self):
        self.lock = threading.Lock()

    def appendEvent(self, event) :
        self.lock.acquire()
        self.my_eventList.append(event)
        self.lock.release()

    def popEvent(self, num = 0) :
        self.lock.acquire()
        if len(self.my_eventList) == 0 :
            return
        self.my_eventList.pop(num)
        self.lock.release()

    def runEvent(self) :
        while True :
            if len(self.my_eventList) == 0 :
                continue
            else :
                print(self.my_eventList[0][0])
                self.my_eventList[0][1]()
                if self.my_eventList[0][2] != None :
                    self.appendEvent(self.my_eventList[0][2])
                self.popEvent()