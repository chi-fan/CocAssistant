# In[]
import math
import json
from PIL import Image
import os

def json_get(string1) :
    with open(string1, "r", encoding='utf-8') as f:
        data2 = json.loads(f.read())    # load的传入参数为字符串类型
    return data2

def json_save(string1, my_font) :
    with open(string1, "w", encoding='utf-8') as f:
        f.write(json.dumps(my_font, indent=4))

# 计算方差
def getvariance(pointarr, pointarr2) :
    #方差计算
    total = 0
    for x in range(len(pointarr)) :
        total += (pointarr[x][0] - pointarr2[x][0]) ** 2 + (pointarr[x][1] - pointarr2[x][1]) ** 2 + (pointarr[x][2] - pointarr2[x][2]) ** 2
    stddev = math.sqrt(total/len(pointarr))
    # print(stddev)
    return stddev

# 获得目标坐标的判断像素
def getpointarr(point, pixdata) :
    pointarr = []
    for y in range(0, 11, 10) : # range(start, end, step)
        for x in range(0, 11, 10) :
            pointarr.append(pixdata[point[0] - 5 + x , point[1] - 5 + y])
    return pointarr

# 在图中找点
def findpoint(img, pointarr):
    img = img.convert("RGB")
    pixdata = img.load()
    # 遍历图片的像素点 找目标点
    for y in range(5, img.size[1] - 5):
        for x in range(5, img.size[0] - 5):
            if getvariance(getpointarr((x, y), pixdata), pointarr)  < 30:
                return  (x, y)

# 获得目标坐标的判断像素
def getpointarr_c(img, point) :

    # test for pick
    step = 10
    img_temp = cut_image(img, (point[0]-step, point[1]-step, point[0]+step, point[1]+step))
    # img_temp.show()
    # test code end

    pixdata = img.load()
    pointarr = []
    for y in range(0, 11, 10) : # range(start, end, step)
        for x in range(0, 11, 10) :
            pointarr.append(pixdata[point[0] - 5 + x , point[1] - 5 + y])
    return pointarr



screen = Screenshot()
# step 1 : save the pic about "donate":
def screenshort_new(filename):
    cmd1 = r"adb shell /system/bin/screencap -p /sdcard/" + filename    #命令1：在手机上截图3.png为图片名
    cmd2 = r"adb pull /sdcard/" + filename + r" D:\COC_support_py\COC-support"                        #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
    screen.screen(cmd1)
    screen.saveComputer(cmd2)
    img = Image.open(filename)
    img = img.transpose(Image.ROTATE_90)
    return img

# step 2: load and cut the screenshort, and save the data as json:
def get_region(type_tell):
    if type_tell == 0:# 0 for support
        init_close_pos = (870, 16)
        region_tell = (405, 20, 890, 60)
        cell_width = 68
    elif type_tell == 1:
        init_close_pos = (894, 23)
        region_tell = (46, 85, 656, 140)
        cell_width = 75
    elif type_tell == 2:
        init_close_pos = (870, 16)
        region_tell = (406, 240, 891, 280)
        cell_width = 68
    elif type_tell == 3:
        init_close_pos = (894, 23)
        region_tell = (48, 240, 570, 300)
        cell_width = 73
    else:
        print("type_tell is out of range")
        os._exit()
    return init_close_pos, region_tell, cell_width

def add_points(filename_json, points_data):
    # load the original data, and add some data
    points_data_old = json_get(filename_json)
    print("Before adding some data:  ",points_data_old)
    if len(points_data_old) == 0:
        points_data_old = points_data
    else:
        for i in range(len(points_data['he'])):
            points_data_old['he'].append(points_data['he'][i])
    print("After adding:  ",points_data_old)
    json_save(filename_json, points_data_old)
    # print(points_data)
    return True

def toclass(value, points):
    points_data = {
        'he':[
                {
                'value': value,
                'points': points,
                 },
            ]
    }
    return points_data

def get_init_points_c(filename, type_real, type_tell=0, init_pos=(296, 34)):
    """ \n
        this function is to add some points for telling the type in the next step. \n
        'filename' is the name of screenshort you collected \n
        'type_real' is a string that the type of you want to save \n
        'type_tell': 0 is for support; 1 is for troop; 2 is for support about spell; 3 is for troop about spell \n
        'init_pos' is the position that you want to save \n
        if the init_pos is None, we will ask you to type the "type"
    """
    # load some information about region and pos_close
    init_close_pos, region_tell, cell_width = get_region(type_tell)

    # load pic and transpose it
    img = Image.open(filename)
    img = img.transpose(Image.ROTATE_90)
    pixdata = img.load()

    # for support, the position of close is not clear
    if type_tell == 0 or type_tell == 2:
        pos_close = findpoint_c(img, 'close', type_tell)
    else:
        pos_close = init_close_pos

    # get the points of close the windows
    points_close = getpointarr(init_close_pos, pixdata)
    points_data = { "he" :[
                                {"value": "close",
                                "points": points_close,
                                },
                        ]
    }

    # if the type_real is None, we will ask you for all pic
    if type_real != None:
        # get the points you want to save
        points_temp = getpointarr((init_close_pos[0] - init_pos[0], init_close_pos[1] + init_pos[1]), pixdata)
        # add the list
        points_data['he'].append( {
                            "value": type_real,
                            "points": points_temp,
                            }
        )
    else:
        # ask you for all pic
        for i in range( math.floor((region_tell[2]-region_tell[0])/cell_width) ):
            img_temp = cut_image(img, (region_tell[0] + i*cell_width,
                                       pos_close[1] + region_tell[1],
                                       region_tell[0] + (i+1)*cell_width,
                                       pos_close[1] + region_tell[3])
                                )
            img_temp.show()
            print("this is ", i+1)
            type_real = input("Please tell me who it is ! :")
            # if you type wihte space, we will ignore the pic
            if type_real != ' ':
                init_pos = (region_tell[0]+(2*i+1)/2*cell_width, pos_close[1] + (region_tell[1]+region_tell[3])/2)
                points_temp = getpointarr(init_pos, pixdata)
                # add the list
                points_data['he'].append( {
                                    "value": type_real,
                                    "points": points_temp,
                                    }
                )

    return points_data

