from aadhar_pan_extractor import Pan_Info_Extractor,Aadhar_Info_Extractor
import os
extractor = Aadhar_Info_Extractor()
extractor_pan = Pan_Info_Extractor()

result = extractor.info_extractor('Small Aadhar.jpg')
print(result)
# folder_path = r'C:\\Users\\jayalatha.k\\Downloads\\PAN Copies'
# files = os.listdir(folder_path)

# for file_name in files:
#     try:
#         image = folder_path+'\\'+file_name+'\\'+'pan_front.jpg'
#         result = extractor_pan.info_extractor(image)
#         print(result)
#         print("==================================")
#     except:
#         print("proper no")