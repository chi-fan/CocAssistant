import re
from PIL import Image

cut_width  = 680
cut_heigh  = 965

def pasteImage(image) :
    width, height = image.size()
    newImage = Image.new('RGB', (width, height), (0, 0, 0))
    newImage.paste(image, (0, 0))
    return newImage

def processImage(image, logicExpression) :
    ''' 将图片按照指定算法转化为黑白图片 '''
    newImage = pasteImage(image)

    newImage = newImage.convert("RGB")
    pixdata = newImage.load()
    for y in range(newImage.size[1]):
        for x in range(newImage.size[0]):
            if logicExpression(pixdata[x, y][0], pixdata[x, y][1], pixdata[x, y][2]):
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)
    return newImage

def locateDialogBoxList(image, number):
    image = image.convert("RGB")
    pixdata = image.load()
    box_list = []
    y = 0
    x = number
    while y < image.size[1] :
        if pixdata [x, y] == (255, 255, 255) :
            box = (x , y)
            box_list.append(box)
            y += 100
        else :
            y += 1
    return box_list

def getArmy(image):
    newImage = processImage(image, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 and abs(x - y) < 3 and abs(x - z) < 3 and abs(y - z) < 3)
    newImage.save("army.jpg")
    return

def translateStringToChinese(pendingString) :
    Request = {}

    realString =  re.split(r'(\n)', pendingString)
    Request['str'] = realString[0]

    # 中间会用空的数据块  跳过
    for i in [2, 4, 6, 8] :
        if i >= len(realString) :
            break
        if(realString[i] == '') :
            realString[2] = realString[i + 2]

    if len(realString) > 2 :
        realString[2] = realString[2].replace('O', '0')
        realString[2] = realString[2].replace('o', '0')

        parameter = re.findall(r'\d+', realString[2])

        Request['army']['fill_in'] = parameter[0]
        Request['army']['max'] = parameter[1]
        if len(parameter) > 3 :
            Request['spells']['fill_in'] = parameter[2]
            Request['spells']['max'] = parameter[3]
        else :
            Request['spells']['fill_in'] = 0
            Request['spells']['max'] = 0

        if  len(parameter) > 5 :
            Request['device']['fill_in'] = parameter[4]
            Request['device']['max'] = parameter[5]
        else :
            Request['device']['fill_in'] = 0
            Request['device']['max'] = 0
    return Request

def getImageRequestList(pendingImage) :
    pendingImage.save('cutIn.png', 'PNG')
    pendingImage = pendingImage.crop(pendingImage, (0, 100, cut_width, cut_heigh))
    pendingImage.save('cutOut.png', 'PNG')
    #获得按钮
    newImage = processImage(pendingImage, lambda x, y, z : not (y > 200 and z < 100))
    # newImage.save('cut_out2.png', 'PNG')
    buttonPostionList = locateDialogBoxList(newImage, 600)
    # for index in buttonPostionList :
    #     print(index)

    #获得横线
    newImage = processImage(pendingImage, lambda x, y, z : not (y < 50 and z < 50))
    # newImage.save('cut_out3.png', 'PNG')
    hor_list = locateDialogBoxList(newImage, 500)
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
            image = image.crop(image, (0 , 2, cut_width, hor_list[index][1]))
        elif index == len(hor_list) :
            image = image.crop(image, (0 , hor_list[index - 1][1] + 84, cut_width, cut_heigh))
        else :
            image = image.crop(image, (0 , hor_list[index - 1][1] + 84, cut_width, hor_list[index][1]))

        newImage = processImage(image, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 and abs(x - y) < 3 and abs(x - z) < 3 and abs(y - z) < 3)
        newImage.save(str(index) + '.png', 'PNG')
        pendingString = pytesseract.image_to_string(newImage, lang='chi_sim')
        # print(code)
        Request = translateStringToChinese(pendingString)
        Request['position'] = buttonPostionList[m]
        m += 1
        requestList.append(Request)
    return requestList

