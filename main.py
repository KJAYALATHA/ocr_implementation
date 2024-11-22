import pytesseract
import cv2
import numpy as np
from PIL import Image
from pytesseract import Output
import matplotlib.pyplot as plt


img = cv2.imread('aadhar.jpg')

rgb = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
print(rgb.shape,"sowthri")

if(rgb.shape[0]>rgb.shape[1]):
    
    print("image is potrait")
    #rotated_image = cv2.rotate(rgb, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated_image = rgb.copy()
else:
    rotated_image = rgb.copy()
scale_factor_width = 1.2  
scale_factor_height = 1.2 
plt.imshow(rotated_image)
plt.axis('off')  # Turn off axis numbers
plt.show()

# Resize the image using the specified scaling factors and interpolation method
resized = cv2.resize(rotated_image, None, fx=scale_factor_width, fy=scale_factor_height, interpolation=cv2.INTER_AREA)
#resized = cv2.resize(rgb, (632, 1022), interpolation=cv2.INTER_AREA)

print(resized.shape,"jaya")

value,thresh = cv2.threshold(resized,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
blurred = cv2.GaussianBlur(thresh, (5, 5), 0)
#blurred = cv2.bilateralFilter(thresh, 9, 75, 75)
edged = cv2.Canny(blurred, 60, 160)
config_tesseract = '--tessdata-dir tessdata'

text = pytesseract.image_to_string(blurred,lang='eng',config=config_tesseract)
result = pytesseract.image_to_data(blurred,lang='eng',config=config_tesseract,output_type=Output.DICT)
print(result['text'])
print(text)
#tesseract --list-langs --> to check the languages support
#tesseract --help-psm --> detail of Page segmentation mode

#page orientation
# img = Image.open('pan_front.jpg')
# print(pytesseract.image_to_osd(img))
def bouding_box(result,i,img,color = (0,0,255)):
    x = result['left'][i]
    y= result['top'][i]
    w = result['width'][i]
    h = result['height'][i]
    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
    return x,y,img
min_confidence = 40
img_copy = blurred.copy()
for i in range(len(result['text'])):
    confidence = int(result['conf'][i])
    if(confidence > min_confidence):
        text = result['text'][i]
        if not text.isspace() and len(text)>0:
            x,y,img = bouding_box(result,i,img_copy)
            #cv2.putText(img_copy,text,(x,y-10),cv2.FONT_HERSHEY_COMPLEX,1.1,(0,0,255))
#print(value)        
plt.imshow(img_copy)
plt.axis('off')  # Turn off axis numbers
plt.show()



