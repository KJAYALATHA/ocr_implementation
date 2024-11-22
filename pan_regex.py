import cv2
import re
import json
import ftfy
import pytesseract
from pytesseract import Output



class PAN_Info_Extractor_Regex:
    def __init__(self):
        self.extracted = {}

    def find_pan_number(self, ocr_text):
        pan_number_patn = '[A-Z]{5}[0-9]{4}[A-Z]{1}'
        match = re.search(pan_number_patn, ocr_text)
        if match:
            return match.group()

    def find_name(self, ocr_text):
        pan_name_patn = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+\b'
        match = re.search(pan_name_patn, ocr_text)
        if match:
            return match.group()
    def find_name_updated(self, ocr_text):
        all_matches = []
        adhar_name_patterns = [
            r'\b[A-Z]{4,}\s[A-Z]{3,}\s(?:[A-Z]+|[A-Z])\b',
            r'\b[A-Z]{4,}\s(?:[A-Z]{3,}|[A-Z])\b',
            r'\b[A-Z]{4,}\b',
            r'\bFathers Name\b',
            r'\bNam\b',
            r'\bName\b'

            #r'\b(?!Government|India|Date|Site)[A-Z]{3,}\b'       
        ]

        split_ocr = ocr_text.split('\n')
        # print('************************************')
        # print(split_ocr)
        # print('************************************88')
       
        for ele in split_ocr:
            dob_patn = r"\d{2}[-/]\d{2}[-/]\d{4}"

            if ('DOB' and 'Year' and 'Birth') not in ele and not re.search(dob_patn, ele):
                for pattern in adhar_name_patterns:
                    match = re.search(pattern, ele)
                    if match:
                        all_matches.append(match.group())
                        break
                        #return match.group()
            else:
                break
        print(all_matches,"=======================")
        card_name = None
        father_name = None
        if(len(all_matches)>0):
            for i in range(len(all_matches)):
                if all_matches[i] == 'Name':
                    card_name = all_matches[i+1]
                    break
                elif all_matches[i] == 'Fathers Name':
                    card_name = all_matches[i-1]
                    break
            else:
                card_name = all_matches[::-1][1]

            #sorted = all_matches[::-1][1]
            return card_name
        else:
            return None
        

    def find_dob(self, ocr_text):
        dob_patn = r"\d{2}[-/]\d{2}[-/]\d{4}"
        match = re.search(dob_patn, ocr_text)
        if match:
            return match.group()
    def clean_text(self,ocr_text):
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s\n/]', '', ocr_text)
    
        return cleaned_text

    def info_extractor(self, front_image, OCR_text=None):
        self.fimage = front_image
        self.OCR_text = OCR_text
        self.Name = 'NAN'
        self.PAN_No = 'NAN'
        self.DateOB = 'NAN'

        img = self.fimage
        if self.OCR_text is None:
            config_tesseract = '--tessdata-dir tessdata --oem 3'
            OCR_text = pytesseract.image_to_string(img,lang='eng',config=config_tesseract)
            result = pytesseract.image_to_data(img,lang='eng',config=config_tesseract,output_type=Output.DICT)
        # OCR_text = ftfy.fix_text(self.OCR_text)
        # OCR_text = ftfy.fix_encoding(OCR_text)
        cleaned_text = self.clean_text(OCR_text)
        
        self.PAN_No = self.find_pan_number(cleaned_text)
        self.Name = self.find_name_updated(cleaned_text)
        self.DateOB = self.find_dob(cleaned_text)
        # print('cleaned text')
        # print(cleaned_text)

        self.extracted = {
            'PAN_number': self.PAN_No,
            'Name': self.Name,
            'DOB': self.DateOB,
        }
        return json.dumps(self.extracted)
