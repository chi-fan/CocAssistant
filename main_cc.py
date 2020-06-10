from print_screen import *
from PIL import Image
from adb import Screenshot
import pytesseract
import re
from image_deal import *
from myfont import *
from myfont_chinese import *
import threading

# img2 = Image.open('13.png')
# img2 = cut_image(img2, (0, 51,  376, 484))
# # img2 = deal_image(img2, lambda x, y, z : x != 160  and y != 160 and z != 155  )
# img2.save('58' + '.png', 'PNG')

# img2 = Image.open('13.png')
# img2 = cut_image(img2, (85, 206, 140, 221))
# img2 = deal_image(img2, lambda x, y, z : x != 160  and y != 160 and z != 155  )

# img2 = deal_image(img2, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
# img2.save('60' + '.png', 'PNG')
# get_inf(img2)


# 翻转
# img2 = Image.open('100.png')
# img2 = img2.transpose(Image.ROTATE_90)
# img2.save('ref_1.png')

# for x in range(71, 76) :9
#     img2 = Image.open(str(x) + '.png')
#     # img2 = img2.transpose(Image.ROTATE_90)        
#     img2 = cut_image(img2, (0, 51,  376, 484))  # 消息框
     
#     get_inf(img2)
# 9
# img2 = Image.open( '72.png') 
#     # img2 = img2.transpose(Image.ROTATE_90)           dian
# get_inf(img2) 


##########################################################main
# state = 1
# myfont = my_ocr('army')
# myfont_chinese = my_ocr_chinese()
# for x in range(90, 96) :
#     img2 = Image.open(str(x) +'.png')
#     #     img2 = Image.open(str(x) + '.png')
#     img2 = img2.transpose(Image.ROTATE_90)  
#     print(get_inf(img2, myfont, myfont_chinese))


# img2 = Image.open('80.png')
# print(get_army_inf(img2, myfont))

# img2 = Image.open('ref_2.png')   
# print(get_inf(img2, myfont, myfont_chinese))



# box =  find_box_window()

# if (box[1] - box[3] != 960 or box[2] - box[4] != 540 ) :
#     print(box[1] - box[3])
#     print( box[2] - box[4])
#     print('请调整屏幕大小到960*540')
#     while True :
#         x = 1


# img = Image.open('ref_1.png')
# img = img.convert("RGB")
# pixdata = img.load()
# #获得增援按钮参考
# contribution_button = getpointarr((321, 447), pixdata)
# #获得对勾
# check_mark  = getpointarr((936, 523), pixdata)
# #获得消息框进入窗口
# message_down= getpointarr((397, 236), pixdata)
# img = Image.open('ref_1.png')
# img = img.convert("RGB")
# pixdata = img.load()
#获得消息框出来窗口
# message_down= getpointarr((397, 236), pixdata)


# cmd1=r"adb shell /system/bin/screencap -p /sdcard/96.png"       #命令1：在手机上截图3.png为图片名
# cmd2=r"adb pull /sdcard/96.png C:\Users\Administrator\Desktop\LB_LAST"                        #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
# screen=Screenshot()
# screen.screen(cmd1)
# screen.saveComputer(cmd2) 

# for x in range(60, 68) :
#     img2 = Image.open(str(x) + '.png')
#     img2 = img2.transpose(Image.ROTATE_90)
#     img2.save( str(x + 20) + '.png', 'PNG')

from findpoints import screenshort_new,isindex,troop_store


class event_list() :
    my_event_list = []
    lock = None    #申请一个线程锁
    def __init__(self):
        self.lock = threading.Lock()
        return 

    def appent_event(self, event) :
        self.lock.acquire()
        self.my_event_list.append(event)
        self.lock.release()
 

    def pop_event(self, num = 0) :
        self.lock.acquire()
        if len(self.my_event_list) == 0 :
            return
        self.my_event_list.pop(num)
        self.lock.release()

    def run_evet(self) :
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
                    self.appent_event(self.my_event_list[0][2])
                self.pop_event()


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
    timer = threading.Timer(6, lambda  :  my_evet.appent_event(coloct_event))
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
my_evet.appent_event(donte_event)
# coloct_event_test()
my_evet.run_evet()

# donte_event_()




