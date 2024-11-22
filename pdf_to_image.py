from pdf2image import convert_from_path
import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()

poppler_path = r'C:\Program Files\poppler-24.02.0\Library\bin'

def get_photo_border(img):
    print("going inside for get photo border function the image is")
    
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
                approx = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.int32)
                return approx,imgGray
    
    return None,imgGray


def extract_image_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)
    
    photo_border,gray = get_photo_border(img)
    #print("after getting border")
    #show_img(gray)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    if photo_border is not None:
        cv2.drawContours(mask, [photo_border], -1, 255, -1)
        

        #check = cv2.bitwise_and(img,img, mask=mask)
        (y, x) = np.where(mask==255)
        (beginX, beginY) = (np.min(x), np.min(y))
        (endX, endY) = (np.max(x), np.max(y))
        card = gray[beginY:endY, beginX:endX]
        
        return card       
    else:
        print("Photo border not found.")
        return gray
    
#extract_image_from_pdf('C:\\Users\\jayalatha.k\\Downloads\\Aadhar Copies\\GS10142362\\GS10142362_front.pdf')
        
    
