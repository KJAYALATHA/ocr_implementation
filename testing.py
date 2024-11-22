from easyocr import Reader
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import matplotlib.pyplot as plt
# Function to preprocess the image
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    increase = cv2.resize(blur, None, fx=2, fy = 2, interpolation=cv2.INTER_CUBIC)

    brightness = 30
    contrast = 40
    adjust = np.int16(increase)


    adjust = adjust * (contrast / 127 + 1) - contrast + brightness
    adjust = np.clip(adjust, 0, 255)
    adjust = np.uint8(adjust)

    # Apply adaptive thresholding to binarize the image
    thresh = cv2.adaptiveThreshold(adjust, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
    #value,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return thresh



language_list = ['en']
#img = cv2.imread('pan_front.jpg')
rotated_image = cv2.imread('pan_front_1.jpg')
img = cv2.rotate(rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Preprocess the image
processed_img = preprocess_image(img)
#processed_img = img.copy()

reader = Reader(language_list)

results = reader.readtext(processed_img)
print(results)

font_path = 'Nirmala-UI.ttf'  
font = ImageFont.truetype(font_path, size=22)

def write_text(text, x, y, img, font, color=(50,50,255), font_size=22):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y), text, font=font, fill=color)
    img = np.array(img_pil)
    return img

def box_coordinates(box):
  (lt, rt, br, bl) = box
  lt = (int(lt[0]), int(lt[1]))
  rt = (int(rt[0]), int(rt[1]))
  br = (int(br[0]), int(br[1]))
  bl = (int(bl[0]), int(bl[1]))
  return lt, rt, br, bl

def draw_img(img, lt, br, color=(200,255,0),thickness=2):
  cv2.rectangle(img, lt, br, color, thickness)
  return img
details = {}
img1 = processed_img.copy()
for (box, text, probability) in results:
  print(box, text, probability)
  lt, rt, br, bl = box_coordinates(box)
  img1 = draw_img(img1, lt, br)
  #img1 = write_text(text, lt[0], lt[1], img1,font)

#plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
plt.imshow(img1)
plt.axis('off')  # Turn off axis numbers
plt.show()
