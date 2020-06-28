from PIL import Image
import os
import jsonFile as jF

class myOpticalCharacterRecognition() :
    orcFile = "myOrc.json"     # armyChinese.json
    allFonts = None
    m_jsonFile = None
    m_fontBoxes = None
    def __init__(self):
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
        boxes, blackpoint = self.getCharPointV(pixdata, size)
        return self.getCharPointH(pixdata, size, boxes, blackpoint)

    def getCharPointH(self, pixdata, size, boxArray, blackpoint) :
        boxes = []
        for  box in boxArray:
            min = None
            max = None
            for y in range(size[1]) :
                for x in range(blackpoint[box[0]], blackpoint[box[1]] + 1) :
                    if pixdata[x, y][0] == 0 :
                        min = y
                        break
                if min != None :
                    break

            for y in range(size[1] - 1, 0, -1) :
                for x in range(blackpoint[box[0]], blackpoint[box[1]] + 1) :
                    if pixdata[x, y][0] == 0 :
                        max = y
                        break
                if max != None :
                    break
            boxes.append((blackpoint[box[0]], min ,blackpoint[box[1]], max))
        return boxes

    def getCharPointV(self, pixdata, size) :
        blackpoint = []
        boxes = []
        for x in range(size[0]) :
            for  y in range(size[1]):
                if pixdata[x, y][0] == 0 :   # 找到黑色像素点
                    blackpoint.append(x)
                    break
        temp = 0
        while True:
            for x in range(1, 200):
                if  temp + x >= len(blackpoint) or blackpoint[temp + x] != blackpoint[temp] + x:
                    boxes.append((temp, temp + x - 1))
                    temp = temp + x
                    break
            if temp >= len(blackpoint) : # 到头了 结束循环
                break
        return boxes, blackpoint

muOcr = myOpticalCharacterRecognition()
img = Image.open(os.getcwd() + "\\picture\\0.png")
print(muOcr.getString(img))