# step 3: open the json and find the positon
# tell the type of troop
def findpoint_c(img, type_need, type_tell=0, isCut=1):
    """ 'img' is the type of image from pillow \n
        'type_need': "balloon", "dragon", "pikka", "wizard" \n
        'type_tell': 0 is for support; 1 is for troop
    """
    # load some informations
    init_close_pos, region_tell, cell_width = get_region(type_tell)

    # load data to tell the type
    filename_json = "test_json.json"
    pix_get = json_get(filename_json)
    # print(pix_get)


    # for speed the code, we will search the type
    index = []
    for i in range(len(pix_get['he'])):
        if pix_get['he'][i]['value'] == type_need:
            print("index is ", i)
            index.append(i)

    # default is we will cut the imge
    if isCut == 1:
        img_close = cut_image(img, (init_close_pos[0] - 10, 0, init_close_pos[0]  + 15, 250) )
        # img_close.show()
        pos_close = findpoint(img_close, pix_get['he'][0]['points'])
    else:
        pos_close = (0, init_close_pos[1])

    if pos_close != None:
        pos_close = (pos_close[0] + (init_close_pos[0]-10), pos_close[1])
        print("the pos of 'close' is ", pos_close)
        if index == 0:
            print("you select the 'close' botton")
            return pos_close
        else:
            if isCut == 1:
                img_support = cut_image(img, (region_tell[0], pos_close[1] + region_tell[1],
                                            region_tell[2], pos_close[1] + region_tell[3])
                                            )
            else:
                img_support = img
            # img_support.show()

            # if we have more data for telling the type
            if len(index) > 1:
                for i in index:
                    pos_data= findpoint(img_support, pix_get['he'][i]['points'])
                    if pos_data != None:
                        break
            else:
                pos_data= findpoint(img_support, pix_get['he'][index[0]]['points'])

            # if we find the points, we return them, if not, we will print and return None
            if pos_data != None:
                pos_data = (pos_data[0] + region_tell[0], pos_data[1] + (pos_close[1]+region_tell[1]))
                print("the pos you want is ", pos_data)
                return pos_data
            else:
                print("we can't find the type!")
                return None
    else:
        print("Maybe you have not open the donate or train troop!")
        return None

army_type_stored = ['pekka', 'balloon', 'wizard', 'dragon', 'archer', 'barbarian']
spell_type_stored = ['haste', 'healing', 'rage']

def troop_store(img, type_tell=1):
    """
        img is image from PIL \n
        type_tell is a flag \n
        this function is for tell the army you have stored
    """
    init_close_pos, region_tell, cell_width = get_region(type_tell)
    pos_close = init_close_pos
    if type_tell == 0 or type_tell == 2:
        pos_close = findpoint_c(img, 'close', type_tell)
    type_now = []
    type_index = []
    for i in range( math.floor((region_tell[2]-region_tell[0])/cell_width)):
        img_temp = cut_image(img, (region_tell[0] + i*cell_width,
                                    pos_close[1] + region_tell[1],
                                    region_tell[0] + (i+1)*cell_width,
                                    pos_close[1] + region_tell[3])
                            )
        # img_temp.show()
        if (type_tell == 1 or type_tell == 0 ):
            for index in army_type_stored:
                pos_temp = findpoint_c(img_temp, index, type_tell, isCut=0)
                if pos_temp != None:
                    type_now.append(index)
                    type_index.append(i)
        else:
            for index in spell_type_stored:
                pos_temp = findpoint_c(img_temp, index, type_tell, isCut=0)
                if pos_temp != None:
                    type_now.append(index)
                    type_index.append(i)
    return type_now, type_index

def isindex():
    filename = 'temp_index.png'
    screenshort_new(filename)
    img = Image.open(filename)
    img = img.transpose(Image.ROTATE_90)
    img_index = cut_image(img, (20, 366, 60, 406))
    filename_json = 'test_json.json'
    pix_get = json_get(filename_json)
    for i in range(len(pix_get['he'])):
        if pix_get['he'][i]['value'] == 'index':
            # print("index is ", i)
            break
    pos_index = findpoint(img_index, pix_get['he'][i]['points'])
    if pos_index == None:
        return False
    else:
        return True
# test code


# filename =""
# img = Image.open(filename)
# img = img.transpose(Image.ROTATE_90)

# print( troop_store(img, 1))


