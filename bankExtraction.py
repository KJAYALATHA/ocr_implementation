import pytesseract
import os
import cv2
import matplotlib.pyplot as plt
from pytesseract import Output

folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\PAN Copies'
files = os.listdir(folder_path)


def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()
print(files)
config_tesseract = '--tessdata-dir tessdata --oem 3'


def image_orientation(imgae):
    try:
        results = pytesseract.image_to_osd(imgae, output_type=Output.DICT,lang='eng+osd', config=config_tesseract)
        return results["orientation"], results["rotate"]
    except Exception as e:
        return None

for file_name in files:
    try:
        image_path = folder_path+'\\'+file_name+'\\'+'pan_front.jpg'
        image = cv2.imread(image_path)
        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_orientation(imgGray)
        show_img(imgGray)
        
        #imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        #imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
        #value,imgThresh = cv2.threshold(imgBlur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #result = pytesseract.image_to_string(imgThresh,lang='eng',config=config_tesseract)
        #print(result)
        #show_img(imgGray)
        
        print("===========================")
    except Exception as e:
        print(e)

