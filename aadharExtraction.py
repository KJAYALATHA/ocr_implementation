import matplotlib.pyplot as plt
import os
import json
from find_direction import check_keywords,rotate_image_based_direction
from pdf_to_image import extract_image_from_pdf
from image_preprocess import preprocess_image
from aadhar_regex import Aadhar_Info_Extractor_Regex
from text_extraction import extractText,extractTextForRotation
from bouding_box import find_region


extractor = Aadhar_Info_Extractor_Regex()


def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  plt.show()
    

folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\Aadhar Copies'
files = os.listdir(folder_path)

def updatedate_for_result(result_data,extracted_data_from_model):
      if(result_data['AadharNumber'] is None):
         result_data['AadharNumber'] = extracted_data_from_model['Aadhar_number']
      if(result_data['Name'] is None):
         if(data_dict['Name'] is None):
            result_data['Name'] = extracted_data_from_model['NewName']
         else:
            result_data['Name'] = extracted_data_from_model['Name']
      if(result_data['Gender'] is None):
         result_data['Gender'] = extracted_data_from_model['Gender']
      if(result_data['DOB'] is None):
         result_data['DOB'] = extracted_data_from_model['DOB']

for i in files:
   final_processed_result = {"AadharNumber":None,"Name":None,"DOB":None,"Gender":None}
   pdf_path = folder_path+'\\'+i+'\\'+i+'_front.pdf'
   print(pdf_path)
   cropped_image = extract_image_from_pdf(pdf_path)
   
   ocr_text,result = extractTextForRotation(cropped_image)
   if check_keywords(ocr_text):
      final_image = cropped_image
   else:
      final_image,result,ocr_text = rotate_image_based_direction(cropped_image)


   processed_image = preprocess_image(final_image)
   
   
   #image = find_region(result=result,image=final_image)
   #image = find_region(result=result,image=final_image)

   #print('===================from package==============================================')
   

   #try:
   #show_img(final_image)
   results = extractor.info_extractor(final_image)
   
   data_dict = json.loads(results)
   #print(data_dict,"un processed with aadhar result")
   updatedate_for_result(final_processed_result,data_dict)

   
   if(final_processed_result['AadharNumber'] is None or final_processed_result['Name'] is None or final_processed_result['DOB'] is None or final_processed_result['Gender'] is None ):
         results = extractor.info_extractor(processed_image)
         data_dict_processed = json.loads(results)
         updatedate_for_result(final_processed_result,data_dict_processed)
         #print(data_dict_processed,'processed data with aadhar result')
         if(final_processed_result['AadharNumber'] is None or final_processed_result['Name'] is None or final_processed_result['DOB'] is None or final_processed_result['Gender'] is None): 
            results = extractor.info_extractor(final_image,ocr_text)
            
            data_dict_mine_cropped = json.loads(results)
            updatedate_for_result(final_processed_result,data_dict_mine_cropped)
            #print(data_dict_mine_cropped,"passed mine un proceese data")
            if(final_processed_result['AadharNumber'] is None or final_processed_result['Name'] is None or final_processed_result['DOB'] is None or final_processed_result['Gender'] is None):
               processed_ocr_text,processed_result = extractTextForRotation(processed_image)
               results = extractor.info_extractor(processed_image,processed_ocr_text)
               data_dict_mine_processed = json.loads(results)
               updatedate_for_result(final_processed_result,data_dict_mine_processed)
               #print(data_dict_mine_processed,"passed mine proceesed data")   
   print("============================jayalatha===================================")
   print(final_processed_result)
   show_img(final_image)
   
   # except Exception as e:
   #       print(e,"inside exception")
   # finally:
   #    pass
      
      #show_img(image)
    
    
    
    
    


 #ocr_text = "OCR text of the Aadhar card"
   # doc = nlp(ocr_text)
   # print(doc.ents)
   # for ent in doc.ents:
   #  print(ent.label_,"sowthriiii",ent.text)
   #  if ent.label_ == "PERSON":
        
   #      print("Name: findingggg", ent.text)


   # if((final_processed_result['AadharNumber'] or final_processed_result['Name'] or final_processed_result['DOB'] or final_processed_result['Gender'] )is None ):
   #       results = extractor.info_extractor(processed_image)
   #       data_dict_processed = json.loads(results)
   #       updatedate_for_result(final_processed_result,data_dict_processed)
   #       print(data_dict_processed,'processed data with aadhar result')
   #       if(data_dict_processed['Aadhar_number'] is None): 
   #          results = extractor.info_extractor(final_image,ocr_text)
   #          print(results,"passed mine un proceese data")
   #          data_dict_mine_cropped = json.loads(results)
   #          if(data_dict_mine_cropped['Aadhar_number'] is None):
   #             processed_ocr_text,processed_result = extractTextForRotation(processed_image)
   #             results = extractor.info_extractor(processed_image,processed_ocr_text)
   #             print(results,"passed mine proceesed data")  