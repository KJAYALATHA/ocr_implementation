from easyocr import Reader
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import numpy as np

import re

def has_pincode(text):
    pattern = re.compile(r'\b\d{6}\b') 
    matches = pattern.findall(text)
    return bool(matches)
def has_word(text, words):
    return any(word in text for word in words)
words_to_check = ["Address", "ress", "Addr", "Add"]
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
def draw_img(img, lt, br, color=(0,0,255),thickness=2):
  cv2.rectangle(img, lt, br, color, thickness)
  return img,lt,br


def eacy(img):
    aadr_status = False
    language_list = ['hi','en']
    reader = Reader(language_list)
    results = reader.readtext(img,detail=1,paragraph=True)
    img1 = img.copy()

    for result in results:
        bbox = result[0]
        text = result[1]  
     
            
        if has_word(text, words=words_to_check):
            lt, rt, br, bl = box_coordinates(bbox)
           
            img1 = draw_img(img1, lt, br)
            aadr_status = True
            break
    
      
    if(not(aadr_status)):
      print("aadress word is not found")
      for result in results:
          bbox = result[0]
          text = result[1]
          if(has_pincode(text)):
            lt, rt, br, bl = box_coordinates(bbox)
            #print(bbox, text,'sowthriii')
            img1 = draw_img(img1, lt, br)
            break
    try:
      cropped_img = img[lt[1]:br[1], lt[0]:br[0]]
    except:
      cropped_img = img1
    
  
    
    return cropped_img
    
# image = cv2.imread('check_image.png')
# eacy(image)