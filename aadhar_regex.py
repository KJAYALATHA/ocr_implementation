import json
import ftfy
import pytesseract
import regex as re




class Aadhar_Info_Extractor_Regex:
    def __init__(self):
        self.extracted = {}

    def find_adhar_number(self, ocr_text):
        
        adhar_number_patn = '[0-9]{4}\s[0-9]{4}\s[0-9]{4}'
        match = re.search(adhar_number_patn, ocr_text)
        if match:
            return match.group()
    def find_name_updated(self, ocr_text):
        all_matches = []
        adhar_name_patterns = [
            r'\b(?!Government|India|Date|Site)[A-Z][a-z]+\s[A-Z][a-z]+\s(?:[A-Z][a-z]+|[A-Z]+)\b',
            r'\b(?!Government|India|Date|Site)[A-Z][a-z]+\s(?:[A-Z][a-z]+|[A-Z])\b',
            r'\b(?!Government|India|Date|Site)[A-Z][a-z]{3,}\b'        
        ]

        split_ocr = ocr_text.split('\n')
       
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
        #print(all_matches,"=======================")
        if(len(all_matches)>0):
            sorted = all_matches[::-1][0]
            return sorted
        else:
            return None
       

    def find_name(self, ocr_text):
        adhar_name_patn = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$'

        split_ocr = ocr_text.split('\n')
        for ele in split_ocr:
            match = re.search(adhar_name_patn, ele)
            if match:
                return match.group()

    def find_dob(self, ocr_text):
       
        dob_patn = r"\d{2}[-/]\d{2}[-/]\d{4}"
        yob_patn = '[0-9]{4}'
        DateOfBirth = None
        if 'DOB' in ocr_text:
            match = re.search(dob_patn, ocr_text)
            if match:
                DateOfBirth = match.group()
        if 'Year of Birth' in ocr_text:
            match = re.search(yob_patn, ocr_text)
            if match:
                DateOfBirth = match.group()
        return DateOfBirth

    def find_gender(self, ocr_text):
        if 'Female' in ocr_text or 'FEMALE' in ocr_text:
            GENDER = 'Female'
        elif 'Male' in ocr_text or 'MALE' in ocr_text:
            GENDER = 'Male'
        else:
            GENDER = 'NAN'
        return GENDER


    def info_extractor(self, front_image,OCR_text = None):
        
        self.fimage = front_image
        self.OCR_text = OCR_text
        self.Name = 'NAN'
        self.Gender = 'NAN'
        self.DateOB = 'NAN'
        self.Aadhar_No = 'NAN'
        self.New_Name = 'NAN'
        
        # front image
        img = self.fimage
        if(self.OCR_text is None):
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
            self.OCR_text = pytesseract.image_to_string(img,lang='eng') 
        OCR_text = ftfy.fix_text(self.OCR_text)
        OCR_text = ftfy.fix_encoding(OCR_text)
        self.Aadhar_No = self.find_adhar_number(OCR_text)
        self.Name = self.find_name(OCR_text)
        self.DateOB = self.find_dob(OCR_text)
        self.Gender = self.find_gender(OCR_text)
        self.New_Name = self.find_name_updated(OCR_text)


        self.extracted = {
        'Aadhar_number': self.Aadhar_No,
        'Name': self.Name,
        'NewName':self.New_Name,
        'Gender': self.Gender,
        'DOB': self.DateOB,
        
        }
        return json.dumps(self.extracted)

