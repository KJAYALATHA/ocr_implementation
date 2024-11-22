import pytesseract
import cv2
from text_extraction import extractText,extractTextForRotation

def check_keywords(text):
    keywords = ["DOB", "Government","India","Aadhar", "Female", "Male",'Address','Uni','Identification','Identi','Add','ress','S/0']
    for keyword in keywords:
        if keyword in text:
            return True
    return False

def rotate_image_based_direction(image):
    for i in range(4):
        rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        text,result = extractTextForRotation(rotated)
        if check_keywords(text):
            return rotated,result,text
    print("image cant able to find direction")
    return rotated,result,text
    # if(image.shape[0]>image.shape[1]):
    #     rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #     return rotated,result,text
    # else:
    #     return rotated,result,text
