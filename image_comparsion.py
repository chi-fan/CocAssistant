import re
from PIL import Image
from imageProcess import *

data = 0


# def get_army(img) :
#     img =  img.resize((1920, 1080))   #这里统一格式为1920 * 1080
#     # img.save('cut_in.png', 'PNG')
#     new_image = cutImage(img, (193, 130, 420, 182))
#     # new_image.save('cut_in1.png', 'PNG')
#     new_image = processImage(new_image, lambda x, y, z : x >= 200  and y >= 200 and z >= 200 and abs(x - y) < data and abs(x - z) < data and abs(y - z) < data)
#     new_image.save('cut_in1.png', 'PNG')
#     code = pytesseract.image_to_string(new_image, lang='chi_sim')
#     print(code)


# img = Image.open('screen.jpg')
# # request_list = get_inf(img)
# get_army(img)








