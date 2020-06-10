from PIL import Image
from myfont import *
import re
import pytesseract
from myfont_chinese import *

cut_width  = 374
cut_heigh  = 478
ref_width  =  374 
ref_heigh  = 112

# 处理图像
def deal_image(image, logic_expression) :
    # 创建一个新的图片对象
    width, height = image.size
    img = Image.new('RGB', (width, height), (0, 0, 0))
    img.paste(image, (0, 0))

    img = img.convert("RGB")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            # print(pixdata[x,y])
            if logic_expression(pixdata[x, y][0], pixdata[x, y][1], pixdata[x, y][2]): 
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)
    return img


# 裁剪图片
def cut_image(image, tuple):
     # 创建一个新的图片对象
    width, height = image.size
    # image.save('cut2.png', 'PNG')
    img = Image.new('RGB', (width, height), (0, 0, 0))
    img.paste(image, (0, 0))
    # img.save('cut.png', 'PNG')
    img = img.crop(tuple)
    return img




# 获得按钮所在边框地址
def get_box(img, number):
    img = img.convert("RGB")
    pixdata = img.load()
    box_list = []
    y = 0
    x = number
    while y < img.size[1] :
        if pixdata [x, y] == (255, 255, 255) :
            box = (x , y)
            box_list.append(box)
            y += 50
        else :
            y += 1
    return box_list


def get_ref_img(img, num) :
    # 创建一个新的图片对象
    width, height = img.size
    img2 = Image.new('RGB', (ref_width, ref_heigh), (0, 0, 0))
    if num == 0 :   #顶
        img2.paste(img, (0, ref_heigh - height))
    else :          #底
        img2.paste(img, (0, 0))
    return img2

def deal_str(deal_code) :
    Request = {
     'str':None,      
     'army':{
      'max':0,
     'fill_in':0,
     },
     'spells':{
      'max':0,
      'fill_in':0,
     },
     'device':{
     'max':0,
     'fill_in':0,
     },
     'position':(0, 0)
    }
     
    temp_number = re.findall(r'\d+', deal_code)
        
    Request['army']['fill_in'] = temp_number[0]
    Request['army']['max'] = temp_number[1]
    if len(temp_number) > 3 :
        Request['spells']['fill_in'] = temp_number[2]
        Request['spells']['max'] = temp_number[3]  
    if  len(temp_number) > 5 :
        Request['device']['fill_in'] = temp_number[4]
        Request['device']['max'] = temp_number[5]          
    return Request


