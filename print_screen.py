import win32api,win32gui,win32con, win32ui
import win32clipboard as wc
import time
import math
from Request_deal import request_deal
from PIL import Image, ImageGrab
from findpoints import findpoint_c, screenshort_new

# In[2]:


# Set the mouse 
def Click(position_x, position_y):
    win32api.SetCursorPos([position_x,position_y])
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, position_x, position_y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, position_x, position_y,0,0) 


# In[3]:


# set the keyboard
def KeyBoard(VK):
    win32api.keybd_event(VK,0,0,0)
    time.sleep(0.2)
    win32api.keybd_event(VK,0,2,0)


# In[4]:


def KeyStr(str):
    str = str.upper()
    for num in str:
        KeyBoard(ord(num))


# In[5]:


# Set the paste
def Paste(data_w):
    wc.OpenClipboard()
    wc.SetClipboardText(data_w,wc.CF_UNICODETEXT)
    #data_r = wc.GetClipboardData(wc.CF_UNICODETEXT)
    wc.CloseClipboard()
    win32api.keybd_event(win32con.VK_CONTROL,0,0,0)
    win32api.keybd_event(ord('V'),0,0,0)
    win32api.keybd_event(win32con.VK_CONTROL,0,2,0)# 2 is equal to the KEYEVENTF_KEYUP
    win32api.keybd_event(ord('V'),0,2,0)


# In[6]:


def findWindow( wClass, wName ):
    time_home = win32api.GetTickCount() # unit is ms
    while True:
        hWnd = win32gui.FindWindow( wClass, wName) 
        if hWnd != 0:
            break
        time_end = win32api.GetTickCount()
        time_open = time_end - time_home
        # print(time_open)
        if time_open > 10000:
            break
    print(hex(hWnd))
    return hWnd


# In[7]:


def findWindowEx( hWnd, chiHand, cClass, cName ):
    time_home = win32api.GetTickCount() # unit is ms
    while True:
        hWnd_c = win32gui.FindWindowEx( hWnd, chiHand, cClass, cName) 
        if hWnd_c != 0:
            break
        time_end = win32api.GetTickCount()
        time_open = time_end - time_home
        # print(time_open)
        if time_open > 10000:
            break
    print(hex(hWnd_c))
    return hWnd_c

# In[ ]:
def window_capture0(box, filename):
    # name some variables
    hWnd = box[0]
    w = box[3] - box[1]
    h = box[4] - box[2]

    # c_hWnd3 = findWindowEx(hWnd,0,'Qt5QWindowIcon','centralWidgetWindow')
    c_hWnd = findWindowEx(hWnd,0,'Qt5QWindowIcon','ScreenBoardClassWindow')
    c_hWnd2 = findWindowEx(c_hWnd,0,'subWin','sub')

    hwnd = c_hWnd2  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    
    # release some handle
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    
def window_capture1(box, filename, num_clik):
    # name some variables
    hWnd = box[0]
    left = box[1]
    top = box[2]
    w = box[3] - box[1]
    h = box[4] - box[2]

    # c_hWnd3 = findWindowEx(hWnd,0,'Qt5QWindowIcon','centralWidgetWindow')
    c_hWnd = findWindowEx(hWnd,0,'Qt5QWindowIcon','ScreenBoardClassWindow')
    c_hWnd2 = findWindowEx(c_hWnd,0,'subWin','sub')

    # open the messages
    Click(round(left+0.05*w), round(top+0.4*h))
    time.sleep(2)

    for index in range(int(num_clik)):    
        # click the “!”
        Click(round(left+0.37*w), round(top+0.14*h))
        time.sleep(0.3)

    time.sleep(1)
    hwnd = c_hWnd2  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    
    # close the messages
    Click(round(left+0.4*w), round(top+0.4*h))
    time.sleep(1)
    print('screenshort: message closed')

    # release some handle
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

