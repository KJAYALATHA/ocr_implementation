from pdf2image import convert_from_path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import imutils
from re import A

poppler_path = r'C:\Program Files\poppler-24.02.0\Library\bin'

def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()

def getContours(img,cThr=[100,100],showCanny=False,minArea=1000,filter=0,draw =False):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    if showCanny:
        show_img(imgThre)

    contours= cv2.findContours(imgThre.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print('========================',contours)
    conts = imutils.grab_contours(contours)
    conts = sorted(conts, key = cv2.contourArea, reverse = True)[:8]
    location = None

    
    for c in conts:
        perimeter = cv2.arcLength(c, True)
        approximation = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approximation) == 4:
            location = approximation
            break
    print(location)
    mask = np.zeros(original.shape, np.uint8) 
    if draw and location is not None:

        img_plate = cv2.drawContours(mask, [location], 0, 255, -1)
        show_img(mask)
        
        # for con in finalCountours:
        #     print(con[4],len(con[4]),"sowthriii")
        #     img_plate = cv2.drawContours(mask,con[4], 0, 255, -1)
        #     show_img(mask)

        #     #img_plate = cv2.drawContours(mask, [location], 0, 255, -1)
    return img,location



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
    imgContours2, conts2 = getContours(img,minArea=2000, filter=4,showCanny=True,
                                                 cThr=[50,50],draw = True)
    
    