from pdf2image import convert_from_path
from easyocr import Reader
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import imutils
import pytesseract
from re import A
from aadhar_pan_extractor import Pan_Info_Extractor,Aadhar_Info_Extractor
extractor = Aadhar_Info_Extractor()

language_list = ['en']
reader = Reader(language_list)


poppler_path = r'C:\Program Files\poppler-24.02.0\Library\bin'

def rotate_image(results):
    print(results,"===============================")

    if(('Male' or 'Female' or 'MALE' or 'FEMALE') in results):
        print("image in correct position")
        return True              
    else:
        return False
counter = 0   
def find_correct_direction(image):
    global counter   
    config_tesseract = '--tessdata-dir tessdata'
    OCR_text = pytesseract.image_to_string(image,config=config_tesseract,lang='eng')
    print(OCR_text)
    show_img(image)
    side = rotate_image(OCR_text)
    if(side):
        return image
    elif(side == False and counter <4):
        counter += 1
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        find_correct_direction(rotated_image)
    else:
        print(counter,"jayalatha")
        print("I cant able to extract the text this is worst image")
        return image



def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()

def get_photo_border(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    imgCanny = cv2.Canny(imgThresh,100,100)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    
    contours, _ = cv2.findContours(imgThre, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        valid_contours = [contour for contour in contours if cv2.contourArea(contour) > 5000]
        
        if valid_contours:
            max_contour = max(valid_contours, key=cv2.contourArea)
            perimeter = cv2.arcLength(max_contour, True)
            approx = cv2.approxPolyDP(max_contour, 0.02 * perimeter, True)
            if len(approx) >= 4:
                x, y, w, h = cv2.boundingRect(approx)
                print(x, y, w, h,"sowthriii")
                approx = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.int32)
                return approx,imgGray
    return None,imgGray

# Assuming 'img' is your Aadhar card image




folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\Aadhar Copies'
files = os.listdir(folder_path)
def pdf_to_image(pdf_path):
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    page_np = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)
    return page_np
for i in files:
    pdf_path = folder_path+'\\'+i+'\\'+i+'_front.pdf'
    print(pdf_path)
    img = pdf_to_image(pdf_path)
    original = img.copy()
    photo_border,gray = get_photo_border(img)
    mask = np.zeros(img.shape[:2], dtype=np.uint8) 
    if photo_border is not None:
        #cv2.drawContours(img, photo_border, -1, (120,255,0), 28)
        #cv2.drawContours(img, [photo_border], -1, (120,255,0), 5)
        img_plate = cv2.drawContours(mask, [photo_border], -1, 255, -1)
        #show_img(mask)
        print('sowthriiiii')
        img_plate = cv2.bitwise_and(img,img, mask=mask)
        #show_img(img_plate)
        (y, x) = np.where(mask==255)
        (beginX, beginY) = (np.min(x), np.min(y))
        (endX, endY) = (np.max(x), np.max(y))
        plate = gray[beginY:endY, beginX:endX]
        
        corrected_image = find_correct_direction(plate)
        #show_img(plate)
        # try:
        #     result = extractor.info_extractor(plate)
        #     print(result)
        # except Exception as e:
        #     print("no add",e)
    else:
        print("Photo border not found.")
        show_img(img)
        
    

# def preprocess_image(image):
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    blur = cv2.GaussianBlur(gray, (5, 5), 0)
#    kernel = np.ones((3, 3), np.uint8)
#    closed = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
   
#    processed_img = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
   
   
#    print("========================================")
#    return processed_img
   