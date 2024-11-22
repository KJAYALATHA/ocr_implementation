import matplotlib.pyplot as plt
import os
#import json
from find_direction import check_keywords,rotate_image_based_direction
from pdf_to_image import extract_image_from_pdf
from image_preprocess import preprocess_image,simple_preprocess
#from aadhar_regex import Aadhar_Info_Extractor_Regex
from text_extraction import extractText,extractTextForRotation
from bouding_box import find_region,cropImage
from LLM_try import find_structure
import cv2
from testing_final import remove_border_and_lines
from eacy_ocr_implementation import eacy


def show_img(img):
  plt.axis("off")
  plt.imshow(img,cmap='gray')
  
  plt.show()
    

folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\Aadhar Copies'
files = os.listdir(folder_path)

for i in files:
   pdf_path = folder_path+'\\'+i+'\\'+i+'_back.pdf'
   print(pdf_path)
   cropped_image = extract_image_from_pdf(pdf_path)
   ocr_text,result = extractTextForRotation(cropped_image)
   if check_keywords(ocr_text):
      final_image = cropped_image
   else:
      final_image,result,ocr_text = rotate_image_based_direction(cropped_image)

  
   address_image = eacy(final_image)

   #find_structure(address_image)
   # img = preprocess_image(address_image)
   # show_img(img)
   process = simple_preprocess(address_image)
   #show_img(process)
   ocr_text_addr,result_addr = extractText(process)

   #print(ocr_text_addr,"ocr text")



   image,address_position,y_axis = find_region(result=result_addr,image=process)
 
   print(address_position,"===============================")

   cropped_image, bounding_box = cropImage(process,y_axis,address_position)

   print(f'====================={address_image.shape}========main image======================')
   ocr_text_addr,result_addr = extractText(cropped_image)
   print(ocr_text_addr)
   
   show_img(cropped_image)

   