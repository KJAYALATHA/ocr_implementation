import pytesseract
from pytesseract import Output
def extractText(image):
    #config_tesseract = '--tessdata-dir tessdata --oem 3 --psm 4'
    config_tesseract = '--tessdata-dir tessdata --oem 3'
    text = pytesseract.image_to_string(image,lang='eng',config=config_tesseract)
    result = pytesseract.image_to_data(image,lang='eng',config=config_tesseract,output_type=Output.DICT)
    
    return text,result

def extractTextForRotation(image):
    #config_tesseract = '--tessdata-dir tessdata --oem 3 --psm 4'
    config_tesseract = '--tessdata-dir tessdata --oem 3 --psm 6'
    text = pytesseract.image_to_string(image,lang='eng',config=config_tesseract)
    result = pytesseract.image_to_data(image,lang='eng',config=config_tesseract,output_type=Output.DICT)
    
    return text,result