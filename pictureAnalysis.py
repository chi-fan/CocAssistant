import re
from PIL import Image
import myOrc
import os

class pictureAnalysis() :
    m_myOrc = None
    dialogWidth = 745
    dialogheigth = 965

    def __init__(self) :
        self.m_myOrc = myOrc.myOrc()

    def translateStringToRequest(self, pendingString) :
        ''' 将特殊字符串转换为部落冲突捐赠数据字典 '''
        Request = {
            'str' : None,
            'army' : {
                'fill_in' : 0,
                'max'     : 0,
            },
            'spells' : {
                'fill_in' : 0,
                'max'     : 0,
            },
            'device' : {
                'fill_in' : 0,
                'max'     : 0,
            },
            'position' : None
        }
        realString =  re.split(r'(\n)', pendingString)
        # 去点多余的点
        while (realString[0] == "") :
            realString.pop(0)
            realString.pop(0)
        Request['str'] = realString[0]

        if len(realString) > 2 :
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
        Request['position'] = None
        return Request

    def getImageRequestList(self, imageName) :
        ''' 返回图片中所有捐赠请求信息 '''
        pendingImage = Image.open(imageName)
        pendingImage = pendingImage.transpose(Image.ROTATE_90)
        pendingImage = pendingImage.crop((0, 100, self.dialogWidth, self.dialogheigth))
        # pendingImage.show()
        # 获得捐赠按钮所在位置
        newImage = self.processImage(pendingImage, lambda x, y, z : not (y > 200 and z < 100))
        buttonPostionList = self.locateDialogBoxList(newImage, 600)
        # for index in buttonPostionList :
        #     print(index)

        # 获得横线
        newImage = self.processImage(pendingImage, lambda x, y, z : not (y < 50 and z < 50))
        horizontalLineList = self.locateDialogBoxList(newImage, 500)
        # for index in horizontalLineList:
        #     print(index)

        # 获得按钮所在的单元
        rangList = []
        for index in buttonPostionList :
            i = 0
            while i < len(horizontalLineList) :
                if index[1] < horizontalLineList[i][1] :
                    rangList.append(i)
                    break
                else :
                    i += 1
                    if i == len(horizontalLineList) :
                        rangList.append(i)
        # for index in rangList:
        #     print(index)

        # 剪裁按钮所在的位置
        requestList = []
        m = 0
        for index in rangList :
            if index == 0 :
                cellBox = pendingImage.crop((0, 2, 500, horizontalLineList[index][1]))
            elif index == len(horizontalLineList) :
                cellBox = pendingImage.crop((0 , horizontalLineList[index - 1][1] + 84, 500, self.dialogheigth))
            else :
                cellBox = pendingImage.crop((0 , horizontalLineList[index - 1][1] + 84, 500, horizontalLineList[index][1]))
            cellBox = self.processImage(cellBox, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 and abs(x - y) < 3 and abs(x - z) < 3 and abs(y - z) < 3)
            # cellBox.show()
            pendingString = self.m_myOrc.getString(cellBox)
            Request = self.translateStringToRequest(pendingString)
            Request['position'] = buttonPostionList[m]
            m += 1
            requestList.append(Request)
        return requestList

    def locateDialogBoxList(self, image, number):
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

    def pasteImage(self, image) :
        width, height = image.size
        newImage = Image.new('RGB', (width, height), (0, 0, 0))
        newImage.paste(image, (0, 0))
        return newImage

    def processImage(self, image, logicExpression) :
        ''' 将图片按照指定算法转化为黑白图片 '''
        newImage = self.pasteImage(image)
        newImage = newImage.convert("RGB")
        pixdata = newImage.load()
        for y in range(newImage.size[1]):
            for x in range(newImage.size[0]):
                if logicExpression(pixdata[x, y][0], pixdata[x, y][1], pixdata[x, y][2]):
                    pixdata[x, y] = (0, 0, 0)
                else:
                    pixdata[x, y] = (255, 255, 255)
        return newImage



instpictureAnalysis = pictureAnalysis()
print(instpictureAnalysis.getImageRequestList(os.getcwd() + "\\picture\\screenshort.png"))