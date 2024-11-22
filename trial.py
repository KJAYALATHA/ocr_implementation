from PIL import Image, ImageEnhance
import pytesseract
import re
import os

def extract_pan(path):
    img = Image.open(path)

    # Produce a B/W image
    img = ImageEnhance.Color(img).enhance(0.0)

    # Sharpen the image
    #img = ImageEnhance.Sharpness(img).enhance(2.0)

    # Darken the Image
    img = ImageEnhance.Contrast(img).enhance(2.0)

    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    # Adding custom options
    custom_config = r'--oem 2 --psm 4 '
    config_tesseract = '--tessdata-dir tessdata --oem 2 --psm 4'

    # Extract text from image using tesseract
    extracted_text = pytesseract.image_to_string(img,lang="eng", config=config_tesseract)

    return extracted_text

def find_dob(extracted_text):
    return re.search(r"\d{1,31}/\d{1,12}/\d{4}",extracted_text).group(0)

def find_name(extracted_text):
    return text[text.index("INDIA")+5:extracted_text.index(find_dob(extracted_text))].rstrip("\n").lstrip("\n")

def find_pan(extracted_text):
    if re.search(r"[a-zA-Z]{3}?[abcfghjlptABCFGHJLPT]?[a-zA-z][0-9]{4}[a-zA-Z]", extracted_text):
        return re.search(r"[a-zA-Z]{3}?[abcfghjlptABCFGHJLPT]?[a-zA-z][0-9]{4}[a-zA-Z]", extracted_text).group(0)
    else:
        return extracted_text[extracted_text.index('Number'):].splitlines()[2].replace(' ', '')

#text = extract_pan(r'C:\Users\yusharma\Documents\ABBYY FlexiCapture POCs\KYC - Airtel\Documents\pan\Pan 3.jpg')
# print(text)
# print("NAME \t: ", find_name(text))
# print("DOB \t: ", find_dob(text))
# print("PAN \t: ", find_pan(text))

folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\PAN Copies'
files = os.listdir(folder_path)

for file_name in files:
    image_path = folder_path+'\\'+file_name+'\\'+'pan_front.jpg'
    text = extract_pan(image_path)
    print(text)
    print('=======================================')
    # print("NAME \t: ", find_name(text))
    # print("DOB \t: ", find_dob(text))
    # print("PAN \t: ", find_pan(text))