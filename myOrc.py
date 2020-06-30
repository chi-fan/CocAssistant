from PIL import Image
import os
import jsonFile as jF

class myOrc() :
    orcFile = "myOrc.json"     # armyChinese.json
    allFonts = None
    m_jsonFile = None
    m_fontBoxes = None
    def __init__(self, fileName = None) :
        if not fileName :
            self.orcFile = fileName
        self.m_jsonFile = jF.jsonFile(os.getcwd() + "\\" + self.orcFile)
        self.allFonts = self.m_jsonFile.jsonGetFile()
        self.m_fontBoxes = fontBoxes()
        if not 'finish' in self.allFonts.keys() :
            self.allFonts['finish'] = []
            self.allFonts['unFinish'] = []
            self.m_jsonFile.jsonSaveFile(self.allFonts)

    def getString(self, img):
        img = img.convert("RGB")
        pixdata = img.load()
        stringInPicture = ''
        boxes = self.m_fontBoxes.getFontBoxes(pixdata, img.size)
        for box in boxes :
            stringInPicture =  stringInPicture + self.getChar(box, pixdata)
        return stringInPicture

    def getChar(self, box, pixdata):
        width = box[2] - box[0] + 1
        length = box[3] - box[1] + 1
        # 将像素点编辑成数组
        points = []
        for y in range(box[1], box[3] + 1) :
            point = []
            for x in range(box[0], box[2] + 1) :
                if pixdata[x, y][0] == 0 :
                    point.append(1)
                else :
                    point.append(0)
            points.append(point)

        for font in self.allFonts['finish'] :
            if [width, length] == font['boxSize'] :
                if self.comparaChar(points, font['points'], (width, length)) :
                    return font['value']
                else :
                    continue

        for font in self.allFonts['unFinish'] :
            if [width, length] == font['boxSize'] :
                if self.comparaChar(points, font['points'], (width, length)) :
                    return ''
                else :
                    continue

        return self.addChar((width, length), points)

    def comparaChar(self, sourcePoints, destinationPoints, size) :   #待优化算法
        for y in range(size[1]) :
            for x in range(size[0]) :
                if sourcePoints[y][x] != destinationPoints[y][x] :
                    return False
        return True

    def addChar(self, size, points) :
        img = Image.new('RGB', (size[0], size[1]), (0, 0, 0))
        img = img.convert("RGB")
        pixdata = img.load()
        for y in range(size[1]) :
            for x in range(size[0]) :
                if points[y][x] == 1 :
                    pixdata[x, y] = (0, 0 ,0)
                else :
                    pixdata[x, y] = (255, 255, 255)
        img.show()
        char = input('输入此图片的值：')
        temp = {
            "value" : char,
            "boxSize" : size,
            "points" : points,
        }
        if char :
            self.allFonts['finish'].append(temp)
        else :
            self.allFonts['unFinish'].append(temp)
        self.m_jsonFile.jsonSaveFile(self.allFonts)
        return char

class fontBoxes() :
    ''' 将图片中的字符提取出一个像素点集合'''
    def getFontBoxes(self, pixdata, size) :
        boxesX, blackpointX, boxesY, blackpointY = self.getCharBoundary(pixdata, size)
        return self.getCharPoint(pixdata, size, boxesX, blackpointX, boxesY, blackpointY)

    def getCharBoundary(self, pixdata, size) :
        blackpointX = []
        boxesX = []
        blackpointY = []
        boxesY = []

        for y in range(size[1]) :
            for  x in range(size[0]):
                if pixdata[x, y][0] == 0  :
                    blackpointY.append(y)
                    break
        pointY = 0
        y = 0
        while pointY < len(blackpointY) :
            if pointY + y >= len(blackpointY) or blackpointY[pointY + y] != blackpointY[pointY] + y:
                boxesY.append((pointY, pointY + y - 1))
                pointY = pointY + y
                y = 0
                continue
            y += 1

        for boxY in boxesY :
            boxX = []
            blackpoint = []
            for x in range(size[0]) :
                for  y in range(blackpointY[boxY[0]], blackpointY[boxY[1]]):
                    if pixdata[x, y][0] == 0 :
                        blackpoint.append(x)
                        break
            pointX = 0
            x = 0
            while pointX < len(blackpoint) :
                if pointX + x >= len(blackpoint) or blackpoint[pointX + x] != blackpoint[pointX] + x:
                    boxX.append((pointX, pointX + x - 1))
                    pointX = pointX + x
                    x = 0
                    continue
                x += 1
            boxesX.append(boxX)
            blackpointX.append(blackpoint)
        return boxesX, blackpointX, boxesY, blackpointY

    def getCharPoint(self, pixdata, size, boxesX, blackpointX, boxesY, blackpointY) :
        boxes = []
        for indexY in range(len(boxesY)) :
            for boxX in boxesX[indexY] :
                min = None
                max = None
                for y in range(blackpointY[boxesY[indexY][0]], blackpointY[boxesY[indexY][1]]) :
                    for x in range(blackpointX[indexY][boxX[0]], blackpointX[indexY][boxX[1]] + 1) :
                        if pixdata[x, y][0] == 0 :
                            min = y
                            break
                    if min != None :
                        break
                if min == None :
                    continue

                for y in range(blackpointY[boxesY[indexY][1]], blackpointY[boxesY[indexY][0]], -1) :
                    for x in range(blackpointX[indexY][boxX[0]], blackpointX[indexY][boxX[1]] + 1) :
                        if pixdata[x, y][0] == 0 :
                            max = y
                            break
                    if max != None :
                        break
                if (blackpointX[indexY][boxX[1]] - blackpointX[indexY][boxX[0]]) * (max - min) < 5 :
                    break
                boxes.append((blackpointX[indexY][boxX[0]], min ,blackpointX[indexY][boxX[1]], max))
        return boxes


muOcr = myOrc()
img = Image.open(os.getcwd() + "\\picture\\0.png")
print(muOcr.getString(img))





