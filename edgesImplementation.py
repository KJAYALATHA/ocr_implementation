import numpy as np
import cv2
import pytesseract
import imutils
from pytesseract import Output
from matplotlib import pyplot as plt
from re import A


def show_img(img):
  fig = plt.gcf()
  fig.set_size_inches(20, 10)
  plt.axis("off")
  plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  plt.show()


img = cv2.imread('pan_front_1.jpg')
rotated_image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
# original = img.copy()
#show_img(rotated_image)
(H, W) = img.shape[:2]
# print(H, W)

gray = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
#show_img(gray)


blur = cv2.GaussianBlur(gray, (3, 3), 0)
#show_img(blur)

# edged = cv2.Canny(blur, 60, 160)
# show_img(edged)

# def find_contours(img): # EXTERNAL
#   conts = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#   conts = imutils.grab_contours(conts)
#   conts = sorted(conts, key = cv2.contourArea, reverse = True)[:6]
#   return conts

# conts = find_contours(edged.copy())
# print(conts)


# for c in conts:
#   perimeter = cv2.arcLength(c, True)
#   approximation = cv2.approxPolyDP(c, 0.02 * perimeter, False)
#   print(approximation,"sow")
#   if len(approximation) == 4:
#     larger = approximation
#     break
# print(larger)
  
# cv2.drawContours(img, larger, -1, (120,255,0), 28)
# cv2.drawContours(img, [larger], -1, (120,255,0), 2)
increase = cv2.resize(blur, None, fx=2, fy = 2, interpolation=cv2.INTER_CUBIC)
#show_img(increase)

brightness = 50
contrast = 80
adjust = np.int16(increase)
print(adjust.shape)

adjust = adjust * (contrast / 127 + 1) - contrast + brightness
adjust = np.clip(adjust, 0, 255)
adjust = np.uint8(adjust)
#show_img(adjust)

# processed_img = cv2.cvtColor(adjust, cv2.COLOR_BGR2GRAY)
#value,processed_img = cv2.threshold(adjust,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
processed_img = cv2.adaptiveThreshold(adjust, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
#show_img(processed_img)
config_tesseract = '--tessdata-dir tessdata'
text = pytesseract.image_to_string(processed_img,lang='eng+hin',config=config_tesseract)
result = pytesseract.image_to_data(processed_img,lang='eng+hin',config=config_tesseract,output_type=Output.DICT)
# margin = 1
# img_edges = processed_img[margin:H - margin, margin:W - margin]
# show_img(img_edges)
print(text)
print("============================================")
print(result['text'])



def bouding_box(result,i,img,color = (0,0,255)):
    x = result['left'][i]
    y= result['top'][i]
    w = result['width'][i]
    h = result['height'][i]
    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
    return x,y,img
min_confidence = 50
img_copy = processed_img.copy()
for i in range(len(result['text'])):
    confidence = int(result['conf'][i])
    if(confidence > min_confidence):
        text = result['text'][i]
        
        if not text.isspace() and len(text)>1:
            x,y,img = bouding_box(result,i,img_copy)
            print(text,"sowthri")
            #cv2.putText(img_copy, text, (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 2.1, (0, 0, 100), 2)

#print(value)        
plt.imshow(img_copy)
plt.axis('off')  # Turn off axis numbers
plt.show()