def window_capture(box, filename, flag_doubleFingers=0):
    # name some variables
    left = box[1]
    top = box[2]
    right = box[3]
    bottom = box[4]

    pos = get_window_pos('nox')
    if flag_doubleFingers == 1:
        pos2 = get_window_pos('通过键盘调节GPS方位和移动速度')
        # 截图
        img_ready = ImageGrab.grab((left, top, right + (pos[0][2]-pos[0][0]) + (pos2[0][2]-pos2[0][0]), bottom))
    else:
        img_ready = ImageGrab.grab((left, top, right + (pos[0][2]-pos[0][0]), bottom))

    # 展示
    # img_ready.show()
    img_ready.save(filename + '.png', 'PNG')

    return img_ready

def find_box_window():
    hWnd = findWindow(None, '夜神模拟器') # get the handle
    c_hWnd = findWindowEx(hWnd,0,'Qt5QWindowIcon','ScreenBoardClassWindow')
    c_hWnd2 = findWindowEx(c_hWnd,0,'subWin','sub')

    win32gui.ShowWindow(hWnd,win32con.SW_SHOWDEFAULT)
    KeyBoard(win32con.VK_LEFT)
    win32gui.SetForegroundWindow(hWnd)
    (left, top, right, bottom) = win32gui.GetWindowRect(c_hWnd2) # get the box of windows
    box  = []
    box.append(hWnd)
    box.append(left)
    box.append(top)
    box.append(right)
    box.append(bottom)
    return box

def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
    # 返回坐标值和handle
    
        return win32gui.GetWindowRect(handle), handle


num_housing_space = {
            'dragon':20,
            'balloon':5,
            'pekka':25,
            'wizard':4,
            'speed_increase':1
            }
pos_index = {
            'dragon':(4,0),
            'balloon':(2,1),
            'pekka':(4,1),
            'wizard':(3,0),
            'healing':(0,1),
            'haste':(4,0),
            'rage':(1,0),
}
def init_pos_army():
    """
        resolution: 540*960
    """
    cell_width = 96
    cell_height = 97
    pos_barbarian = (97, 326)
    positions ={}
    kys = list(pos_index.keys())
    # print(kys)
    for i in range(len(pos_index)):
        index = kys[i]
        pos_temp = (pos_barbarian[0] + (pos_index[index][0]*cell_width), 
                    pos_barbarian[1] + (pos_index[index][1]*cell_height),
        )
        positions[index] =pos_temp

    pos_army     = (40, 390)
    pos_train_troops = (35, 270)
    pos_brew_spells  = (35, 445)
    pos_close_army = (894, 23)

    positions['army'] = pos_army
    positions['train_troops'] = pos_train_troops
    positions['Brew_spells'] = pos_brew_spells
    positions['close_army'] = pos_close_army

    return positions
      
# train troops and support 
def build_all(box, request_list):
    """
        box is [handle, left, top, bottom] \n
        request_list is the array about dic \n
        ******      Attention
        before running the function, you should be index.
        After build_all, function will close the windows about train troop
    """
    # get the box of windows
    left = box[1]
    top = box[2]
    
    positions = init_pos_army()

    # get the information about request
    request     = request_deal(request_list[0]['str'])
    num_army    = int(request_list[0]['army']['max'])
    num_spells  = int(request_list[0]['spells']['max'])
    num_devices = int(request_list[0]['device']['max'])
    num_army_fill_in = int(request_list[0]['army']['fill_in'])
    num_spells_fill_in = int(request_list[0]['spells']['fill_in'])
    num_device_fill_in = int(request_list[0]['device']['fill_in'])

    # open army
    time.sleep(0.2)
    Click(left + positions['army'][0], top + positions['army'][1])
    
    # select dragon
    if request[0] != None:
        # open train troops
        time.sleep(0.2)
        Click(left + positions['train_troops'][0], top + positions['train_troops'][1])
        if ( num_army - num_army_fill_in ) >= num_housing_space[request[0]]:
            for index in range( math.floor( ( num_army - num_army_fill_in ) / num_housing_space[request[0]] ) ):
                time.sleep(0.2)
                Click(left + positions[request[0]][0], top + positions[request[0]][1])
    
    # select speed increase
    if request[1] != None:
        # open brew spells
        time.sleep(0.2)
        Click(left + positions['Brew_spells'][0], top + positions['Brew_spells'][1])
        if ( num_spells - num_spells_fill_in ) >= num_housing_space[request[1]]:
            for index in range( math.floor( ( num_spells - num_spells_fill_in ) / num_housing_space[request[1]] ) ):
                time.sleep(0.2)
                Click(left + positions[request[1]][0], top + positions[request[1]][1])

    # select device
    # if request[2] != None:
        # open brew spells
        ##
            
    # close the army
    time.sleep(0.2)
    Click(left + positions['close_army'][0], top + positions['close_army'][1])
    print('close the army')

    return True
    
