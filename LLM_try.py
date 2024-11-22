import pytesseract
import matplotlib.pyplot as plt
import cv2

def show_img(img):
  plt.axis("off")
  plt.imshow(cv2.cvtColor(img,cv2.COLOR_GRAY2BGR))
  plt.show()

def find_structure(image):
  #image = cv2.imread('check_image.png')
  #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(image,(7,7),0)
  imgThresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 9)
  #value,imgThresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,21))
  dilate = cv2.dilate(imgThresh,kernel=kernel,iterations=2)
  show_img(dilate)
  contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
  for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    print(x,y,w,h)
    print(image.shape,"shape")
    if(h>150 and w > 50):
      cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
  show_img(image)
  
  
#find_structure()


