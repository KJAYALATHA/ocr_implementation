import cv2
import numpy as np
import matplotlib.pyplot as plt



def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()



def preprocess_image(image):
   #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   increase = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

   blur = cv2.GaussianBlur(increase, (5, 5), 0)
   #imgThresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 9)
   value,imgThresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   #imgThresh = cv2.bitwise_not(imgThresh)
   # Apply histogram equalization to enhance contrast
  #  clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
  #  imgThresh = clahe.apply(imgThresh)
   gamma = 0.5  # Experiment with different gamma values
   imgThresh = np.power(imgThresh/255.0, gamma) * 255.0

   # Apply contrast stretching
   min_val = np.min(imgThresh)
   max_val = np.max(imgThresh)
   imgThresh = (imgThresh - min_val) / (max_val - min_val) * 255.0

   # Convert to uint8
   imgThresh = imgThresh.astype(np.uint8)
  
   kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
  #  imgThresh = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, kernel)
   
   imgThresh = cv2.erode(imgThresh, kernel, iterations=1)  # Erosion to remove small white spots
   imgThresh = cv2.dilate(imgThresh, kernel, iterations=2)
   #imgThresh = cv2.medianBlur(imgThresh,3)
   
   return imgThresh



def simple_preprocess(image):
   custom_kernel = np.ones((1, 1), np.uint8)
   blur = cv2.GaussianBlur(image, (3, 3), 0)
   
   imgThresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
   #value,imgThresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   show_img(imgThresh)
   imgThresh = cv2.dilate(imgThresh, custom_kernel, iterations=1)
   imgThresh = cv2.erode(imgThresh, custom_kernel, iterations=1)
   return imgThresh

def simple_preprocess_pan(image):
   custom_kernel = np.ones((1, 1), np.uint8)
   blur = cv2.GaussianBlur(image, (3, 3), 0)
   
   imgThresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 9)
   #value,imgThresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   show_img(imgThresh)
   imgThresh = cv2.dilate(imgThresh, custom_kernel, iterations=1)
   imgThresh = cv2.erode(imgThresh, custom_kernel, iterations=1)
   return imgThresh
   