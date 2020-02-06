import pytesseract
from PIL import Image
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR';
image = Image.open('D:\\COC_support_py\\COC-support\\google.png');
code = pytesseract.image_to_string(image, lang = 'chi_sim');
print(code);