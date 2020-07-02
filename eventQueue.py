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

    def setEvent(self, interval, event) :
            timer = recycleTimer(interval, lambda : self.appendEvent(event))
            timer.start()

    def runEvent(self) :
        while True :
            if len(self.my_eventList) == 0 :
                continue
            else :
                self.my_eventList[0]()
                self.popEvent()


class recycleTimer(threading.Timer) :
    ''' 继承timer类 重写run() 以实现重复定时器 '''
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)
