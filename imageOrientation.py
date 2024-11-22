import pytesseract
from pytesseract import Output
import cv2
from PIL import Image

config_tesseract = '--tessdata-dir tessdata --oem 3'

def image_orientation(imgae):
    try:
        pil_img = Image.fromarray(imgae)
        results = pytesseract.image_to_osd(pil_img, output_type=Output.DICT,lang='eng+osd', config=config_tesseract)
        return results["orientation"]
    except Exception as e:
        print(e)
        return None
    
def rotate_image(img):
    orientation = image_orientation(img)
    
    if orientation == 0:
        return img
    elif orientation == 90:
        rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return rotated_img     
    elif orientation == 180:
        rotated_img = cv2.rotate(img, cv2.ROTATE_180)
        return rotated_img
    elif orientation == 270:
        rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        return rotated_img       
    else:
        print("cant able to find orientation=================")
        return img