def get_inf(img, myfont, myfont_chinese) :
    # printprint(img.size[0] , img.size[1])
    img = cut_image(img, (0, 51, cut_width, cut_heigh))
    # img.save('cut_out45.png', 'PNG')
    #获得按钮
    new_image = deal_image(img, lambda x, y, z : not (y > 200 and z < 100))
    # new_image.save('cut_out2.png', 'PNG')
    button_list = get_box(new_image, 270)
    # for index in button_list :
    #     print(index)

    #获得横线
    new_image = deal_image(img, lambda x, y, z : not (y < 50 and z < 50))
    # new_image.save('cut_out3.png', 'PNG')
    hor_list = get_box(new_image, 250)
    # for index in hor_list:
    #     print(index)

    # 获得按钮所在的单元
    rang_list = [] 
    for index in button_list :
        i = 0
        while i < len(hor_list) :
            if index[1] < hor_list[i][1] :
                rang_list.append(i)
                break
            else :
                i += 1
                if  i == len(hor_list) :
                    rang_list.append(i)

    # 剪裁按钮所在的位置
    request_list = []

    m = 0
    for index in rang_list :   # 这里在裁剪时要定义标准长宽  374 112
        if index == 0 :
            image =  cut_image(img, (0 , 2, cut_width, hor_list[index][1]))
            image = get_ref_img(image, 0)
        elif index == len(hor_list):
            image =  cut_image(img, (0 , hor_list[index - 1][1] + 3, cut_width, cut_heigh))
            image = get_ref_img(image, 1)
        else :
            image =  cut_image(img, (0 , hor_list[index - 1][1] + 3, cut_width, hor_list[index][1]))
        # image.save('save_2.png', 'PNG')

        #捐兵数字添加
        new_image = cut_image(image, (60, 66, 247, 86))   # 裁剪出要的区域
        new_image = deal_image(new_image, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
        Request = deal_str(myfont.get_string(new_image))
        #捐兵文字添加
        new_image = cut_image(image, (40, 40, 247, 62))   # 裁剪出要的区域
        new_image = deal_image(new_image, lambda x, y, z : x > 100  and y > 100 and z > 100 )
        code = myfont_chinese.get_string(new_image)
        Request["str"] = code
        Request['position'] = (button_list[m][0], button_list[m][1] + 68)
        print(button_list[m][0], button_list[m][1] + 68)
        m += 1
        print(Request)
        request_list.append(Request)
    return request_list


def cut_blob(image) :
    width, height = image.size
    img = Image.new('RGB', (width, height), (0, 0, 0))
    img.paste(image, (0, 0))
    img = img.convert("RGB")
    pixdata = img.load()   
    
    for x in range(img.size[0]) :
        if pixdata[x, 0][0] == 0 :
            for y in range(img.size[1]) :
                if pixdata[x, y][0] == 0 :
                    pixdata[x, y] = (255, 255, 255)
                else :
                    break
    for x in range(img.size[0]) :
        if pixdata[x, img.size[1] - 1][0] == 0 :
            for y in range(img.size[1] - 1, -1, -1) :
                if pixdata[x, y][0] == 0 :
                    pixdata[x, y] = (255, 255, 255)
                else :
                    break
    return img


def get_army_inf(img, myfont) : 
    img2 = cut_image(img, (97, 69, 170, 90))
    img2 = deal_image(img2, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
    img2 = cut_blob(img2)
    code = myfont.get_string(img2)
    new_image = cut_image(img, (48, 97, 638, 115))
    new_image = deal_image(new_image, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
    deal_code = myfont.get_string(new_image)
    army_list = re.findall(r'\d+', deal_code)

    img2 = cut_image(img, (97, 213, 170, 237))
    img2 = deal_image(img2, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
    img2 = cut_blob(img2)
    spells = myfont.get_string(img2)
    army_all = {
        "troops" : code,
        "army_list" : army_list,
        "spells" : spells
    }
    return army_all


def get_army_inf2(img, myfont) : 
    img2 = cut_image(img, (72, 60, 139, 76))
    img2 = deal_image(img2, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
    deal_code = myfont.get_string(img2)
    return deal_code

# def  findpoint(img, pointarr):
#     img = img.convert("RGB")
#     pixdata = img.load()
#     for point in pointarr :
#         print(pixdata[point[0], point[1]])

#     pointarr = get_arr(pointarr)
#     if pointarr == None:  # 空数组直接返回
#         return None


#     mypoint = None
#     # 遍历图片的像素点 找目标点
#     for y in range(img.size[1]):
#         for x in range(img.size[0]):
#             if pixdata[x, y] == (pointarr[0][2], pointarr[0][3], pointarr[0][4]):   
#                 for point in pointarr:
#                     if x + point[0] >= img.size[0] or y + point[1] >= img.size[1] :
#                       break
#                     if pixdata[x + point[0], y + point[1]] != (point[2], point[3], point[4]):
#                       break
#                     if point == pointarr[-1]:  # 到达最后一个点还符合 找到目标点
#                       mypoint = (x, y)
#                 if mypoint != None:  # 找到点， 跳出x轴循环
#                     break
        
#         if mypoint != None: # 找到点， 跳出y轴循环
#             break

#     return mypoint




# def  findpoint(img, point, img_ref, point_ref):

# #方差计算
# total = 0
# for value in data:
#     total += (value - average) ** 2
 
# stddev = math.sqrt(total/len(data))
# print(stddev)



# img = Image.open('12.png')
# temp_number = get_army_num(img)
# print(temp_number)

# get the handle of windows of COC and the positon of windows
# box = find_box_window()

# # get the screenshort
# img = window_capture(box, 'TEST_png')
# img.save("1.png", "PNG")

# img = cut_image(img, (58, 50, 118, 63))
# img = deal_image(img, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 )
# # img.save('387_1.png', 'PNG')
# code = pytesseract.image_to_string(img, lang='coc')
# print(code)


# cmd1=r"adb shell /system/bin/screencap -p /sdcard/2.png"       #命令1：在手机上截图3.png为图片名
# cmd2=r"adb pull /sdcard/2.png C:\Users\Administrator\Desktop\LB_LAST"                        #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
# screen=Screenshot()
# screen.screen(cmd1)
# screen.saveComputer(cmd2)


# img = Image.open('13.png')
# img = img.convert("RGB")
# pixdata = img.load()
# point = (902, 480)
# pointarr = getpointarr(point, pixdata) 


# img2 = Image.open('2.png')
# img2 = img2.transpose(Image.ROTATE_90)
# print(ifpoint(img2, point, pointarr)) 


# box =  find_box_window()
# print(box)
# print(box[1] - box[3])
# print(box[2] - box[4])
# Click(box[1] +point[0], box[2] +point[1])



# img2 = Image.open('3.png')
# img2 = img2.transpose(Image.ROTATE_90)
# img2.save('19.png')

# for x in range(1, 9) :
#     img2 = Image.open('3' + str(x) + '.png')
#     # img2 = img2.transpose(Image.ROTATE_90)
#     # img2.save('3'+ str(x) + '.png')
#     img2 = cut_image(img2, (72, 60, 139, 76))
#     img2 = deal_image(img2, lambda x, y, z : x != 160  and y >= 160 and z >= 155  )
#     img2.save('5'+ str(x) + '.png')
#     get_army_num(img2)

# img2 = Image.open('58.png')
# # img2 = cut_image(img2, (72, 60, 139, 76))
# # img2 = deal_image(img2, lambda x, y, z : x != 160  and y != 160 and z != 155  )
# img2.save('58' + '.tif', 'TIFF')
# get_army_num(img2)

def getscreen_army_number() :
    cmd1=r"adb shell /system/bin/screencap -p /sdcard/2.png"       #命令1：在手机上截图3.png为图片名
    cmd2=r"adb pull /sdcard/2.png C:\Users\Administrator\Desktop\LB_LAST"                        #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
    screen=Screenshot()

    box =  find_box_window()
    print(box[3] - box[1])
    print(box[4] - box[2])
    for count in range(10, 50) :
        Click(box[1] +108, box[2] + 408)
        time.sleep(1)
        screen.screen(cmd1)
        screen.saveComputer(cmd2)
        img2 = Image.open('2.png')
        img2 = img2.transpose(Image.ROTATE_90)
        img2 = cut_image(img2, (72, 60, 139, 76))
        # img2 = deal_image(img2, lambda x, y, z : x != 160  and y >= 160 and z >= 155  )
        img2.save('./font/coc.exp1' + str(count) + '.tif', 'TIFF')




# getscreen_army_number()

# for count in range(10, 50) :
#         img2 = Image.open('./font/coc.exp1' + str(count) + '.tif')
#         img2 = deal_image(img2, lambda x, y, z : x >= 220  and y >= 220 and z >= 220  )
#         img2.save('./font/cl2.coc.exp1' + str(count) + '.tif')
# Paste('he')
# cmd1=r"adb shell /system/bin/screencap -p /sdcard/101.png"       #命令1：在手机上截图3.png为图片名
# cmd2=r"adb pull /sdcard/101.png C:\Users\Administrator\Desktop\LB_LAST"                        #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
# screen=Screenshot()
# screen.screen(cmd1)
# screen.saveComputer(cmd2)