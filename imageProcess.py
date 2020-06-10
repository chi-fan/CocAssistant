import re

from PIL import Image

cut_width  = 680
cut_heigh  = 965

def processImage(image, logic_expression) :
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


def cutImage(image, tuple):
    width, height = image.size
    img = Image.new('RGB', (width, height), (0, 0, 0))
    img.paste(image, (0, 0))

    img = img.crop(tuple)
    return img

def locateDialogBoxList(img, number):
    img = img.convert("RGB")
    pixdata = img.load()
    box_list = []
    y = 0
    x = number
    while y < img.size[1] :
        if pixdata [x, y] == (255, 255, 255) :
            box = (x , y)
            box_list.append(box)
            y += 100
        else :
            y += 1
    return box_list

def get_army(image):
    new_image = processImage(image, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 and abs(x - y) < 3 and abs(x - z) < 3 and abs(y - z) < 3)
    new_image.save("army.jpg")
    return

def translateStringToChinese(pendingString) :
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

    temp =  re.split(r'(\n)', pendingString)
    Request['str'] = temp[0]

    # 中间会用空的数据块  跳过
    for i in [2, 4, 6, 8] :
        if i >= len(temp) :
            break
        if(temp[i] == '') :
            temp[2] = temp[i + 2]

    if len(temp) > 2 :
        temp[2] = temp[2].replace('O', '0')
        temp[2] = temp[2].replace('o', '0')

        print(temp)
        temp_number = re.findall(r'\d+', temp[2])

        print(temp_number)
        Request['army']['fill_in'] = temp_number[0]
        Request['army']['max'] = temp_number[1]
        if len(temp_number) > 3 :
            Request['spells']['fill_in'] = temp_number[2]
            Request['spells']['max'] = temp_number[3]
        if  len(temp_number) > 5 :
            Request['device']['fill_in'] = temp_number[4]
            Request['device']['max'] = temp_number[5]
    return Request

def getImageRequestList(pendingImage) :
    # print(pendingImage.size[0] , pendingImage.size[1])
    pendingImage =  pendingImage.resize((1920, 1080))   #这里统一格式为1920 * 1080
    pendingImage.save('cut_in.png', 'PNG')
    pendingImage = cutImage(pendingImage, (0, 100, cut_width, cut_heigh))
    pendingImage.save('cut_out.png', 'PNG')
    #获得按钮
    new_image = processImage(pendingImage, lambda x, y, z : not (y > 200 and z < 100))
    # new_image.save('cut_out2.png', 'PNG')
    buttonPostionList = locateDialogBoxList(new_image, 600)
    # for index in buttonPostionList :
    #     print(index)

    #获得横线
    new_image = processImage(pendingImage, lambda x, y, z : not (y < 50 and z < 50))
    # new_image.save('cut_out3.png', 'PNG')
    hor_list = locateDialogBoxList(new_image, 500)
    # for index in hor_list:
    #     print(index)

    # 获得按钮所在的单元
    rangList = []
    for index in buttonPostionList :
        i = 0
        while i < len(hor_list) :
            if index[1] < hor_list[i][1] :
                rangList.append(i)
                break
            else :
                i += 1
                if  i == len(hor_list) :
                    rangList.append(i)

    # 剪裁按钮所在的位置
    requestList = []

    m = 0
    for index in rangList :
        if index == 0 :
            image =  cutImage(img, (0 , 2, cut_width, hor_list[index][1]))
        elif index == len(hor_list) :
            image =  cutImage(img, (0 , hor_list[index - 1][1] + 84, cut_width, cut_heigh))
        else :
            image =  cutImage(img, (0 , hor_list[index - 1][1] + 84, cut_width, hor_list[index][1]))

        new_image = processImage(image, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 and abs(x - y) < 3 and abs(x - z) < 3 and abs(y - z) < 3)
        new_image.save(str(index) + '.png', 'PNG')
        pendingString = pytesseract.image_to_string(new_image, lang='chi_sim')
        # print(code)
        Request = translateStringToChinese(pendingString)
        Request['position'] = buttonPostionList[m]
        m += 1
        requestList.append(Request)
    return requestList

