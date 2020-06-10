# tessarect  我训练了半天还是不好用  所以自己写一个
from PIL import Image
import json


def get_char_point_h(pixdata, size, boxarr, blackpoint) :
    boxs = []
 
    for  box in boxarr:
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
        boxs.append((blackpoint[box[0]], min ,blackpoint[box[1]], max))
    # print(boxs)
    return boxs


def get_char_point_v(pixdata, size) :
    blackpoint = []
    boxs = []
    for x in range(size[0]) :
        for  y in range(size[1]):
            if pixdata[x, y][0] == 0 :   # 找到黑色像素点
                blackpoint.append(x)
                break

    temp = 0
    while True:
        for x in range(1, 200):
            if  temp + x >= len(blackpoint) or blackpoint[temp + x] != blackpoint[temp] + x:
                boxs.append((temp, temp + x - 1))
                temp = temp + x
                break
        if temp >= len(blackpoint) : # 到头了 结束循环
            break
    return boxs, blackpoint

def get_char_point(img) :
    img = img.convert("RGB")
    pixdata = img.load()    
    size = (img.size[0], img.size[1])
    boxs, blackpoint = get_char_point_v(pixdata, size)
    boxs =  get_char_point_h(pixdata, size, boxs, blackpoint)
    return convert_json(pixdata, size, boxs) 
    
    
def convert_json(pixdata, size, boxs) :
    arm_num = []
    for box in boxs :
        points = []
        for y in range(box[1], box[3] + 1) : 
            point = []
            for x in range(box[0], box[2] + 1) :
                if pixdata[x, y][0] == 0 :
                    point.append(1)
                else :
                    point.append(0)
            points.append(point)
        temp = {
            "value" : None,
            "box_size" : [box[2] - box[0] + 1, box[3]- box[1] + 1],
            "points" : points,     
        }
        arm_num.append(temp)
    
    my_font = {"army" : arm_num}
    # print(my_font)
    return my_font


    
def json_get() :
    with open("army.json", "r", encoding='utf-8') as f:
        data2 = json.loads(f.read())    # load的传入参数为字符串类型
    return data2

def json_save( my_font) :
    with open("army.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(my_font))

class my_ocr():
    fonts = None
    index = None
    main_font = None
    def __init__(self, index): 
        self.main_font = json_get() 
        self.fonts = self.main_font[index] 
        self.index = index


    def get_string(self, img):
        img = img.convert("RGB")
        pixdata = img.load()
        my_string = ''    
        size = (img.size[0], img.size[1])
        boxs, blackpoint = get_char_point_v(pixdata, size)
        boxs =  get_char_point_h(pixdata, size, boxs, blackpoint) 
        for box in boxs :
            my_string =  my_string + self.get_char(box, pixdata)
        return my_string 

    def get_char(self, box, pixdata):
        w = box[2] - box[0] + 1
        h = box[3] - box[1] + 1
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
        # 比较查找数组
        for font in self.fonts :
            if w == font['box_size'][0] and h == font['box_size'][1] :                
                if self.compare_char(points ,font['points'], (w, h)) :
                    return font['value']
                else :
                    continue       
        # 没有这个字
        return self.add_char([w, h], points)




    def compare_char(self, src_points, dir_points, size):
        for y in range(size[1]) :
            for x in range(size[0]) :
                if src_points[y][x] != dir_points[y][x] :
                    return False
        return True

    def add_char(self, size, points) :
        img = Image.new('RGB', (size[0], size[1]), (0, 0, 0))
        img = img.convert("RGB")
        pixdata = img.load()
        for y in range(size[1]) :
            for x in range(size[0]) :
                if points[y][x] == 1 :   # 黑点
                    pixdata[x, y] = (0, 0 ,0)
                else :
                    pixdata[x, y] = (255, 255, 255)
        img.show()
        char = input('输入此图片的值：')
        temp = {
            "value" : char,
            "box_size" : size,
            "points" : points,     
        }
        self.fonts.append(temp)
        self.main_font[self.index] = self.fonts
        json_save(self.main_font)
        return char


# myfont = my_ocr('army')
# # print(myfont.fonts)
# img = Image.open('cl2.coc.exp119.tif')
# print(myfont.get_string(img))

# myfont = json_get()
# print(myfont)

# img = Image.open('cl2.coc.exp138.tif')
# my_font =  get_char_point(img)
# my_font = convert_json() 
# print( my_font["army"][0]["points"][1][1])




