import os
import cv2
import numpy as np
import pytesseract
import imutils
from pytesseract import Output
from matplotlib import pyplot as plt
from re import A
from imageOrientation import rotate_image
from image_preprocess import simple_preprocess_pan
from pan_regex import PAN_Info_Extractor_Regex

Pan_Extractor = PAN_Info_Extractor_Regex()


folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\PAN Copies'
files = os.listdir(folder_path)


def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()


for file_name in files:
    final_processed_result = {"PAN_number":None,"Name":None,"DOB":None}
    try:
        image = folder_path+'\\'+file_name+'\\'+'pan_front.jpg'
        image = cv2.imread(image) 
        rotated_image = rotate_image(image)
        gray = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
        simple_pre = simple_preprocess_pan(gray)

       
        result = Pan_Extractor.info_extractor(rotated_image)
        print(result,"original image")
        result1 = Pan_Extractor.info_extractor(simple_pre)
        print(result1,"preprocessed image")
        show_img(rotated_image)

    except Exception as e:
        print(e," coming main")