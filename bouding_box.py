import cv2


def get_text_position(text_bbox, image_width):
    print(text_bbox,"sowthriiii")
    text_center_x = text_bbox[0] + text_bbox[2] / 2
    print(text_center_x,"checkingggg") 
    if text_center_x < image_width / 2:
        return "left"
    elif text_center_x >  image_width / 2:
        return "right"
    else:
        return "middle"

def bouding_box(result,i,img,color = (0, 0, 255)):

    x = result['left'][i]
    y= result['top'][i]
    w = result['width'][i]
    h = result['height'][i]
    print(x,y,w,h)
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    
    return x,y,w,h

def find_region(result,image):
    img_copy = image.copy()  
    min_confidence = 10
    print(result['text'],"resulttttttttttttttttt")
    for i in range(len(result['text'])):
        confidence = int(result['conf'][i])
        if(confidence > min_confidence):
            text = result['text'][i]
            if not text.isspace() and len(text)>3 and 'Address' in text:
                x,y,w,h = bouding_box(result,i,img_copy) 
                address_bouding = get_text_position(image_width=img_copy.shape[1],text_bbox=[x,y,w,h])     
                return img_copy,address_bouding,y   

                print(text,"sowthri")
                #cv2.putText(img_copy, text, (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 2.1, (0, 0, 100), 2)
    
    return img_copy,None,None
    

def cropImage(image, row_start,address_position):
    print(row_start,"rowstart")

    #text_center_x = text_bbox[0] + text_bbox[2] / 2

    print(address_position,"===========address position")

    if(row_start > 2):
        row_start -= 2


    if address_position == 'right':
        cropped_image_address = image[row_start:, image.shape[1] // 2:]
    else:
        cropped_image_address = image[row_start :, :]
    height, width = cropped_image_address.shape[:2]
    bounding_box = {
        'x': 0,
        'y': row_start,
        'width': width,
        'height': height
    }
    print(cropped_image_address.shape,"inside bounding boxxxx")

    return cropped_image_address, bounding_box