
#C:\Users\jayalatha.k\Downloads\PAN Copies
import os
import cv2
import numpy as np
import pytesseract
import imutils
from pytesseract import Output
from matplotlib import pyplot as plt
from re import A
from imageOrientation import rotate_image

folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\PAN Copies'
files = os.listdir(folder_path)
print(len(files))

def find_direction(image):
    image = cv2.imread(image)
    if(image.shape[0]>image.shape[1]):
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated_image = image.copy()
    return rotated_image


def imageProcessing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    increase = cv2.resize(blur, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    brightness = 50
    contrast = 80
    adjust = np.int16(increase)
    adjust = adjust * (contrast / 127 + 1) - contrast + brightness
    adjust = np.clip(adjust, 0, 255)
    adjust = np.uint8(adjust)
    #value,processed_img = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
    return processed_img
def bouding_box(result,i,img,color = (0,0,255)):
    x = result['left'][i]
    y= result['top'][i]
    w = result['width'][i]
    h = result['height'][i]
    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
    return x,y,img
def extractText(image):
    config_tesseract = '--tessdata-dir tessdata'
    text = pytesseract.image_to_string(image,lang='eng',config=config_tesseract)
    result = pytesseract.image_to_data(image,lang='eng',config=config_tesseract,output_type=Output.DICT)
    print(text)
    return result

for file_name in files:
    try:
        print("========================")
        image = folder_path+'\\'+file_name+'\\'+'pan_front.jpg'
        print(image)
        #image_pro = find_direction(image)
        image = cv2.imread(image)
        image_pro = rotate_image(image)
        # processedImage = imageProcessing(image_pro)
        # result = extractText(processedImage)
        # min_confidence = 30
        # img_copy = processedImage.copy()
        # for i in range(len(result['text'])):
            # confidence = int(result['conf'][i])
            # if(confidence > min_confidence):
            #     text = result['text'][i]
                
            #     if not text.isspace() and len(text)>1:
            #         x,y,img = bouding_box(result,i,img_copy)
            #         print(text,"sowthri")
                    # cv2.putText(img_copy, text, (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 2.1, (0, 0, 100), 2)

        #print(value)        
        plt.imshow(image_pro)
        plt.axis('off')  # Turn off axis numbers
        plt.show()

        print("=======================================================")
        

    except Exception as e:
        print("no proper file")








