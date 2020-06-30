import print_screen as PS
import re
from findpoints import screenshort_new,isindex,troop_store
import time
import eventQueue as EQ

requestInit = None

def donte_event_() :
    if not isindex() :
        print("error: this is not index!")
    print(box)
    PS.Click(box[1] + 12, box[2] + 240)
    time.sleep(0.5)
    img = screenshort_new("screenshort.png")
    requestInit = get_inf(img, myfont, myfont_chinese)
    PS.contribute(box, requestInit)
    PS.Click(box[0] + 393, box[1] + 240)
    print("donte_event_")
    return

def build_event_() :
    if not isindex() :
        #  error deal
        print("error: this is not index!")
    PS.Click(box[1] + 37, box[2] + 400)
    time.sleep(0.5)
    img = screenshort_new("screenshort.png")
    army_list = get_army_inf(img, myfont)
    if army_list == None  :
        return
    print(army_list)

    #19个mm ，15 个气球 9个法师 3条龙 2个皮卡
    print(requestInit)
    build_all(box, requestInit)


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

if __name__ == "__main__":
    print("____________________________________________________________________\n")
    print("\t\t\t吃饭和island的coc辅助工具")
    print("____________________________________________________________________\n")
    build_event = ["build", build_event_, None]
    donte_event = ["donte", donte_event_, build_event]
    build_event[2] = donte_event
    box =  PS.find_box_window()
    print(box)
    coloct_event = ["coloct",  coloct_event_, None]

    my_evet = EQ.eventQueue()
    my_evet.appendEvent(donte_event)
    # coloct_event_test()
    my_evet.runEvent()

    # donte_event_()