def contribute( box, request_list):
    """
        box is [handle, left, top, right, bottom]\n
        request_list is the array about dic \n
        ******      Attention
        before running the function, you have opend the message
        After contribute, nothing will happen for windows
    """
    # get the box of windows
    left = box[1]
    top = box[2]

    # get the information about request
    request     = request_deal(request_list[0]['str'])
    num_army    = int(request_list[0]['army']['max'])
    num_spells  = int(request_list[0]['spells']['max'])
    num_devices = int(request_list[0]['device']['max'])
    position    = request_list[0]['position']
    num_army_fill_in = int(request_list[0]['army']['fill_in'])
    num_spells_fill_in = int(request_list[0]['spells']['fill_in'])
    num_device_fill_in = int(request_list[0]['device']['fill_in'])

    # click the donate
    Click( left + position[0], top + position[1])
    time.sleep(1)

    screenshort_new("temp_support.png")
    img = Image.open("temp_support.png")
    img = img.transpose(Image.ROTATE_90)
    pos_army_temp = findpoint_c(img, request[0])

    # select army
    if request[0] != None:
        if ( num_army - num_army_fill_in ) >= num_housing_space[request[0]]:
            for index in range( math.floor( ( num_army - num_army_fill_in ) / num_housing_space[request[0]] ) ):
                time.sleep(0.2)
                Click(left + pos_army_temp[0], top + pos_army_temp[1])
    
    # select spells
    if request[1] != None:
        if ( num_spells - num_spells_fill_in ) >= num_housing_space[request[1]]:
            for index in range( math.floor( ( num_spells - num_spells_fill_in ) / num_housing_space[request[1]] ) ):
                time.sleep(0.2)
                Click(left + pos_army_temp[0], top + pos_army_temp[1])

    # select device
    if request[2] != None:
        if ( num_devices - num_device_fill_in ) >= num_housing_space[request[2]]:
            for index in range( math.floor( ( num_devices - num_device_fill_in ) / num_housing_space[request[2]] ) ):
                time.sleep(0.2)
                Click(left + pos_army_temp[0], top + pos_army_temp[1])

    return True
    
# test code for build
# box = find_box_window()
# request_list = [
#                 {
#                 'str':'法 师',
#                 'army':{
#                         'max': 25,
#                         'fill_in':21,
#                         },
#                 'spells':{
#                         'max': 2,
#                         'fill_in':0,  
#                         },
#                 'device':{
#                         'max': 2,
#                         'fill_in':2,  
#                         },
#                 'position':(0,0)
#                 },
# ]
# print( request_list[0]['army']['max'] )
# build_all_c(box, request_list)
# contribute_c(box, request_list )

# img = Image.open("temp_support.png")
# img = img.transpose(Image.ROTATE_90)
# pos_army_temp = findpoint_c(img, 'dragon')
# print( pos_army_temp )
