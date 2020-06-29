from print_screen import *
from PIL import Image
from adb import Screenshot
import re
from image_deal import *
from myfont import *
from myfont_chinese import *
import threading

from findpoints import screenshort_new,isindex,troop_store


class event_list() :
    my_event_list = []
    lock = None    #申请一个线程锁
    def __init__(self):
        self.lock = threading.Lock()
        return

    def appendEvent(self, event) :
        self.lock.acquire()
        self.my_event_list.append(event)
        self.lock.release()


    def popEvent(self, num = 0) :
        self.lock.acquire()
        if len(self.my_event_list) == 0 :
            return
        self.my_event_list.pop(num)
        self.lock.release()

    def runEvent(self) :
        print("____________________________________________________________________\n")
        print("                               吃饭和island的coc辅助工具")
        print("____________________________________________________________________\n")
        while True :
            if len(self.my_event_list) == 0 :
                # print("等待事件插入")
                continue
            else :
                print(self.my_event_list[0][0])
                self.my_event_list[0][1]()
                if self.my_event_list[0][2] != None :
                    self.appendEvent(self.my_event_list[0][2])
                self.popEvent()


request_init = None

def donte_event_() :
    if not isindex() :
        #  error deal
        print("error: this is not index!")
    print(box)
    Click(box[1] + 12, box[2] + 240)
    time.sleep(0.5)
    img = screenshort_new("screenshort.png")
    request_init = get_inf(img, myfont, myfont_chinese)
    contribute(box, request_init)
    Click(box[0] + 393, box[1] + 240)
    print("donte_event_")
    return

def build_event_() :
    if not isindex() :
        #  error deal
        print("error: this is not index!")
    Click(box[1] + 37, box[2] + 400)
    time.sleep(0.5)
    img = screenshort_new("screenshort.png")
    army_list = get_army_inf(img, myfont)
    if army_list == None  :
        return
    print(army_list)

    #19个mm ，15 个气球 9个法师 3条龙 2个皮卡
    print(request_init)
    build_all(box, request_init)


    # Click(box[0] + 393, box[1] + 240)
    print("build_event_")
    return

def coloct_event_() :
    time.sleep(5)
    print("coloct_event_")
    timer = threading.Timer(0, coloct_event_test)
    timer.start()
    return


def coloct_event_test() :
    timer = threading.Timer(6, lambda  :  my_evet.appendEvent(coloct_event))
    timer.start()
    return

# cmd1=r"adb shell /system/bin/screencap -p /sdcard/screenshort.png"       #命令1：在手机上截图3.png为图片名
# cmd2=r"adb pull /sdcard/screenshort.png C:\Users\Administrator\Desktop\LB_LAST"                        #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
# screen=Screenshot()
myfont = my_ocr('army')
myfont_chinese = my_ocr_chinese()
build_event = ["build", build_event_, None]
donte_event = ["donte", donte_event_, build_event]
build_event[2] = donte_event
box =  find_box_window()
print(box)
coloct_event = ["coloct",  coloct_event_, None]

my_evet = event_list()
my_evet.appendEvent(donte_event)
# coloct_event_test()
my_evet.runEvent()

# donte_event_()




