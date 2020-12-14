import threading

class recycleTimer(threading.Timer) :
    ''' 继承timer类 重写run() 以实现重复定时器 '''
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)

# timer = recycleTimer(1, lambda : print("hello"))
# timer.start()
